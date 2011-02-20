from django.contrib import admin
from watchingaz.tools.models import Trackable, Tracker

class TrackableAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trackable, TrackableAdmin)

class TrackerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tracker, TrackerAdmin)