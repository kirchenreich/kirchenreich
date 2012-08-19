import json

from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.contrib.gis.geos import Point, Polygon

from krprj.world.models import WorldBorder


class WorshipMapView(TemplateView):
    """The index view of kirchenreich.org which shows the map with places of
    worship."""

    template_name = "worshipmap.html"

    def get_context_data(self, **kwargs):
        context = super(WorshipMapView, self).get_context_data(**kwargs)
        return context


class GetPlacesInBoxJSONView(View):

    def get(self, request, *args, **kwargs):

        # Get cordinates for bbox from get parameter
        p1x, p1y, p2x, p2y = (
            float(n) for n in request.GET.get('in_bbox').split(',')
        )
        # Create min and max points with cordinates in EPSG:900913 for bbox
        p1 = Point(p1x, p1y, srid=900913)
        p2 = Point(p2x, p2y, srid=900913)

        # Transform EPSG:900913 (from OpenLayers) to EPSG:4326 (WGS64)
        p1.transform(4326)
        p2.transform(4326)

        # Create bbox which represents the visible map
        visible_map = Polygon.from_bbox(
            (p1.x, p1.y, p2.x, p2.y)
        )

        # Look for countries which are intersects by our visible map
        countries = WorldBorder.objects.filter(mpoly__intersects=visible_map)

        return HttpResponse(json.dumps({
            'countries': list(countries.values('name', 'iso2'))
        }))
