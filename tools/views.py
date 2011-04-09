from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader, Template

from watchingaz.base.models import Term
from watchingaz.tools.forms import AddTrackerForm, SearchBarForm
from watchingaz.tools.models import Tracker, MyTracker, UserVote
from watchingaz.bills.models import Bill

import re
def developers_index(request):
    c = {}
    return render_to_response('developers.html', RequestContext(request, c))
def search(request):
    c = {}
    search = request.GET.get('search_field', None)
    options = request.GET.get('search_options', 'b') # make bills default
    session = request.GET.get('session', '50th-1st-regular')
    if search:
        if options == 'b':
            if re.match(r'([S|H][B|R|C][M|R]?)\s?(\d\d\d\d)', search.upper()):
                query = re.match(r'([S|H][B|R|C][M|R]?)\s?(\d\d\d\d)',
                                  search.upper()).groups()
                query = "%s %s" % (query[0], query[1])
                search_results = Bill.objects.filter(number=query.upper(),
                                                     session__name=session)
            else:
                search_results = Bill.objects.filter(title__icontains=search,
                                                     session__name=session)
                if not search_results:
                    search_results = Bill.objects.filter(subjects__subject__icontains=search,
                                                         session__name=session)
            c['search_results'] = search_results[:10]
        elif options == 'l':
            pass
        else:
            c['search_results'] = ['Please Enter a Bill number, title, subject or something!']
        c['search_form'] = SearchBarForm({'search_field':search})
    else:
        c['search_form'] = SearchBarForm()
    if request.is_ajax():
        return render_to_response('_search.json', RequestContext(request, c))
    return render_to_response('search.html', RequestContext(request, c))

@login_required
def get_comment_form(request, content_type, commentable_id):
    c = {}
    commentable_type = ContentType.objects.get(app_label="bills", model=content_type)
    c['commentable'] = commentable_type.get_object_for_this_type(node_id=commentable_id)
    if request.is_ajax():
        return render_to_response('_comment.html', RequestContext(request, c))
#@login_required
def add_tracker(request):
    c = {}
    initial = {}
    if request.POST:
        if request.user.is_authenticated():
            initial['update_on'] = 'w'
            profile = request.user.get_profile()
        elif 'first_try' in request.POST:
            initial['email'] = request.POST('email', None)

        initial['object_id'] = request.POST.get('object_id', None)
        initial['where_to'] = request.POST.get('where_to', None)
        initial['content_type'] = request.POST.get('content_type', None)
        track_form = AddTrackerForm(initial)
        if track_form.is_valid():
            ct = ContentType.objects.get(
                                    id=track_form.cleaned_data['content_type']
                                    )
            content_object = ContentType.objects.get(
                                    id=track_form.cleaned_data['content_type']
                                    ).get_object_for_this_type(
                                        id=track_form.cleaned_data['object_id'])

            tracker,c = Tracker.objects.get_or_create(term=Term.objects.latest(),
                                                    content_type=ct,
                                                    tracked_id=track_form.cleaned_data['object_id']
                                                    )
            user_tracker = MyTracker()
            user_tracker.user = profile
            user_tracker.tracker = tracker
            user_tracker.frequency = track_form.cleaned_data['update_on']
            user_tracker.save()
#            if 'email' in track_form.cleaned_data and track_form.cleaned_data['email']:
#                tracker.email = track_form.cleaned_data['email']
#            else:
#                tracker.user = profile

            if 'trackers' in request.COOKIES:
                request.COOKIES['trackers']
            if request.is_ajax():
                return render_to_response('base/_tracker_added.html', {})
            return HttpResponseRedirect(track_form.cleaned_data['where_to'])
        else:
            c['track_form'] = track_form
        if request.is_ajax():
            return render_to_response('_add_tracker.html', RequestContext(request, c))
        return render_to_response('add_tracker.html', RequestContext(request, c))
    else:
        raise Http404("Sorry but this page does not exist ;)")

def ontology(request):
    response = HttpResponse(mimetype='application/xml-rdf')
    t = loader.get_template('ontology.owl')
    response.write(t.render(Context({})))
    return response

def bill_rdf(request, session, bill_number):
    subject = Bill.objects.get(number=bill_number, session__name=session)
    if not subject.type:
        raise Http404("Resource %s/%s not found." % (ns, subject_id))
        
    response = HttpResponse(mimetype='application/xml-rdf')
    
    t = loader.get_template('subject_view.rdf')
    c = Context({
        'subject': subject,
    })
    response.write(t.render(c))
    return response

def subject_view(request, subject_class, subject_id):
    classes = {'Person': 'people', 'Committee': 'committees'}
    if not subject_class in classes:
        raise Http404("404 not found")
    content_type = ContentTypes.objects.get(app_label=classes[subject_class],
                                            model=subject_class)
    try:
        subject = content_type.get_object_for_this_type(subject_id)
    except ObjectDoesNotExist:
        raise Http404("404 not found")
    response = HttpResponse(mimetype='application/xml-rdf')
    
    t = loader.get_template('subject_view.rdf')
    c = Context({
        'subject': subject,
    })
    response.write(t.render(c))
    return response

@login_required
def vote(request, position):
    c = {}
    if request.POST:
        try:
            obj_id = int(request.POST['vote_on'])
            bill = Bill.objects.get(id=obj_id)
        except ValueError, Bill.DoesNotExist:
            raise Http404("Bill %s not found." %request.POST['vote_on'])
        vote, c = UserVote.objects.get_or_create(bill=bill, user=request.user.get_profile())
        print position
        vote.vote = {'for':True, 'against':False}[position]
        print vote.vote
        vote.save()
        messages.info(request, "Your vote %s for %s has been recorded." % (
                                                            position, bill.number))
    else:
        raise Http404()
    if request.is_ajax():
        return HttpResponse(content=json.dumps(bill.get_user_support()), mimetype="application/json")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])