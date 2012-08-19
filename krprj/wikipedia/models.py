from django.contrib.gis.db import models

class CategoryWikipedia(models.Model):
    name = models.CharField(max_length=50)
    language =  models.CharField(max_length=10)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.language)

class LanguageWikipedia(models.Model):
    title =  models.CharField(max_length=200)
    language = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.language)

class ValueStore(models.Model):
    key =  models.CharField(max_length=50, db_index=True)
    value = models.TextField(default='')

    def __unicode__(self):
        return "%s" % (self.key)
    
class KircheWikipedia(models.Model):
    title = models.CharField(max_length=200)

    infobox = models.TextField(blank=True, null=True, default=None)
    contents = models.TextField(blank=True, null=True, default=None)

    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    sha1 = models.TextField(blank=True, null=True, default=None)

    categories = models.ManyToManyField(CategoryWikipedia,
                                        related_name='categories+')

    languages = models.ManyToManyField(LanguageWikipedia,
                                       related_name='languages+')

    values = models.ManyToManyField(ValueStore,
                                    related_name='values+')

    objects = models.GeoManager()

    def __unicode__(self):
        return "%s" % self.title

