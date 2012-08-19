from django.conf.urls import patterns, url

from .views import WorshipMapView, GetPlacesInBoxJSONView

urlpatterns = patterns('worshipmap.views',
    url(r'^$', WorshipMapView.as_view(), name='worshipmap'),
    url(r'^_get_places$', GetPlacesInBoxJSONView.as_view()),
)
