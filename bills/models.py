from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
#from django.dispatch import receiver
from watchingaz.utils import legislature_to_number
from watchingaz.base.models import BaseSource, Session
from watchingaz.people.models import Person
from watchingaz.committees.models import Committee
from watchingaz.lib.models.multifield import MultiSelectField
from watchingaz.lib.forms.extra_widgets import MultiSelectFormField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^watchingaz\.lib\.models\.multifield\.MultiSelectField"])

ACTION_CHOICES = (("bill:introduced", "bill:introduced"),
                  ("bill:passed", "bill:passed"),("bill:failed", "bill:failed"),
                  ("bill:withdrawn", "bill:withdrawn"),
                  ("bill:substituted" ,"bill:substituted"),
                  ("bill:veto_override:passed", "bill:veto_override:passed"),
                  ("bill:veto_override:failed", "bill:veto_override:failed"),
                  ("governor:received","governor:received"),
                  ("governor:signed","governor:signed"),
                  ("governor:vetoed", "governor:vetoed"),
                  ("governor:vetoed:line-item","governor:vetoed:line-item"),
                  ("amendment:introduced","amendment:introduced"),
                  ("amendment:passed","amendment:passed"),
                  ("amendment:failed","amendment:failed"),
                  ("amendment:tabled","amendment:tabled"),
                  ("amendment:amended","amendment:amended"),
                  ("amendment:withdrawn","amendment:withdrawn"),
                  ("committee:referred","committee:referred"),
                  ("committee:failed","committee:failed"),
                  ("committee:passed","committee:passed"),
                  ("committee:passed:favorable","committee:passed:favorable"),
                  ("committee:passed:unfavorable","committee:passed:unfavorable"),
                  ("bill:reading:1","bill:reading:1"),("bill:reading:2","bill:reading:2"),
                  ("bill:reading:3","bill:reading:3"),("other","other"))

class ActionType(models.Model):
    type = MultiSelectField(max_length=200, choices=ACTION_CHOICES)
    full_description =models.TextField(blank=True)
    def __unicode__(self):
        return u",".join(self.type)

class BillAction(models.Model):
    bill = models.ForeignKey('Bill', related_name="actions")
    actor = models.TextField()
    date = models.DateTimeField()
    action = models.CharField(max_length=255)
    type = models.ManyToManyField(ActionType)
    class Meta:
        get_latest_by = 'date'
    def __unicode__(self):
        return "%s %s %s" % (self.bill.number, self.action, self.type.get())

class Bill(models.Model):
    number = models.CharField(max_length=10)
    session = models.ForeignKey(Session, related_name="bills")
    chamber = models.CharField(max_length=10)
    title = models.CharField(max_length=255, null=True, blank=True)
    subjects = models.ManyToManyField('BillSubject', null=True, blank=True)
    sponsors = models.ManyToManyField(Person, through='Sponsor')
    type = models.CharField(max_length=30, blank=True)
    final_disposition = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    page_views_count = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s %s" % (self.number, self.title)
    def get_absolute_url(self):
        return "/bills/%s/%s" % ( legislature_to_number(self.session.name),
                                  self.number)
    def get_bill_stats(self, date=None):
        """Gets the basic page views and if possible corresponding actions
        to use for building a bill stats chart.
        Currently returns a list or None if no page_view objects have been found
        returns [{'date': '5/1/10', 'views': 20, 'action':'action.action'}]"""
        #if not date:
        #    date = datetime.date.today()
        # bill.get_actions()
        actions = self.actions.all()
        sactions = []
        page_views = self.page_views.all()
        if not page_views:
            return None
        for day in page_views:
            sactions.append({'date': day.date,
                             'views':day.views})
        for action in actions:
            for date in sactions:
                if action.date == date['date']:
                    date['action'] = action.action
        for date in sactions:
            if 'action' not in date:
                date['action'] = ''
            date['date'] = date['date'].strftime('%m/%d/%Y')
        return sactions
    def get_user_support(self):
        """Returns a list of two dicts for the user support chart
        bill.get_user_support()--> [
                                        {"position": "'for'",
                                         "count": 9, },
                                        {"position":"'against'",
                                         "count":10000}
                                      ]
        """

        votes = self.user_votes.all()
        for_bill = 0
        against_bill = 0
        for vote in votes:
            if vote == False:
                against_bill += 1
            elif vote == True:
                for_bill += 1
        return [{"position": "'for'", "count": for_bill, },{"position":"'against'", "count":against_bill}]
    def update_user_votes(self):
        votes = self.user_votes.all(bill=self)
        for_bill = 0
        against_bill = 0
        for vote in votes:
            if vote == False:
                against_bill += 1
            elif vote == True:
                for_bill += 1
        return {'for': for_bill, 'against': against_bill, 'percent': float(for_bill) / float(for_bill + against_bill)}

class BillPageView(models.Model):
    bill = models.ForeignKey(Bill, related_name="page_views",
                             unique_for_date="date")
    date = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s: %s: %d" % (self.bill.number, self.date.strftime("%m/%d/%Y"),
                               self.views)

#@receiver(post_save, sender=Bill)
def bill_status_handler(sender, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        status = BillStatus(bill=kwargs['instance'])
        status.save()
post_save(bill_status_handler, sender=Bill)
class BillStatus(models.Model):
    bill = models.OneToOneField(Bill, related_name='status')
    introduced = models.NullBooleanField(null=True, blank=True)
    first_read_date = models.DateTimeField(null=True, blank=True)
    passed_primary = models.NullBooleanField(null=True, blank=True)
    primary_date = models.DateTimeField(null=True, blank=True)
    passed_other = models.NullBooleanField(null=True, blank=True)
    other_date = models.DateTimeField(null=True, blank=True)
    concur = models.NullBooleanField(null=True, blank=True)
    concur_date = models.DateTimeField(null=True, blank=True)
    passed_gov = models.NullBooleanField(null=True, blank=True)
    gov_date = models.NullBooleanField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    def get_status(self):
        """
        Checks to see if this status object is up to date and either calls
        update_status or returns a dict of basic action info:
        {
            'primary' : {'passed': self.passed_primary, 'date': self.primary_date},
            'other'   : {'passed': self.passed_other,   'date': self.other_date},
            'governor': {'passed': self.passed_gov,     'date': self.gov_date}
        }
        """
        if self.updated_on < self.bill.updated_at:
            actions = self.bill.actions.filter(date__gt=self.updated_on)
            if actions:
                return self.update_status()
        # TODO when the new session begins in earnest return a dict of relevent info
        return self.update_status()

    def update_status(self):
        """
        Updates the status object and returns a dict of basic action info for
        use in a template like this:
        {
            'primary' : {'passed': self.passed_primary, 'date': self.primary_date},
            'other'   : {'passed': self.passed_other,   'date': self.other_date},
            'governor': {'passed': self.passed_gov,     'date': self.gov_date}
        }
        """
        q = { True: 'passed', False: 'failed', None: 'no-action'}
        actions = self.bill.actions.all()
        try:
            introduced = actions.get(type__type__icontains='bill:introduced')
        except ObjectDoesNotExist:
            self.introduced = None
            self.save()
            return {'introduced': {'passed': 'no-action'}}
        if introduced:
            self.introduced = True
            self.first_read_date = introduced.date
        third_read = actions.filter(actor=self.bill.chamber,
                                    type__type__icontains="bill:reading:3")
        if third_read:
            action = third_read[0].type.all()[0].type
            for act in action:
                if act == 'bill:passed':
                    self.passed_primary = True
                    self.primary_date = third_read[0].date
                elif act == 'bill:failed':
                    self.passed_primary = False
                    self.primary_date = third_read[0].date
        other_third = actions.filter(actor=self.bill.chamber,
                                     type__type__icontains="bill:reading:3")
        if other_third:
            action = other_third[0].type.all()[0].type
            for act in action:
                if act == 'bill:passed':
                    self.passed_other = True
                    self.other_date = other_third[0].date
                elif act == 'bill:failed':
                    self.passed_other = False
                    self.other_date = third_read[0].date
        gov_act = actions.filter(type__type__icontains="governor:signed")
        if gov_act:
            self.passed_gov = True
            self.gov_date = gov_act[0].date
        gov_act = actions.filter(type__type__icontains="governor:vetoed")
        if gov_act:
            self.passed_gov = False
            self.gov_date = gov_act[0].date
        self.save()
        return {'introduced' : {'passed': q[self.introduced], 'date': self.first_read_date},
                'primary' : {'passed': q[self.passed_primary], 'date': self.primary_date},
                'other'   : {'passed': q[self.passed_other],   'date': self.other_date},
                'governor': {'passed': q[self.passed_gov],     'date': self.gov_date}}


class BillVote(models.Model):
    bill = models.ForeignKey(Bill, related_name="votes")
    chamber = models.CharField(max_length=10, null=True, blank=True)
    committee = models.ForeignKey(Committee, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    motion = models.TextField(null=True, blank=True)
    passed = models.NullBooleanField()
    yes_count = models.IntegerField(max_length=2, default=0)
    yes_votes = models.ManyToManyField(Person, through='YesVote', null=True,
                                       blank=True, related_name='yes_votes')
    no_count = models.IntegerField(max_length=2, default=0)
    no_votes = models.ManyToManyField(Person, through='NoVote', null=True,
                                      blank=True, related_name='no_votes')
    other_count = models.IntegerField(max_length=2, default=0)
    other_votes = models.ManyToManyField(Person, through='OtherVote', null=True,
                                         blank=True, related_name='other_votes')
    exc_count = models.IntegerField(max_length=2, default=0)
    abs_count = models.IntegerField(max_length=2, default=0)
    present_count = models.IntegerField(max_length=2, default=0)
    nv_count = models.IntegerField(max_length=2, default=0)
    type = models.TextField(blank=True, null=True)
    sources = models.TextField(blank=True, null=True)

class BillSubject(models.Model):
    subject = models.CharField(max_length=100)
    occurrence_count = models.IntegerField(default=0)

class BaseDocument(models.Model):
    name = models.TextField()
    url = models.URLField(verify_exists=False)
    retrieved = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True

class BasePersonVote(models.Model):
    vote = models.ForeignKey(BillVote)
    person = models.ForeignKey(Person, unique=False)
    class Meta:
        abstract = True

class BillSource(BaseSource):
    bill = models.ForeignKey(Bill, related_name='sources')

class VoteSource(BaseSource):
    vote = models.ForeignKey(BillVote)

class Document(BaseDocument):
    bill = models.ForeignKey(Bill, related_name='documents')
    text = models.TextField(blank=True)
    doc_type = models.CharField(max_length=30, blank=True)
    doc_id = models.CharField(max_length=60, blank=True)

class Amendment(models.Model):
    bill = models.ForeignKey(Bill, related_name='amendments')
    title = models.TextField()
    adopted = models.BooleanField(default=False)
    url = models.URLField(verify_exists=True)

class Sponsor(models.Model):
    "Bill Sponsor relationships"
    bill = models.ForeignKey(Bill)
    person = models.ForeignKey(Person, null=True, blank=True)
    type = models.CharField(max_length=2)
    scraped_name = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s %s' % (self.person.full_name, self.type)

class Title(models.Model):
    "Alternate Bill Titles"
    bill = models.ForeignKey(Bill, related_name='alternate_titles')
    text = models.TextField()
    primary = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title

class Version(BaseDocument):
    """
    Bill Versions the text is currently stored at:
    http://www.watching.az/data/bill_text/(term)/(session)/(bill_version).html
    so that we can easily refactor them without hitting the db all the time
    """
    title = models.TextField(blank=True)
    bill = models.ForeignKey(Bill, related_name='versions')
    document_id = models.CharField(max_length=60, blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/bills/%s/%s/%s/' % ( self.bill.session.name, self.bill.number,
                                      self.name)

class VersionText(models.Model):
    node_id = models.CharField(max_length=30, primary_key=True)
    version = models.ForeignKey(Version)

class YesVote(BasePersonVote):
    pass
class NoVote(BasePersonVote):
    pass
class OtherVote(BasePersonVote):
    pass
class AbsentVote(BasePersonVote):
    pass
class ExcusedVote(BasePersonVote):
    pass
class NotVote(BasePersonVote):
    pass
class PresentVote(BasePersonVote):
    pass
class VacantVote(BasePersonVote):
    pass
