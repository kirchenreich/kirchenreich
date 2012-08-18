from django.conf.urls import patterns, url

from .views import WorshipMapView

urlpatterns = patterns('worshipmap.views',
    url(r'^$', WorshipMapView.as_view(), name='worshipmap'),
)
