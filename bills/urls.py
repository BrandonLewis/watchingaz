from django.conf.urls.defaults import *
urlpatterns = patterns('watchingaz.bills.views',
    (r'^$', 'bill_index'),
    (r'^(\d{2})Leg/(\d\w)/(house|senate)/(resolution|bill|memorial|all|newest)/$', 'bills_by_chamber'),
    (r'^(?P<term>\d{2})Leg/(?P<session>\d\w)/(?P<bill_number>.*)/(?P<version>.*)/$', 'bill_text'),
    (r'^(?P<term>\d{2})Leg/(?P<session>\d\w)/(?P<bill_number>.*)/$', 'bill_overview'),
)
