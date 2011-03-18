from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^bills/', include('watchingaz.bills.urls')),
    (r'^people/', include('watchingaz.people.urls')),
    (r'^committees/', include('watchingaz.committees.urls')),
    # accounts and profiles
    (r'^accounts/', include('registration.backends.default.urls')),
    # tools and apis
    #(r'locksmith/', include('locksmith.hub.urls')),
    (r'^ns/', include('watchingaz.tools.urls')),
    (r'^trackers/add/', 'watchingaz.tools.views.add_tracker'),
    (r'^search/', 'watchingaz.tools.views.search'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'watchingaz.base.views.index'),
)
