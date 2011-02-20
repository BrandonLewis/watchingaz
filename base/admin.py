from watchingaz.base.models import Metadata, Term, Session, SessionDetail
from django.contrib import admin

class MetadataAdmin(admin.ModelAdmin):
    pass

admin.site.register(Metadata, MetadataAdmin)

class TermAdmin(admin.ModelAdmin):
    pass

admin.site.register(Term, TermAdmin)

class SessionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Session, SessionAdmin)

class SessionDetailAdmin(admin.ModelAdmin):
    pass

admin.site.register(SessionDetail, SessionDetailAdmin)
