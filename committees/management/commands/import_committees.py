from django.core.management.base import BaseCommand, CommandError, make_option
from django.conf import settings
from watchingaz.committees.models import Committee, CommitteeSource
import os
import glob
import urllib2
import json
from dateutil.parser import parse

COMMITTEE_INDEX = 'http://anvilrock-test/api/v1/committees/'
COMMITTEE_URL = 'http://anvilrock-test/api/v1/committees/%s/'
{'+session': 'session', '+az_committee_id': 'az_committee_id'}

def process_obj(obj, **kwargs):
    remove = set()
    convert = {}
    change = {'id': 'leg_id'}
    if 'change' in kwargs:
        change.update(kwargs.get('change'))
    if 'remove' in kwargs:
        remove.update(kwargs['remove'])
        for x in remove:
            del(obj[x])
    if 'convert' in kwargs:
        convert.update(kwargs.get('convert'))

    parties = {
        'Republican': 'R',
        'Democratic': 'D',
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
        elif key == 'updated_at' or key == 'created_at':
            converted[str(key)] = parse(obj[key]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            converted[str(key)] = obj[key]
    if convert:
        for x in convert:
            print convert[x](converted[x])
    return converted

#def import_committee(com, parent_id=None):
#    """Takes a json object and creates or updates a committee"""
#    if com['parent_id']:
#        #we cannot create a committee if its parent doesnt exist
#        try:
#            parent = Committee.objects.get(leg_id=com['parent_id'])
#        except Committee.ObjectDoesNotExist:
#
#            #lets get the data for the parent committee
def import_committee(committee):
    change = {'+short_name': 'short_name'}
    remove = ('members', '+session', '+az_committee_id')
    committee = process_obj(committee, change=change, remove=remove)

    parent_id = committee.pop('parent_id', None)
    if parent_id and parent_id != committee['leg_id']:
        try:
            parent = Committee.objects.get(leg_id=parent_id)
        except Committee.DoesNotExist:
            page = urllib2.urlopen(COMMITTEE_URL % parent_id)
            parent_committee = json.load(page)
            page.close()
            committee['parent'] = import_committee(parent_committee)
            committee['committee'] = committee.pop('subcommittee')
    committee.pop('subcommittee', None)
    committee['name'] = committee.pop('committee')
    sources = committee.pop('sources')
    new_com,c = Committee.objects.get_or_create(**committee)

    new_com.name = committee['name']
    new_com.state = committee['state']
    new_com.chamber = committee['chamber']
    new_com.created_at = committee['created_at']
    new_com.updated_at = committee['updated_at']
    for source in sources:
        source = process_obj(source)
        new_source, sc = CommitteeSource.objects.get_or_create(committee=new_com,
                                                               **source)
        if sc:
            new_source.save()
    new_com.save()
    if parent_id:
        return new_com
    print "saved committee: %s" % new_com.leg_id

def import_committees(state, term, force_update, initial=True):
    if initial:
        data_dir = os.path.join(settings.DATA_DIR, state.lower(), 'committees')
        paths = sorted(glob.glob(os.path.join(data_dir, '*')))
        count = 0
        subcommittees = []
        for data in sorted(paths):
            page = open(data, 'rb')
            committee = json.load(page)
            page.close()
            import_committee(committee)
    else:
        pass


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--state', action='store_true', dest='state',
                    default='AZ', help='Two char state abbreviation'),
        make_option('--term', action='store_true', dest='term',
                    default='50',
                    help='import bills from the openstates project'),
    )

    def handle(self, *args, **options):
        import_committees(state=options.get('state'),
                     term=options.get('term'),
                     force_update=options.get('force_update')
                     )