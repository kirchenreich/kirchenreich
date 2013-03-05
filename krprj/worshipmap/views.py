import json

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Count, Q

from krprj.krunite.models import KircheUnite, KircheChecks
from krprj.osm.models import KircheOsm, Ref
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
    model = KircheUnite

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlaceOfWorshipDetailView, self).get_context_data(
            **kwargs)

        context['checks'] = self.object.checks
        context['checks_percent_reached'] = round(
            self.object.checks.percent_reached
        )

        self.object.point.transform(4326)
        context['point'] = self.object.point

        context['osm_places'] = []
        for osm_place in self.object.kircheosm_set.all():
            # Need point of place in EPSG:4326 for Leaflet
            osm_place.point.transform(4326)
            context['osm_places'].append({
                'osm_id': osm_place.osm_id,
                'name': osm_place.name,
                'religion': osm_place.religion,
                'denomination': osm_place.denomination,
                'point': osm_place.point,
                'addional_fields': json.loads(osm_place.addional_fields)
            })
        context['wikipedia_pages'] = self.object.kirchewikipedia_set.all()
        return context


class DashboardView(TemplateView):
    """Show some stats about the data"""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['wikipedia_count'] = KircheWikipedia.objects.count()
        context['osm_count'] = KircheOsm.objects.count()
        context['krunite_count'] = KircheUnite.objects.count()

        # Ref counts
        context['ref_need_update'] = Ref.objects.filter(need_update=True) \
                                                .count()
        context['ref_count'] = Ref.objects.count()

        # osm_types
        context['osm_type'] = KircheOsm.objects.values_list('osm_type') \
                                               .annotate(count=Count("id"))
        context['osm_type'] = dict(context['osm_type'])

        # Wikipedia
        context['wikipedia_infobox_count'] = KircheWikipedia.objects \
                                                .filter(~Q(infobox="{}")) \
                                                .count()

        # Checks
        context['checks'] = []
        for check in KircheChecks().available:
            filter = {check: 1}
            check = {
                'name': check,
                'reached': KircheChecks.objects.filter(**filter).count(),
                'description': KircheChecks().get_check_description(check)
            }
            check['pending'] = context['krunite_count'] - check['reached']
            check['percent_reached'] = round(
                float(check['reached']) / float(context['krunite_count']) \
                * 100,
                3
            )
            print check
            context['checks'].append(check)

        print context['checks']

        # date
        context['last_7days'] = KircheOsm.objects.filter(
            last_update__gt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=7)
            )
        ).count()
        context['older_than_1week'] = KircheOsm.objects.filter(
            last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=7)
            )
        ).count()
        context['older_than_2weeks'] = KircheOsm.objects.filter(last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=14)
            )
        ).count()
        context['older_than_3weeks'] = KircheOsm.objects.filter(last_update__lt=(
                datetime.datetime.utcnow().replace(tzinfo=utc) -
                datetime.timedelta(days=21)
            )
        ).count()

        return context
