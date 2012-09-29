from django.contrib.gis.db import models
from datetime import datetime
from django.utils.timezone import utc

from krprj.world.models import WorldBorder
from krprj.wikipedia.models import KircheWikipedia
import json


class KircheChecks(models.Model):
    """
    """

    osm = models.BooleanField(default=False)

    osm_name = models.BooleanField(default=False)
    osm_religion = models.BooleanField(default=False)
    osm_denomination = models.BooleanField(default=False)
    osm_address_complete = models.BooleanField(default=False)

    wikipedia = models.BooleanField(default=False)

    wikipedia_infobox = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%d [%s] (%s/%s)" % (self.id, self.kircheunite.name or '',
                                    self.achieved, self.available)

    @property
    def available(self):
        count = 0
        for field in self._meta.fields:
            if isinstance(field, models.BooleanField):
                count += 1
        return count

    @property
    def achieved(self):
        count = 0
        for field in self._meta.fields:
            if isinstance(field, models.BooleanField):
                count += int(getattr(self, field.name))
        return count

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


class KircheUniteManager(models.Manager):

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
    """ Table for joining osm and wikipedia datasets.
    ForeignKeys are from KircheOsm (kircheosm) and
                         KircheWikipedia (kirchewikipedia)
    """

    # name field is only for convenience
    name = models.TextField(blank=True, null=True, default=None)
    point = models.PointField(blank=True, null=True)

    country = models.ForeignKey(WorldBorder, blank=True, null=True)

    checks = models.OneToOneField(KircheChecks, blank=True, null=True)

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # manager
    objects = KircheUniteManager()

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')

    def update_wikipedia(self):
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
        if self.checks is None:
            self.checks = KircheChecks()
            self.checks.save()
            self.save()

        self.checks._run()
