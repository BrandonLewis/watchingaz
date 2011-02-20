from django.db import models
from watchingaz.base.models import BaseSource
from watchingaz.people.models import Person

class Committee(models.Model):
    name = models.TextField()
    short_name = models.CharField(max_length=20, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    state = models.CharField(max_length=2)
    chamber = models.CharField(max_length=5)
    type = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(Person, through="CommitteeMembers")
    leg_id = models.CharField(max_length=30)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    page_views_count = models.IntegerField(default=0)

class CommitteeSource(BaseSource):
    committee = models.ForeignKey(Committee, related_name='source')

class CommitteeMembers(models.Model):
    committee = models.ForeignKey(Committee)
    member = models.ForeignKey(Person)
    role = models.CharField(max_length=100)