from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.contrib.auth.models import User

#@receiver(post_save, sender=User)
def profile_handler(sender, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        if User.objects.count() == 1:
            return
        profile = Profile(user=kwargs['instance'])
        profile.save()
post_save.connect(profile_handler, sender=User)
class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    options = models.ManyToManyField('Option')
    def __unicode__(self):
        return self.user.username + " profile"
    def is_tracking(self, object_id):
        try:
            return self.tracked_items.filter(tracker__tracked_id=object_id).exists()
        except ObjectDoesNotExist:
            return False

class Option(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=20, blank=True)


class BetaFeatures(models.Model):
    pass
