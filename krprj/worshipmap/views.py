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
        p1x, p1y, p2x, p2y = (
            float(n) for n in request.GET.get('in_bbox').split(',')
        )
        p1 = Point(p1x, p1y, srid=900913)
        p1.transform(4326)
        p2 = Point(p2x, p2y, srid=900913)
        p2.transform(4326)

        visible_map = Polygon.from_bbox(
            (p1.x, p1.y, p2.x, p2.y)
        )

        countries = WorldBorder.objects.filter(mpoly__intersects=visible_map)
        return HttpResponse(json.dumps({
            'countries': list(countries.values('name', 'iso2'))
        }))
