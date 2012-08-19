from django.contrib.gis.db import models
from datetime import datetime
from django.utils.timezone import utc

from krprj.world.models import WorldBorder
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

    last_update = models.DateTimeField(default=datetime.utcnow(
            ).replace(tzinfo=utc))
    created = models.DateTimeField(default=datetime.utcnow(
            ).replace(tzinfo=utc))

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')

    def save(self, *args, **kwargs):
        self.last_update = datetime.utcnow().replace(tzinfo=utc)
        super(KircheChecks, self).save(*args, **kwargs)

    def sum_checks(self):
        # FIXME: not count last_update and created!!
        return sum([field for field in KircheChecks._meta.fields])

    def run(self):
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


class KircheUniteManager(models.Manager):

    def correlate_all_osm(self):
        """ correlate osm datasets with wikipedia datasets
        """
        from krprj.osm.models import KircheOsm
        from krprj.wikipedia.models import KircheWikipedia
        for elem in KircheOsm.objects.all():
            self.correlate_osm(elem, KircheWikipedia)

    def get_country(self, point):
        try:
            return WorldBorder.objects.get(
                mpoly__intersects=point)
        except WorldBorder.DoesNotExist:
            return None

    def get_wikipedia(self, point, KircheWikipedia):
        # find all wikipedia entries within 100 meters
        pnts = KircheWikipedia.objects.filter(
            point__distance_lte=(point, 100))
        return pnts

    def correlate_osm(self, elem, KircheWikipedia):
        if not elem.unite:
            elem.unite = KircheUnite.objects.create(name=elem.name,
                                                    point=elem.point)
        elem.unite.country = self.get_country(elem.point)
        elem.unite.save()
        if not elem.unite.checks:
            elem.unite.checks = KircheChecks.objects.create(osm=True)
        elem.unite.checks.run()

        for pnt in self.get_wikipedia(elem.point, KircheWikipedia):
            elem.unite.kirchewikipedia_set.add(pnt)
            print elem.unite.kirchewikipedia_set.all()

        elem.unite.save()
        elem.save()


class KircheUnite(models.Model):
    # only for convenience
    name = models.TextField(blank=True, null=True, default=None)
    point = models.PointField(blank=True, null=True)

    country = models.ForeignKey(WorldBorder, blank=True, null=True)

    checks = models.OneToOneField(KircheChecks, blank=True, null=True)

    last_update = models.DateTimeField(default=datetime.utcnow(
            ).replace(tzinfo=utc))
    created = models.DateTimeField(default=datetime.utcnow(
            ).replace(tzinfo=utc))

    # manager
    objects = KircheUniteManager()

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')
