from watchingaz.people.models import *
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "first_name", "last_name", "leg_id", "chamber")
    
admin.site.register(Person, PersonAdmin)
