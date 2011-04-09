from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from watchingaz.dashboard.models import Profile
from watchingaz.bills.models import Bill
from watchingaz.base.models import Term
from watchingaz.people.models import Person


class Trackable(models.Model):
    "if a model/contenttype is in this table users can track changes to it"
    content_type = models.ForeignKey(ContentType, unique=True)
    def __unicode__(self):
        return self.content_type.__unicode__()
    
class Tracker(models.Model):
    """Tracker represents any object/content type """
    content_type = models.ForeignKey(ContentType)
    tracked_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'tracked_id')
    term = models.ForeignKey(Term)
    last_updated = models.DateField(blank=True, null=True)

    def save(self, *args, **kargs):
        if not Trackable.objects.get(content_type=self.content_type):
            raise ValidationError("This item is not trackable")
        super(Tracker, self).save(*args, **kargs)

class MyTracker(models.Model):
    # the reason for the update frequency being assigned per tracked item
    # is that someone might want to track one bill that is a hot item and be
    # notified daily while for other bills its not an urgent need
    update_choices = (('d', 'Daily'), ('w', 'Weekly', ), ('m', 'Monthly'))
    user = models.ForeignKey(Profile, related_name='tracked_items', null=True,
                             blank=True)
    tracker = models.ForeignKey(Tracker, related_name='users_tracking')
    frequency = models.CharField(max_length=1, choices=update_choices)

class UserVote(models.Model):
    bill = models.ForeignKey(Bill, related_name='user_votes')
    user = models.ForeignKey(Profile, related_name='users_votes')
    vote = models.NullBooleanField(null=True, blank=True)
    def set_vote(self, vote):
        self.vote = vote
        self.save()
        result = self.bill.update_user_votes()
        return result

class Question(models.Model):
    user = models.ForeignKey(Profile, related_name="my_questions")
    ip = models.IPAddressField()
    email = models.EmailField()
    subject = models.CharField(max_length=140)
    text = models.TextField()
    
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers")
    user = models.ForeignKey(Profile, related_name="my_answers")
    text = models.TextField()
    
#class TransparencyDataModel(models.Model):
#    "this model will likely be split into several smaller models"
#    cycle = models.IntegerField(max_length=5)
#    transaction_namespace = models.CharField(max_length=22)
#    transaction_id = models.CharField(max_length=32)
#    transaction_type = models.CharField(max_length=16)
#    filing_id = models.CharField(max_length=9)
#    is_amendment = models.CharField(max_length=12)
#    amount = models.CharField(max_length=11)
#    date = models.CharField(max_length=10)
#    
#    contributor_name = models.CharField(max_length=255)
#    contributor_ext_id = models.CharField(max_length=18)
#    contributor_type = models.CharField(max_length=16)
#    contributor_occupation = models.CharField(max_length=64)
#    contributor_employer = models.CharField(max_length=64)
#    contributor_gender = models.CharField(max_length=18)
#    contributor_address = models.CharField(max_length=84)
#    contributor_city = models.CharField(max_length=38)
#    contributor_state = models.CharField(max_length=17)
#    contributor_zipcode = models.CharField(max_length=19)
#    contributor_category = models.CharField(max_length=20)
#    
#    organization_name = models.CharField(max_length=255)
#    organization_ext_id = models.CharField(max_length=19)
#    parent_organization_name = models.CharField(max_length=255)
#    parent_organization_ext_id = models.CharField(max_length=26)
#    
#    recipient_name = models.CharField(max_length=96)
#    recipient_ext_id = models.CharField(max_length=16)
#    recipient_party = models.CharField(max_length=15)
#    recipient_type = models.CharField(max_length=14)
#    recipient_state = models.CharField(max_length=15)
#    recipient_state_held = models.CharField(max_length=20)
#    recipient_category = models.CharField(max_length=18)
#    
#    committee_name = models.CharField(max_length=255)
#    committee_ext_id = models.CharField(max_length=16)
#    committee_party = models.CharField(max_length=15)
#    candidacy_status = models.CharField(max_length=16)
#    district= models.CharField(max_length=8)
#    district_held = models.CharField(max_length=13)
#    seat = models.CharField(max_length=14)
#    seat_held = models.CharField(max_length=9)
#    seat_status = models.CharField(max_length=11)
#    seat_result = models.CharField(max_length=11)