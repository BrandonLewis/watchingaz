from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader, Template

from watchingaz.bills.models import (Bill, ActionType, Version, VersionText, 
                                     BillPageView, Sponsor)
from watchingaz.tools.forms import (AddTrackerShortForm, SearchBarForm, 
                                    QuestionForm)
from watchingaz.bills.utils import get_bill_text
from watchingaz.utils import number_to_leg, legislature_to_number

import json, datetime, os

def bill_index(request):
    """
    The bill index displays basic info abouts bill ordered in a couple of
    categories:
        most_viewed = Bills that have either the most views in a day or the
                      most views total
        action_list = Bills that have been placed on the floor calendar for whichever
                      chamber they are currently in
        user_related = Bills that might be of interest to a logged in visitor based
                       on their past viewing preferences
        user_tracked = bills that a user is tracking with an indicator showing whether
                       there has been any action on this bill since their last visit
                       or if there is any action pending
    """
    c = {}
    most_viewed = Bill.objects.filter(session__name=settings.DEFAULT_SESSION
                                      ).order_by('-page_views_count')[:23]
    paged = Paginator(most_viewed, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        most_viewed_bills = paged.page(page)
    except (EmptyPage, InvalidPage):
        most_viewed_bills = paged.page(paged.num_pages)
    c['title'] = "Arizona Legislation - Watching AZ"
    c['total_pages'] = paged.num_pages
    c['most_viewed'] = most_viewed_bills
    c['total_items'] = paged.count
    if request.is_ajax():
        response = HttpResponse(mimetype='application/json')
        t = loader.get_template('bills/_paged_items.json')
        response.write(t.render(RequestContext(request, context)))
        return response
    c['upper_newest'] = Bill.objects.filter(chamber='upper',
                                            session__name=settings.DEFAULT_SESSION
                                            ).order_by('-created_at')[:10]
    c['lower_newest'] = Bill.objects.filter(chamber='lower',
                                            session__name=settings.DEFAULT_SESSION
                                            ).order_by('-created_at')[:10]
    c['upper_recent_action'] = Bill.objects.filter(chamber='upper',
                                            session__name=settings.DEFAULT_SESSION
                                             ).order_by('actions__date')[:10]
    c['lower_recent_action'] = Bill.objects.filter(chamber='lower',
                                            session__name=settings.DEFAULT_SESSION
                                             ).order_by('actions__date')[:10]
                                             
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        try:
            c['tracked_bills'] = profile.tracked_items.filter(
                    tracker__content_type__model='bill')
        except ObjectDoesNotExist:
            pass

    return render_to_response('bill_index.html', RequestContext(request, c))

def bills_by_chamber(request, term, session, chamber, bill_type):
    chmbr = {'senate': 'upper', 'house': 'lower'}

    if bill_type == 'newest':
        bills = Bill.objects.filter(chamber=chmbr[chamber.lower()],
                                    session__name="50th-1st-regular"
                                    ).values_list('number', 'title', 'session__name'
                                                  ).order_by('-created_at')
    elif bill_type == 'all':
        bills = Bill.objects.filter(chamber=chmbr[chamber.lower()],
                                    session__name="50th-1st-regular").order_by(
                'number')
    else:
        bills = Bill.objects.filter(chamber=chmbr[chamber.lower()],
                                    session__name="50th-1st-regular",
                                    type=bill_type
                                    ).values_list('number', 'title', 'session__name'
                                                  ).order_by('-created_at')
    paged = Paginator(bills, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        newest_bills = paged.page(page)
    except (EmptyPage, InvalidPage):
        newest__bills = paged.page(paged.num_pages)
    c = {}
    c['term'] = term
    c['session'] = session
    c['title'] = "Newest Bills in the %s - Anvil Rock Road" % chamber.capitalize()
    c['newest'] = newest_bills
    c['chamber'] = chamber

    if request.is_ajax():
        return render_to_response('_bills_by_chamber.json',
                                  RequestContext(request, c))

    return render_to_response('bills_by_chamber.html',
                              RequestContext(request, c))

def bill_overview(request, term, session, bill_number):
    """
    Individual Bill Detail shows sponsors, versions, actions(past and pending)
    with a link to show text and comments and also an option to view the Arizona
    Statues that this legislation affects when applicable
    """
    session = number_to_leg(term, session)

    bill = get_object_or_404(Bill, number=bill_number, session__name=session)
    # TODO replace this with real analytics
    bill.page_views_count += 1
    page_view, c = bill.page_views.get_or_create(date=datetime.date.today())
    page_view.views += 1
    page_view.save()
    bill.save()

    ###################################
    # Basic Bill Information
    ###################################
    c = {}
    c['title'] = "%s - %s" % (bill.number, bill.title)
    c['bill'] = bill
    # just need the name and document_id or each summary
    # sorting by date should be replaced by date added for the new session
    # need to make it so that the user can select a summary to read
    c['summaries'] = bill.documents.filter(doc_type="summary")
    if 'summary' in request.GET and request.GET['summary']:
        pass
    for summary in c['summaries']:
        if summary.doc_id:
            c['text'] = get_summary(summary)
            break
    else:
        c['text'] = ''
    
    c['sponsors'] = Sponsor.objects.filter(bill=bill).order_by('type')
    c['chamber'] = {'upper': 'Senate', 'lower': 'House'}[bill.chamber]
    c['other_chamber'] = {'upper': 'House', 'lower': 'Senate'}[bill.chamber]
    try:
        c['latest_action'] = bill.actions.latest()
    except ObjectDoesNotExist:
        c['latest_action'] = None
    c['latest_action'] = _render_action_description(c['latest_action'], bill)

    ###################################
    # Charts and User Actions
    ###################################
    actions = bill.actions.all().order_by('order')
    simi = []
    for act in actions:
        action = {}
        action['start'] = act.date.strftime('%Y %m %d')
        action['title'] = act.action
        action['description'] = act.action
        simi.append(action)
    c['actions'] = actions
    c['graph_actions'] = json.dumps(simi)
    c['bill_graph'] = json.dumps(bill.get_bill_stats())
    c['support'] = json.dumps(bill.get_user_support())
    c['tracker_form'] = AddTrackerShortForm(
            initial={'object_id': bill.id,
                     'content_type': ContentType.objects.get(model="bill").id,
                     'where_to': request.get_full_path()}
            )
    ###################################
    # bill tracking
    ###################################
    if request.user.is_authenticated():
        tracked = request.user.profile.is_tracking(bill.id)
        if tracked:
            c['is_tracking'] = True
    elif 'trackers' in request.COOKIES:
        if bill.id in request.COOKIES['trackers']:
            c['is_tracking'] = True
    return render_to_response('bill.html', RequestContext(request, c))

def bill_text(request, term, session, bill_number, version):
    """
    Display the bill text with comments and permalinks to sections.
    """
    session_name = get_session(term, session)

    c = {}
    c['no_throttle'] = True
    c['can_comment'] = True
    c['prefs'] = {
        "beta": {
            "show_statute": True,
            "email_section": True,
        }
    }
    c['version'] = get_object_or_404(Version, bill__number=bill_number,
                                     bill__session__name=session_name, name=version.replace('-', ' '))
    c['title'] = "%s - %s" % (c['version'].bill.number, c['version'].name)
    version_url = c['version'].url.split('/')[-1]
    c['text'] = get_bill_text(term=term, session=session, version=c['version'])
    c['text'] = "{% load comments %}\n" + c['text']
    c['text'] = Template(c['text']).render(RequestContext(request, c))

    return render_to_response('bill_text.html',
                              RequestContext(request, c))

def get_summary(summary):
    return ''

def get_session(term, session):
    return _get_session(term, session)

def _get_session(term, session):
    """wrapper around number_to_session(term, session)
    so that it raises a Http404 for invalid session|term
    """
    try:
        session = number_to_leg(term, session)
    except AttributeError:
        raise Http404('Invalid Legislative Session')
    return session
    
def _render_action_description(action, bill):
    if not action:
        return """<p>This bill is still awaiting its first 
        reading. Check back later or track this bill to keep up to date.</p>"""
    description = ActionType.objects.get(type=action.atype).full_description
    return Template(description).render(Context({'action':action, 'bill':bill}))
