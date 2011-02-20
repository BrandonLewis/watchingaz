from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('watchingaz.people.views',
        (r'^$', 'person_index'),
        (r'^(?P<id>AZL\d{6})/', 'person_view'),
)