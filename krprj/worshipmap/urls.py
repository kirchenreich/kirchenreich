from django.conf.urls import patterns, url

from .views import WorshipMapView, PlaceOfWorshipDetailView, DashboardView

urlpatterns = patterns('worshipmap.views',
    url(r'^dashboard', DashboardView.as_view()),
    url(r'^(?P<pk>\d+)', PlaceOfWorshipDetailView.as_view()),
    url(r'^$', WorshipMapView.as_view(), name='worshipmap'),
)
