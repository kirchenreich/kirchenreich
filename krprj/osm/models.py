from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, MultiPolygon, Polygon

from krprj.krunite.models import KircheUnite

import json
from datetime import datetime
from django.utils.timezone import utc

class KircheOsm(models.Model):
    osm_id = models.IntegerField(db_index=True)
    TYPE_CHOICES = (
            ('N','node'),
            ('W','way'),
            )
    osm_type = models.CharField(max_length=5, choices = TYPE_CHOICES,
                                default='')

    name = models.TextField(blank=True, null=True, default=None)
    religion = models.TextField(blank=True, null=True, default=None)
    denomination = models.TextField(blank=True, null=True, default=None)
    # for now; later using hstore or extra table.
    addional_fields = models.TextField(blank=True, null=True,
                                       default=None)

    # if dataset is a way this should be the (calculated) center
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    point = models.PointField(blank=True, null=True)

    mpoly = models.MultiPolygonField(blank=True, null=True)

    unite = models.ForeignKey(KircheUnite, blank=True, null=True)

    objects = models.GeoManager()

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s (%s) [%s]" % (self.id, self.name or '', self.religion or '')

    def set_geo(self, lon=None, lat=None):
        """ set point and mpoly if necessary.
        a lot have been missed on import.
        """
        changed = False
        if not lon:
            lon = self.lon
        if not lat:
            lat = self.lat

        if not self.point and lon and lat:
            self.point = Point(lon, lat)
            changed = True

        if not self.mpoly and lon and lat:
            self.mpoly = MultiPolygon(Polygon(((lon, lat),
                                               (lon, lat),
                                               (lon, lat),
                                               (lon, lat))))
            changed = True

        if changed:
            self.save()

    def osm_url(self):
        if osm_type:
            base = 'http://www.openstreetmap.org/browse'
            return "%s/%s/%d" % (base, self.get_osm_type_display(), self.osm_id)
        else:
            return ''

    def jsonify(self):
        d = {'osm_id': self.osm_id,
             'name': self.name,
             'religion': self.religion,
             'denomination': self.denomination,
             'addional_fields': self.addional_fields,
             'lon': self.lon,
             'lat': self.lat,
             'point': self.point.json,
             'mpoly': self.mpoly.json,
             'unite': self.unite
             }
        return json.dumps(d)


class Ref(models.Model):
    """ table for caching references needed for ways
    """
    osm_id = models.IntegerField(db_index=True)
    point = models.PointField(blank=True, null=True)

    need_update = models.BooleanField(default=True)

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s (%s)" % (self.id, self.osm_id)

    def set_point(self, lon=None, lat=None):
        """ set point if necessary.
        """
        changed = False
        if not self.point and lon and lat:
            self.point = Point(lon, lat)
            changed = True
        if changed:
            self.save()
        return changed
