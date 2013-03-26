from django.conf.urls.defaults import patterns, include, url
from plivocall import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',(r'^$', views.plivo_start),
(r'^plivo/answer/$',views.plivo_answer),
(r'^plivo/hangup/$',views.plivo_hangup),
(r'^plivo/makecall/$',views.makecall),
(r'^plivo/ratings/$',views.plivo_ratings),
)
