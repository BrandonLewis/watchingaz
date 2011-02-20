from django.db import models

class BaseSource(models.Model):
    url = models.URLField(verify_exists=False)
    retrieved = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True

class Metadata(models.Model):
    name = models.CharField(max_length=12, null=True)
    abbreviation = models.CharField(max_length=2, primary_key=True)
    legislature_name = models.CharField(max_length=120)
    lower_chamber_name = models.CharField(max_length=120)
    upper_chamber_name = models.CharField(max_length=120)
    lower_chamber_title = models.CharField(max_length=20)
    upper_chamber_title = models.CharField(max_length=20)
    lower_chamber_term = models.IntegerField(max_length=1)
    upper_chamber_term = models.IntegerField(max_length=1)
    latest_dump_url = models.URLField(verify_exists=False, blank=True)
    latest_dump_date = models.DateTimeField(blank=True, null=True)

class Term(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_year = models.IntegerField(max_length=4, null=True)
    end_year = models.IntegerField(max_length=4, null=True)
    metadata = models.ForeignKey(Metadata, related_name='terms')
    class Meta:
        get_latest_by = 'name'

class Session(models.Model):
    name = models.CharField(max_length=200, unique=True)
    term = models.ForeignKey(Term, related_name='sessions')
    last_update = models.DateTimeField(blank=True, null=True)

class SessionDetail(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10)
    session = models.OneToOneField(Session, related_name='session_details')
    s_id = models.IntegerField(max_length=3, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    full_name = models.CharField(max_length=200)
    metadata = models.ForeignKey(Metadata, related_name='session_details')
