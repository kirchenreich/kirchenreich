from django.contrib.gis.db import models

class KircheOsm(models.Model):
    osm_id = models.IntegerField()
    name = models.TextField(blank=True, null=True, default=None)
    religion = models.CharField(max_length=200,
                                blank=True, null=True, default=None)
    denomination = models.CharField(max_length=200,
                                    blank=True, null=True, default=None)
    # for now; later using hstore or extra table.
    addional_fields = models.TextField(blank=True, null=True,
                                       default=None)

    # if dataset is a way this should be the (calculated) center
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    point = models.PointField(blank=True, null=True)

    mpoly = models.MultiPolygonField(blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return "%s (%s) [%s]" % (self.id, self.name or '', self.religion or '')
