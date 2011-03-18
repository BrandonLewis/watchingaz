from watchingaz.bills.models import *
from django.contrib import admin

class BillAdmin(admin.ModelAdmin):
    search_fields = ("number", "session__name", "title")

admin.site.register(Bill, BillAdmin)

class BillPageViewAdmin(admin.ModelAdmin):
    search_fields = ("bill__number",)

admin.site.register(BillPageView, BillPageViewAdmin)

class VersionAdmin(admin.ModelAdmin):
    search_fields = ("bill__number", "bill__session__name", "name")

admin.site.register(Version, VersionAdmin)
admin.site.register(VersionText)

class ActionTypeAdmin(admin.ModelAdmin):
    search_fields = ("type",)

admin.site.register(ActionType, ActionTypeAdmin)

class ActionAdmin(admin.ModelAdmin):
    search_fields = ("bill__number", "action")
admin.site.register(BillAction, ActionAdmin)

class SponsorAdmin(admin.ModelAdmin):
    search_fields = ("bill__number", "person__leg_id", "person__full_name", 
                     "person__first_name", "person__last_name")
admin.site.register(Sponsor, SponsorAdmin)
