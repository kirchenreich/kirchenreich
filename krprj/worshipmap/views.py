import json
from copy import copy

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from krprj.osm.models import KircheOsm
from krprj.osm.models import Ref
from krprj.wikipedia.models import KircheWikipedia

import datetime
from django.utils.timezone import utc


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
        point.transform(3857)
        context['point_for_openlayers'] = point

        context['addional_fields'] = json.loads(
            self.object.addional_fields
        )

        if self.object.unite:
            context['checks'] = self.object.unite.checks
            context['wikipedia_pages'] = self.object.unite\
                                                    .kirchewikipedia_set.all()

        return context

class StatisticsView(TemplateView):
    """Show some stats about the data"""

    template_name = "statistics.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatisticsView, self).get_context_data(
            **kwargs)

        # Ref counts
        context['ref_need_update'] = Ref.objects.filter(need_update=True).count()
        context['ref_count'] = Ref.objects.count()

        # osm_types
        data = [i[0] for i in KircheOsm.objects.values_list('osm_type')]
        uniques = set(data)
        data = dict([(i, data.count(i)) for i in uniques])
        context['osm_type'] = data

        # date
        context['older_than_1week'] = KircheOsm.objects.filter(last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=7))).count()
        context['older_than_2weeks'] = KircheOsm.objects.filter(last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=14))).count()
        context['older_than_3weeks'] = KircheOsm.objects.filter(last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=21))).count()

        return context
