from django.core.management.base import BaseCommand, CommandError, make_option
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from watchingaz.base.models import Session
from watchingaz.bills.models import *
from watchingaz.people.models import Person
from watchingaz.tools.models import Tracker
import os
import glob
import urllib
import json
import time
import datetime
from dateutil.parser import parse
from scrapelib import Scraper

CHAMBER = {'upper': 'S', 'lower': 'H'}
BILL_INDEX = 'http://openstates.sunlightlabs.com/api/v1/bills/'
BILL_URL = 'az/%s/%s/'

def get_person_for_vote(person, **kargs):
    if 'vote' in kargs:
        vote = kargs['vote']

    if 'leg_id' in person and person['leg_id']:
        search = Person.objects.get(leg_id=person['leg_id'])
        return search
    name = person['name'].split()
    last_name = name[-1]
    first_name = name[0]
    try:
        search = Person.objects.get(last_name__icontains=last_name,
                                    first_name__icontains=first_name)
    except Person.MultipleObjectsReturned:
        search = Person.objects.filter(last_name__icontains=last_name,
                                       first_name__icontains=first_name)[0]
    return search

def process_vote(vote, bill):
    v, c = BillVote.objects.get_or_create(bill=bill,
                                          date=parse(vote['date']).strftime(
                                                  '%Y-%m-%d %H:%M:%S'),
                                          chamber=vote['chamber'],
                                          motion=vote['motion'])
    if c:
        v.passed = vote['passed']
        v.yes_count = vote['yes_count']
        v.no_count = vote['no_count']
        if int(vote['other_count']) == len(vote['other_votes']):
            v.other_count = vote['other_count']
        else:
            v.other_count = len(vote['other_votes'])
        if '+excused' in vote:
            v.exc_count = vote['+excused']
        if '+absent' in vote:
            v.abs_count = vote['+absent']
        if '+present' in vote:
            v.present_count = vote['+present']
        if '+not_voting' in vote:
            v.nv_count = vote['+not_voting']

        if 'committee' in vote and vote['committee']:
            if (int(v.yes_count) + int(v.no_count) + int(v.other_count)) > 10:
                v.save()
                return
        for rep in vote['yes_votes']:
            person = get_person_for_vote(rep, vote=vote)
            if person:
                how_voted, c = YesVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()

        for rep in vote['no_votes']:
            person = get_person_for_vote(rep, vote=vote)
            if person:
                how_voted, c = NoVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()

        for rep in vote['other_votes']:
            person = get_person_for_vote(rep, vote=vote)
            if person:
                how_voted, c = OtherVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()

        if '+nv' in vote:
            for rep in vote['+nv']:
                person = get_person_for_vote(rep, vote=vote)
                how_voted, c = NotVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()

        if '+ab' in vote:
            for rep in vote['+ab']:
                person = get_person_for_vote(rep, vote=vote)
                how_voted, c = AbsentVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()

        if '+ex' in vote:
            for rep in vote['+ex']:
                person = get_person_for_vote(rep, vote=vote)
                how_voted, c = AbsentVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()
        if '+p' in vote:
            for rep in vote['+p']:
                person = get_person_for_vote(rep, vote=vote)
                how_voted, c = PresentVote.objects.get_or_create(vote=v, person=person)
                how_voted.save()
        v.save()
    return c

def sleep_and_resource(func, *args, **kwargs):
    time = datetime.time.time()
    func(*args, **kwargs)

def process_bill(b):
    """
    takes a json bill object and adds it to the databases
    """
    updated = False
    session = Session.objects.get(name=b['session'])
    bill, created = Bill.objects.get_or_create(number=b['bill_id'],
                                               title=b['title'],
                                               session=session,
                                               type=b['type'])
    bill.created_at = parse(b['created_at']).strftime('%Y-%m-%d %H:%M:%S')
    bill.updated_at = parse(b['updated_at']).strftime('%Y-%m-%d %H:%M:%S')
    bill.chamber = b['chamber']
    bill.state = b['state']
    if '+final_disposition' in b:
        bill.final_disposition = b['+final_disposition']
    for title in b['alternate_titles']:
        t, c = Title.objects.get_or_create(text=title, bill=bill)
        if c:
            updated = True
            t.save()
    for source in b['sources']:
        t,c = BillSource.objects.get_or_create(bill=bill, url=source['url'])
        if c:
            updated = True
            t.retrieved=source['retrieved']
            t.save()
    for version in b['versions']:
        v, c = Version.objects.get_or_create(name=version['name'],
                                             url=version['url'],
                                             bill=bill)
        if 'document_id' in version:
            if v.doc_id != version['document_id']:
                v.retrieved = version.get('retrieved', None)
                v.doc_id = version.get('document_id', None)
                v.save()
        elif c:
            updated = True
            v.save()

    for document in b['documents']:
        d, c = Document.objects.get_or_create(
                name=document['name'],
                url=document['url'],
                doc_type=document.get('+type', ''),
                bill=bill)
        if 'document_id' in document:
            if document['document_id'] != d.doc_id:
                d.retrieved = document.get('retrieved', None)
                d.doc_id = document.get('document_id', '')
                d.save()
        elif c:
            updated = True
            d.save()
    action_count = 0
    for action in b['actions']:
        a, c = BillAction.objects.get_or_create(
                action=action['action'],
                actor=action['actor'],
                date=parse(action['date']).strftime('%Y-%m-%d %H:%M:%S'),
                bill=bill, atype=action['type'])
        # removed the ManyToMany relation on billaction but still will use this 
        # for common action descriptions
        if c:
            updated = True
            a.order = action_count
            a.save()
        else:
            if a.order != action_count:
                a.order = action_count
                a.save()
        action_count += 1
        action_type, c = ActionType.objects.get_or_create(type=action['type'])

    for vote in b['votes']:
        c = process_vote(vote, bill)
        if c:
            updated = True
    for s in b['sponsors']:
        if s['leg_id']:
            person = Person.objects.get(leg_id=s['leg_id'])
            try:
                sponsor, c = Sponsor.objects.get_or_create(person=person,
                                                         bill=bill,
                                                         type=s['type'],
                                                         scraped_name=s['name'])
                if c:
                    updated = True
            except Sponsor.MultipleObjectsReturned:
                # TODO log this and notify me so i can manually update it
                print person, bill, bill.session
        else:
            person = None
            try:
                sponsor, c = Sponsor.objects.get_or_create(bill=bill,
                                                         type=s['type'],
                                                         scraped_name=s['name'])
                if c:
                    updated = True
            except Sponsor.MultipleObjectsReturned:
                print person, bill, bill.session
    bill.save()
    #TODO if created: update new bills tracker
    if updated:
        print "bill updated"
        try:
            tracker = Tracker.objects.get(content_type__name='bill',
                                          tracked_id=bill.id)
            tracker.updated = datetime.datetime.now()
            tracker.save()
        except ObjectDoesNotExist:
            pass
    print "Saved Bill: " + b['bill_id']

def import_bills(state, last_updated, cache_dir, data_dir):
    if last_updated:
        scraper = Scraper(cache_dir=cache_dir)
        url = BILL_INDEX + "?%s"
        query = {'state': state, 'updated_since': last_updated, # YYYY-MM-DD
                 'apikey': settings.SUNLIGHT_API_KEY}
        query = urllib.urlencode(query)
        url = url % query
        with scraper.urlopen(url) as bill_index:
            bills = json.loads(bill_index)
            for b in bills:
                url = BILL_INDEX + "%s/%s/%s/?apikey=%s" % (b['state'], b['session'],
                                                  urllib.quote(b['bill_id']), settings.SUNLIGHT_API_KEY)
                with scraper.urlopen(url) as bill_page:
                    bill = json.loads(bill_page)
                    process_bill(bill)
    else:
        pattern = os.path.join(data_dir, state, 'bills', state)
        sessions = Session.objects.values_list('name')
        _request_frequency = 1
        _last_request = 0
        for session in sessions:
            for chamber in ('upper', 'lower'):
                paths = glob.glob(os.path.join(pattern, session[0], chamber, '*'))
                for path in sorted(paths):
                    now = time.time()
                    diff = _request_frequency - (now - _last_request)
                    if diff > 0:
                        print "sleeping for %fs" % diff
                        time.sleep(diff)
                        _last_request = time.time()
                    else:
                        _last_request = now
                    page = open(path, 'rb')
                    bill = json.load(page)
                    page.close()
                    process_bill(bill)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    make_option('--state', action='store', dest='state',
                default='az', help='Two char state abbreviation'),
    make_option('--last_updated', action='store', dest='last_updated',
                default=None,
                help='import bills from the openstates project'),
    make_option('--cache_dir', action='store', dest='cache_dir',
                default=settings.CACHE_DIR,
                help='path to directory containing the data dump'),
    make_option('--data_dir', action='store', dest='data_dir',
                default=settings.DATA_DIR,
                help='path to directory containing the data dump'),
    )

    def handle(self, *args, **options):
        import_bills(state=options.get('state'),
                     last_updated=options.get('last_updated'),
                     cache_dir=options.get('cache_dir'),
                     data_dir=options.get('data_dir')
                     )