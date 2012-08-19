from django.contrib.gis.db import models
from datetime import datetime

from krprj.osm.models import KircheOsm
from krprj.wikipedia.models import KircheWikipedia
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
        self.last_update = datetime.utcnow()
        super(KircheChecks, self).save(*args, **kwargs)

    def sum_checks(self):
        # FIXME: not count last_update and created!!
        return sum([field for field in KircheChecks._meta.fields])


class KircheUniteManager(models.Manager):

    def correlate(self):
        """ correlate osm datasets with wikipedia datasets
        """
        raise NotImplementedError


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

