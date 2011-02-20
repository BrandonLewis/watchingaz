from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def index(request):
    c = {}
    return render_to_response('committee_index.html', RequestContext(request, c))

def committee_detail(request, committee_id):
    c = {}
    return render_to_response('committee_detail.html', RequestContext(request, c))