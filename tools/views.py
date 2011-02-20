from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext

from watchingaz.base.models import Term
from watchingaz.tools.forms import AddTrackerForm, SearchBarForm
from watchingaz.tools.models import Tracker, MyTracker
from watchingaz.bills.models import Bill

import re

def search(request):
    c = {}
    search = request.GET.get('search_field', None)
    options = request.GET.get('search_options', 'b') # make bills default
    if search:
        if options == 'b':
            if re.match(r'([S|H][B|R|C][M|R]?)\s?(\d\d\d\d)', search.upper()):
                query = re.match(r'([S|H][B|R|C][M|R]?)\s?(\d\d\d\d)',
                                  search.upper()).groups()
                query = "%s %s" % (query[0], query[1])
                search_results = Bill.objects.filter(number=query.upper())
            else:
                search_results = Bill.objects.filter(title__icontains=search)
                if not search_results:
                    search_results = Bill.objects.filter(subjects__subject__icontains=search)
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
@login_required
def add_tracker(request):
    c = {}
    initial = {}
    if request.POST:
        if request.user.is_authenticated():
            initial['update_on'] = 'd'
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
