from django.conf.urls.defaults import *
from watchingaz.base.views import blank
urlpatterns = patterns('watchingaz.bills.views',
    (r'^$', 'bill_index'),
    (r'^(\d{2})Leg/(\d\w)/(house|senate)/(resolution|bill|memorial|all|newest)/$', 'bills_by_chamber'),
    (r'^(?P<term>\d{2})Leg/(?P<session>\d\w)/(?P<bill_number>.*)/__history__.html', blank),
    (r'^(?P<term>\d{2})Leg/(?P<session>\d\w)/(?P<bill_number>.*)/(?P<version>[a-zA-Z]+\-[a-zA-Z]+)/$', 'bill_text'),
    (r'^(?P<term>\d{2})Leg/(?P<session>\d\w)/(?P<bill_number>.*)/$', 'bill_overview'),
)
