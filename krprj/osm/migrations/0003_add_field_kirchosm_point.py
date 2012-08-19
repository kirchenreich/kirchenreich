# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.gis.geos import Point

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for node in orm['osm.KircheOsm'].objects.all():
            node.point = Point(node.lon, node.lat)
            node.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'osm.kircheosm': {
            'Meta': {'object_name': 'KircheOsm'},
            'addional_fields': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'denomination': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'osm_id': ('django.db.models.fields.IntegerField', [], {}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['osm']
    symmetrical = True
