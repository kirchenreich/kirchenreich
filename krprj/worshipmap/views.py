import json
from copy import copy

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from krprj.osm.models import KircheOsm
from krprj.wikipedia.models import KircheWikipedia


class WorshipMapView(TemplateView):
    """The index view of kirchenreich.org which shows the map with places of
    worship."""

    template_name = "worshipmap.html"

    def get_context_data(self, **kwargs):
        context = super(WorshipMapView, self).get_context_data(**kwargs)

        context['osm_places_count'] = KircheOsm.objects.count()
        context['wikipedia_places_count'] = KircheWikipedia.objects.count()
        return context


class PlaceOfWorshipDetailView(DetailView):
    """The detail view about a place of worship"""

    template_name = "place_of_worship_detail.html"
    model = KircheOsm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlaceOfWorshipDetailView, self).get_context_data(
            **kwargs)

        # Need point of place in EPSG:900913 for OpenLayers but don't want to
        # change self.object.point
        point = copy(self.object.point)
        point.transform(900913)
        context['point_for_openlayers'] = point

        context['addional_fields'] = json.loads(
            self.object.addional_fields
        )

        return context
