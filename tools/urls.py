from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('watchingaz.tools.views',
    (r'^ontology.owl$', 'ontology'),
    (r'^Bill/(?P<session>\d{2}\w+\d\w{2}\-[regular|special])/(?P<bill_number>\w+\-\d{4})/$', 'bill_rdf'),
    (r'^(?P<subject_class>\w+)/(?P<subject_id>\w+)/$', 'subject_view'),
)