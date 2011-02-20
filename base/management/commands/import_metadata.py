from django.core.management.base import BaseCommand, make_option
from django.conf import settings
from watchingaz.base.models import Metadata, Term, Session, SessionDetail
import urllib2
import json
from pprint import pprint
from dateutil.parser import parse

BASE_URL = 'http://openstates.sunlightlabs.com/api/v1/metadata/%s/?apikey=%s'

def import_metadata(state, api_key):
    page = urllib2.urlopen(BASE_URL % (state, api_key))
    m = json.load(page)
    pprint(m)
    try:
        metadata = Metadata.objects.get(abbreviation=m['abbreviation'])
    except Metadata.DoesNotExist:
        metadata = Metadata(abbreviation=m['abbreviation'])

    metadata.legislature_name = m['legislature_name']
    metadata.lower_chamber_name = m['lower_chamber_name']
    metadata.upper_chamber_name = m['upper_chamber_name']
    metadata.lower_chamber_title = m['lower_chamber_title']
    metadata.upper_chamber_title = m['upper_chamber_title']
    metadata.lower_chamber_term = m['lower_chamber_term']
    metadata.upper_chamber_term = m['upper_chamber_term']
    metadata.latest_dump_date = m['latest_dump_date']
    metadata.latest_dump_url = m['latest_dump_url']
    metadata.save()
    for t in m['terms']:
        term,tc = Term.objects.get_or_create(metadata=metadata,
                                                      name=t['name'])
        term.start_year = t['start_year']
        term.end_year = t['end_year']
        term.save()
        for s in t['sessions']:
            session,sc = Session.objects.get_or_create(name=s, term=term)
            if sc:
                term.sessions.add(session)
        if sc:
            term.save()
    for d in sorted(m['session_details'].keys()):
        session = Session.objects.get(name=d)
        detail,c = SessionDetail.objects.get_or_create(metadata=metadata,
                                                     name=d,type=m['session_details'][d]['type']
                                                     ,session=session,
                                                     full_name=m['session_details'][d]['verbose_name'])
        detail.s_id = m['session_details'][d].get('session_id', None)
        detail.start_date = m['session_details'][d].get('start_date', None)
        detail.end_date = m['session_details'][d].get('end_date', None)
        detail.save()
        if c:
            metadata.session_details.add(detail)
    metadata.save()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--state', action='store_true', dest='state',
                    default='AZ', help='Two char state abbreviation'),
        make_option('--api-key', action='store_true', dest='api_key',
                    default=settings.SUNLIGHT_API_KEY, help='Sunlight Services Api Key'),
    )

    def handle(self, *args, **options):
        import_metadata(state=options.get('state'),
                        api_key=options.get('api_key'),
                        )