import json
from django.contrib.gis.db import models
from django.db.models import Count

from krprj.world.models import WorldBorder
from krprj.wikipedia.models import KircheWikipedia


class KircheChecks(models.Model):
    """
    """

    osm = models.BooleanField("OpenStreetMap place",
                              default=False)
    osm_name = models.BooleanField("OpenStreetMap place is named",
                                   default=False)
    osm_religion = models.BooleanField("OpenStreetMap has information "
                                       "about religion", default=False)
    osm_denomination = models.BooleanField("OpenStreetMap knows the "
                                           "denomination", default=False)
    osm_address_complete = models.BooleanField("Full address in "
                                               "OpenStreetMap", default=False)

    wikipedia = models.BooleanField("Wikipedia article", default=False)

    wikipedia_infobox = models.BooleanField("Wikipedia article has infobox",
                                            default=False)

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%d [%s] (%s/%s)" % (self.id, self.kircheunite.name or '',
                                    len(self.achieved), len(self.available))

    @property
    def available(self):
        """This property returns a list of available checks."""
        checks = []
        for field in self._meta.fields:
            if isinstance(field, models.BooleanField):
                checks.append(field.name)
        return checks

    @property
    def achieved(self):
        """Instead to available() this property returns the list of achieved
        checks by the unite object."""
        checks = []
        for field in self._meta.fields:
            if isinstance(field, models.BooleanField) \
            and getattr(self, field.name):
                checks.append(field.name)
        return checks

    @property
    def percent_reached(self):
        return float(len(self.achieved)) / float(len(self.available)) * 100

    @property
    def pretty(self):
        checks = []
        for check in self.available:
            field = self._meta.get_field_by_name(check)[0]
            checks.append({
                'name': check,
                'description': field.verbose_name,
                'value': getattr(self, check)
            })
        return checks

    def _run(self):
        """Don't run this method directly!
        Use KircheUnite.update_checks() instead.

        Run some quality checks over the osm and wikipedia objects.
        """

        if self.kircheunite:
            for osm in self.kircheunite.kircheosm_set.all():
                self.osm = True
                if osm.name:
                    self.osm_name = True
                if osm.religion:
                    self.osm_religion = True
                if osm.denomination:
                    self.osm_denomination = True
                d = json.loads(osm.addional_fields)
                if ('addr:housenumer' in d and
                    'addr:city' in d and
                    'addr:postcode' in d and
                    'addr:street' in d):
                    self.osm_address_complete = True

            for wiki in self.kircheunite.kirchewikipedia_set.all():
                self.wikipedia = True
                if len(wiki.infobox) > 3:
                    self.wikipedia_infobox = True

            self.save()


class KircheUniteManager(models.GeoManager):

    def get_by_osm_or_create(self, osm):
        """Get a KircheUnit object for KircheOsm object. If there no
        KircheUnite object than it will be create a new one and set name
        and point in the unite object from the Osm object.
        """

        unite_objs = self.filter(kircheosm=osm)
        if unite_objs.count() == 0:
            unite = self.model()
            unite.name = osm.name
            unite.point = osm.point
            unite.save()

            osm.unite = unite
            osm.save()

            # This is not perfect but it's working
            return self.filter(kircheosm=osm)

        return unite_objs


class KircheUnite(models.Model):
    """ Model for joining osm and wikipedia objects.
    ForeignKeys are from KircheOsm (kircheosm) and
                         KircheWikipedia (kirchewikipedia)
    """

    # name field is only for convenience
    name = models.TextField(blank=True, null=True, default=None)
    religion = models.TextField(blank=True, null=True, default=None)
    denomination = models.TextField(blank=True, null=True, default=None)

    point = models.PointField(srid=4326, blank=True, null=True)
    country = models.ForeignKey(WorldBorder, blank=True, null=True)

    checks = models.OneToOneField(KircheChecks, related_name='kircheunite',
                                  blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # manager
    objects = KircheUniteManager()

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')

    def update(self):
        """Update basedata, wikipedia; country; checks"""
        self.update_basedata()
        self.update_wikipedia()
        self.update_country()
        self.update_checks()

    def update_basedata(self):
        """If the unite doesn't have the basedata than it will try to get it
        from OSM or maybe wikipedia.
        """
        religion = self.kircheosm_set.values_list('religion') \
                                     .annotate(count=Count("id")) \
                                     .order_by('count')
        if len(religion) > 0:
            religion = religion[0][0]

        denomination = self.kircheosm_set.values_list('denomination') \
                                         .annotate(count=Count("id")) \
                                         .order_by('count')
        if len(denomination) > 0:
            denomination = denomination[0][0]

        if religion:
            self.religion = religion
        if denomination:
            self.denomination = denomination

        if religion or denomination:
            self.save()

    def update_wikipedia(self):
        """Try to find some wikipedia objects within a radius of 100m to the
        point of the unite object.
        """
        if self.point is None:
            return

        articles = KircheWikipedia.objects.filter(
            point__distance_lte=(self.point, 100)
        )
        self.kirchewikipedia_set.add(*articles)
        return articles

    def update_country(self):
        """Take the point of the unite object and update the country into the
        database and return the result.
        """
        if self.point is None:
            return None

        try:
            self.country = WorldBorder.objects.get(
                mpoly__intersects=self.point
            )
            self.save()
            return self.country
        except WorldBorder.DoesNotExist:
            return None

    def update_checks(self):
        """Update/Create the check object and run the available checks"""
        if self.checks is None:
            self.checks = KircheChecks()
            self.checks.save()

            self.checks_id = self.checks.id
            self.save()

        self.checks._run()
