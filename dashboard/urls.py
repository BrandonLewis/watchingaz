from django.conf.urls.defaults import *
urlpatterns = patterns('watching_az.dashboard.views',
    (r'^mydashboard/$', 'index'),
    #(r'^$')
)
  