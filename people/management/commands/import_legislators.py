from django.core.management.base import BaseCommand, CommandError, make_option
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from watchingaz.people.models import Person, Role
from watchingaz.committees.models import Committee
import os
import glob
import re
import urllib2
import json
import logging
import datetime
from dateutil.parser import parse

CHAMBER = {'upper': 'S', 'lower': 'H'}
PEOPLE_INDEX = 'http://anvilrock-test/api/v1/legislators/?term=%s&apikey=%s'
PERSON_URL = 'http://anvilrock-test/api/v1/legislators/%s/'
{'+session': 'session', '+az_committee_id': 'az_committee_id'}

def process_obj(obj, **kwargs):
    remove = {}
    convert = {}
    change = {'id': 'leg_id'}
    if 'change' in kwargs:
        change.update(kwargs.get('change'))
    if 'remove' in kwargs:
        remove.update(kwargs.get('change'))
    if 'convert' in kwargs:
        convert.update(kwargs.get('convert'))

    parties = {
        'Republican': 'R',
        'Democratic': 'D',
        'Democrat': 'D',
        'Independant': 'I',
        'Libertarian': 'L',
        'Green Party': 'G'
    }
    chamber_list = {
        'upper': 'S',
        'lower': 'H'
    }
    converted = {}
    for key in obj:
        if key.startswith('+'):
            converted[str(key[1:])] = obj[key]
        elif key in change:
            converted[str(change[key])] = obj[key]
        elif key == 'party':
            converted[str('party')] = parties[obj[key]]
        elif key == 'created_at' or key == 'updated_at':
            converted[str(key)] = parse(obj[key]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            converted[str(key)] = obj[key]
    if convert:
        for x in convert:
            if x in converted:
                #print convert[x](converted[x])
                pass
    return converted
    
def import_person(person):
    """takes a json object and updates the legislator"""
    # convert
    change = {'role': 'type'}
    convert = {'end_date': lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x else x,
               'start_date': lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x else x}
    query = {}
    names = person['full_name'].split()
    query['first_name'] = names[0]
    query['last_name'] = names[-1]
    query['leg_id'] = person.pop('leg_id')
    new_person, created = Person.objects.get_or_create(**query)
    
    new_person.full_name = person['full_name']
    new_person.middle_name = person['middle_name']
    new_person.suffixes = person.get('suffixes', '')
    new_person.office_phone = person.get('office_phone', None) or person.get('+phone', '')
    new_person.office_address = person.get('office_address', None) or person.get('+address', '')
    new_person.email = person.get('email', None) or person.get('+email', '')
    new_person.photo_url = person.get('photo_url', '')
    new_person.transparencydata_id = person.get('transparencydata_id', '')
    new_person.votesmart_id = person.get('votesmart_id', '')
    for term in person['old_roles']:
        for role in person['old_roles'][term]:
            converted = process_obj(role, change=change, convert=convert)
            if 'committee_id' in role:
                del(role['subcommittee'])
                committee = Committee.objects.get(leg_id=converted.pop('committee_id'))
                converted['committee'] = committee
            # keep changes in date from creating a new role
            start_date = converted.pop('start_date', None)
            end_date = converted.pop('end_date', None)
            p_role, created = Role.objects.get_or_create(person=new_person, **converted)
            p_role.start_date = start_date
            p_role.end_date = end_date
            p_role.save()

    for role in person['roles']:
        converted = process_obj(role, change=change, convert=convert)
        if 'committee_id' in role:
            del(role['subcommittee'])
            committee = Committee.objects.get(leg_id=converted.pop('committee_id'))
            converted['committee'] = committee
        # keep changes in date from creating a new role
        start_date = converted.pop('start_date', None)
        end_date = converted.pop('end_date', None)
        print converted
        p_role, created = Role.objects.get_or_create(person=new_person, **converted)
        p_role.start_date = start_date
        p_role.end_date = end_date
        p_role.save()
    if person['active'] == True:
        new_person.active = True
        new_person.district = person['roles'][0]['district']
        new_person.chamber = person['roles'][0]['chamber']
    else:
        new_person.active = False
    new_person.save()
        
def import_legislators(state, term, initial=True):

    if initial:
        data_dir = os.path.join(settings.DATA_DIR, state, 'legislators')
        paths = glob.glob(os.path.join(data_dir, '*'))
        for data in paths:
            person = open(data, 'rb')
            import_person(json.load(person))
            person.close()

    else:
        leg_ids = Person.objects.filter(term=term).values_list('leg_id')
        for leg_id in leg_ids:
            page = urllib2.urlopen(PERSON_URL % leg_id)
            person = json.load(page)
            import_person(person)
            page.close()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--state', action='store_true', dest='state',
                    default='az', help='Two char state abbreviation'),
        make_option('--term', action='store_true', dest='term',
                    default='50',
                    help='import bills from the openstates project'),
        make_option('--data_dir', action='store_true', dest='data_dir',
                    default=settings.DATA_DIR,
                    help='location of the data dump directory'),
        make_option('--initial', action='store_true', dest='initial',
                    default=True,
                    help='True if you are initializing the state or if you are' +
                         'updating from a data dump'),
    )

    def handle(self, *args, **options):
        import_legislators(state=options.get('state'),
                     term=options.get('term'),
                     initial=options.get('initial')
                     )
