from django.conf.urls import patterns, include
from tastypie.api import Api

from .resources import PlacesResource, OSMPlacesResource

v1_api = Api(api_name='v1')
v1_api.register(PlacesResource())
v1_api.register(OSMPlacesResource())

urlpatterns = patterns('', (r'^', include(v1_api.urls)))
