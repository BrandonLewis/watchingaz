from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('watchingaz.committees.views',
        (r'^$', 'index'),
        (r'^(?P<id>AZC\d{6})/', 'committee_detail'),
)