from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class CategoryWikipedia(models.Model):
    name = models.CharField(max_length=50)
    language = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.language)


class LanguageWikipedia(models.Model):
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.language)


class ValueStore(models.Model):
    key = models.CharField(max_length=50, db_index=True)
    value = models.TextField(default='')

    def __unicode__(self):
        return "%s" % (self.key)


class KircheWikipedia(models.Model):
    title = models.CharField(max_length=200, db_index=True)

    infobox = models.TextField(blank=True, null=True, default=None)
    contents = models.TextField(blank=True, null=True, default=None)

    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    sha1 = models.TextField(blank=True, null=True, default=None)

    point = models.PointField(blank=True, null=True)

    categories = models.ManyToManyField(CategoryWikipedia,
                                        related_name='categories+')

    languages = models.ManyToManyField(LanguageWikipedia,
                                       related_name='languages+')

    values = models.ManyToManyField(ValueStore,
                                    related_name='values+')

    unite = models.ForeignKey("krunite.KircheUnite", blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return "%s" % self.title

    @property
    def url(self):
        title = self.title.replace(' ', '_')
        return "http://en.wikipedia.org/wiki/%s" % title

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
            self.save()

    def jsonify(self):
        d = {'title': self.title,
             'infobox': self.infobox,
             'contents': self.contents,
             'lon': self.lon,
             'lat': self.lat,
             'sha1': self.sha1,
             'point': self.point.json}
        return json.dumps(d)
