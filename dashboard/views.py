from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader, Template

from watchingaz.dashboard.models import Profile

def index(request):
    pass

def view_profile(request, user):
    c = {}
    if request.user.is_authenticated():
        pass
    return render_to_response('view_profile.html', RequestContext(request, c))

@login_required
def edit_profile(request, user):
    c ={}
    if request.user.is_authenticated():
        pass
    return reder_to_response('edit_profile.html', RequestContext(request, c))