from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from collections import namedtuple
from watchingaz.committees.models import Committee
from watchingaz.people.models import Person

azNS = settings.BASE_NS
bill_tuple = namedtuple("BillTuple", ['number','title', 'type'])

def person_index(request):
    c = {'term':'50', 'session': '1r', 'azNS':azNS}
    #people = Person.objects.filter(roles__term="50", roles__type="member").order_by('chamber', 'district')
    people = Person.objects.filter(active=True)
    lower_people = []
    upper_people = []
    for person in people:
        if person.chamber == 'lower':
            lower_people.append(person)
        else:
            upper_people.append(person)
    upper_people = sorted(upper_people, key=lambda x: int(x.district))
    lower_people = sorted(lower_people, key=lambda x: int(x.district))
    c['people'] = {'upper': upper_people,
                   'lower': lower_people}
    return render_to_response('person_index.html', RequestContext(request, c))

def person_view(request, id):
    c = {'term':'50', 'session': '1r', 'azNS':azNS}
    c['person'] = Person.objects.get(leg_id=id)
    roles = c['person'].roles.all().order_by('-type') #('-term', '-type')
    membership = {} # they served in the house term 49-50
    committee_roles = []
    
    for role in roles:
        if role.type == 'member':
            if role.term in membership:
                membership[role.term].append(role)
            else:
                membership[role.term] = [role]
        elif role.type == 'committee member':
            committee_roles.append(role)
            
    c['roles'] = roles
    # unnecessary but its nice to use words rather than indexes
    c['sponsored_bills'] = []
    sponsored_bills = c['person'].sponsor_set.filter(bill__session__name="50th-1st-regular").values_list("bill__number", "bill__title", "type").order_by('bill__number')
    for bill in sponsored_bills:
        c['sponsored_bills'].append(bill_tuple(*bill))

    return render_to_response('person.html', RequestContext(request, c))
