from django.conf.urls import patterns, url

from .views import WorshipMapView, PlaceOfWorshipDetailView, StatisticsView

urlpatterns = patterns('worshipmap.views',
    url(r'^statistics', StatisticsView.as_view()),
    url(r'^(?P<pk>\d+)', PlaceOfWorshipDetailView.as_view()),
    url(r'^$', WorshipMapView.as_view(), name='worshipmap'),
)
