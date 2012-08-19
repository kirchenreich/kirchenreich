# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KircheOsm'
        db.create_table('osm_kircheosm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osm_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('religion', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('denomination', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('addional_fields', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mpoly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(null=True, blank=True)),
        ))
        db.send_create_signal('osm', ['KircheOsm'])


    def backwards(self, orm):
        # Deleting model 'KircheOsm'
        db.delete_table('osm_kircheosm')


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
            'religion': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['osm']