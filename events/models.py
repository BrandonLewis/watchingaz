from django.db import models

class Event(models.Model):
    """Events can be anything from committee meetings to bill actions AZ's
    participant field can contain the committee memebers but for now we are
    ignoring them."""
    id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    details = models.TextField(blank=True)
    when = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    type = models.CharField(max_length=30, blank=True)
    participants = models.CharField(max_length=255, blank=True)
    session = models.CharField(max_length=200, blank=True)
    def __unicode__(self):
        return self.title