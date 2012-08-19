from django.conf.urls import patterns, url

from .views import WorshipMapView, PlaceOfWorshipDetailView

urlpatterns = patterns('worshipmap.views',
    url(r'^(?P<pk>\d+)', PlaceOfWorshipDetailView.as_view()),
    url(r'^$', WorshipMapView.as_view(), name='worshipmap'),
)
