from django.contrib.gis.db import models
from datetime import datetime
from django.utils.timezone import utc

from krprj.world.models import WorldBorder


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


    last_update = models.DateTimeField(default=datetime.utcnow)
    created = models.DateTimeField(default=datetime.utcnow)

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')

    def save(self, *args, **kwargs):
        self.last_update = datetime.utcnow().replace(tzinfo=utc)
        super(KircheChecks, self).save(*args, **kwargs)

    def sum_checks(self):
        # FIXME: not count last_update and created!!
        return sum([field for field in KircheChecks._meta.fields])

    def run(self):
        pass


class KircheUniteManager(models.Manager):

    def correlate_all_osm(self):
        """ correlate osm datasets with wikipedia datasets
        """
        from krprj.osm.models import KircheOsm
        from krprj.world.models import WorldBorder
        from krprj.wikipedia.models import KircheWikipedia

        for elem in KircheOsm.objects.all()[0:1]:
            if not elem.unite:
                elem.unite = KircheUnite.objects.create(name=elem.name,
                                                        point=elem.point)
            elem.unite.country = WorldBorder.objects.get(
                mpoly__intersects=elem.point)
            elem.unite.save()
            if not elem.unite.checks:
                chks = KircheChecks.objects.create(osm=True)
            chks.run()
            elem.unite.checks = chks

            # find all wikipedia entries within 100 meters
            # KircheWikipedia.objects.filter(point__distance_lte=(a.point, 100))

            elem.unite.save()
            elem.save()


class KircheUnite(models.Model):
    # only for convenience
    name = models.TextField(blank=True, null=True, default=None)
    point = models.PointField(blank=True, null=True)

    country = models.ForeignKey(WorldBorder, blank=True, null=True)

    checks = models.OneToOneField(KircheChecks, blank=True, null=True)

    last_update = models.DateTimeField(default=datetime.utcnow)
    created = models.DateTimeField(default=datetime.utcnow)

    # manager
    objects = KircheUniteManager()

    def __unicode__(self):
        return "%d [%s]" % (self.id, self.name or '')

