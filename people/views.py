from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext

from collections import namedtuple
from watchingaz.committees.models import Committee
from watchingaz.people.models import Person

bill_tuple = namedtuple("BillTuple", ['number','title', 'type'])

def person_index(request):
    c = {'term':'50', 'session': '1r'}
    c['people'] = Person.objects.filter(roles__term="50", roles__type="member").order_by('chamber', 'district')
    return render_to_response('person_index.html', RequestContext(request, c))

def person_view(request, id):
    c = {'term':'50', 'session': '1r'}
    c['person'] = Person.objects.get(leg_id=id)
    roles = c['person'].roles.all().order_by('-term', '-type')

    for role in roles:
        if role.committee:
            role.committee = Committee.objects.get(id=role.committee)
    c['roles'] = roles
    # unnecessary but its nice to use words rather than indexes
    c['sponsored_bills'] = []
    sponsored_bills = c['person'].sponsor_set.filter(bill__session__name="50th-1st-regular").values_list("bill__number", "bill__title", "type").order_by('bill__number')
    for bill in sponsored_bills:
        c['sponsored_bills'].append(bill_tuple(*bill))

    return render_to_response('person.html', RequestContext(request, c))
