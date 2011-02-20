from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from watchingaz.base.models import Session
from watchingaz.bills.models import Bill
from watchingaz.events.models import Event
import datetime, re

def index(request):
    session = Session.objects.get(name=settings.DEFAULT_SESSION)
    c = {}
    c['title'] = "Watching AZ - Home Page"
    c['bills_list'] = Bill.objects.filter(session=session
                                          ).order_by('-actions__date')[:10]
    c['today_events'] = Event.objects.filter(when__startswith=datetime.date.today())
    start = datetime.datetime.today()
    end = start + datetime.timedelta(days=7)
    c['week_events'] = Event.objects.filter(when__range=(start, end))
    c['bill_events'] = c['week_events'].filter(details__iregex=r'[s|h][b|c|r|j][r|m]?\d{4}')
    return render_to_response('index.html', RequestContext(request, c))
