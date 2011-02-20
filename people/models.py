from django.db import models
from django.contrib.localflavor.us.models import USStateField

class Person(models.Model):
    party_types = (
        ('R', 'Republican'),
        ('D', "Democrat"),
        ('I', 'Independant'),
        ('L', 'Libertarian'),
        ('G', 'Green Party')
    )

    full_name = models.CharField(max_length=120, blank=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    middle_name = models.CharField(max_length=60, blank=True)
    suffixes = models.CharField(max_length=60, blank=True)
    office_address = models.CharField(max_length=255, blank=True)
    office_phone = models.CharField(max_length=12, blank=True)
    office_fax = models.CharField(max_length=12, blank=True)
    email = models.EmailField(blank=True, null=True)
    url = models.URLField(verify_exists=False, blank=True, null=True)
    active = models.BooleanField(default=False)
    chamber = models.CharField(max_length=5, blank=True)
    district = models.CharField(max_length=3, blank=True)
    state = USStateField(default='AZ')
    party = models.CharField(max_length=1, choices=party_types, blank=True)
    photo_url = models.URLField(verify_exists=True, blank=True)
    leg_id = models.CharField(max_length=9, unique=True)
    nimsp_candidate_id = models.CharField(max_length=10, blank=True)
    votesmart_id = models.CharField(max_length=10, blank=True, null=True)
    transparencydata_id = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    page_views_count = models.IntegerField(default=0)

class Role(models.Model):
    party_types = (
        ('R', 'Republican'),
        ('D', "Democrat"),
        ('I', 'Independant'),
        ('L', 'Libertarian'),
        ('G', 'Green Party')
    )
    person= models.ForeignKey(Person, related_name='roles')
    chamber = models.CharField(max_length=5, null=True, blank=True)
    state = USStateField(default='AZ')
    term = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    committee = models.CharField(max_length=255, blank=True, null=True)
    subcommittee = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=10, blank=True, null=True)
    party = models.CharField(max_length=1, choices=party_types, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)