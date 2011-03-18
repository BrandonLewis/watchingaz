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
    

# TODO probably use signals to ensure that trackers are marked as updated
class Tracker(models.Model):
    """Tracker represents any object/content type """
    content_type = models.ForeignKey(ContentType)
    tracked_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'tracked_id')
    term = models.ForeignKey(Term)

    def save(self, *args, **kargs):
        if not Trackable.objects.get(content_type=self.content_type):
            raise ValidationError("This item is not trackable")
        super(Tracker, self).save(*args, **kargs)

class MyTracker(models.Model):
    update_choices = (('d', 'Daily'), ('w', 'Weekly', ), ('m', 'Monthly'),
                      ('o', 'on_action'))
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
    
class AggregateContributions(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=32)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=200) #will need to change this to a company
    organization_id = models.CharField(max_length=32)
    direct_amount = models.DecimalField(max_digits=15, decimal_places=2)
    direct_count = models.IntegerField(max_length=6)
    employee_amount = models.DecimalField(max_digits=15, decimal_places=2)
    employee_count = models.IntegerField(max_length=6)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_count = models.IntegerField(max_length=6)
    
class DataTopSectors(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=32)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    sector = models.CharField(max_length=1)
    
class TopIndustryBySector(models.Model):
    count = models.IntegerField(max_length=5)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    industry = models.CharField(max_length=3)
