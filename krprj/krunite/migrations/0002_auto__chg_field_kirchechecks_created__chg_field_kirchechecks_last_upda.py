# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'KircheChecks.created'
        db.alter_column('krunite_kirchechecks', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'KircheChecks.last_update'
        db.alter_column('krunite_kirchechecks', 'last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))
        # Adding field 'KircheUnite.religion'
        db.add_column('krunite_kircheunite', 'religion',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'KircheUnite.denomination'
        db.add_column('krunite_kircheunite', 'denomination',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


        # Changing field 'KircheUnite.created'
        db.alter_column('krunite_kircheunite', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'KircheUnite.last_update'
        db.alter_column('krunite_kircheunite', 'last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):

        # Changing field 'KircheChecks.created'
        db.alter_column('krunite_kirchechecks', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'KircheChecks.last_update'
        db.alter_column('krunite_kirchechecks', 'last_update', self.gf('django.db.models.fields.DateTimeField')())
        # Deleting field 'KircheUnite.religion'
        db.delete_column('krunite_kircheunite', 'religion')

        # Deleting field 'KircheUnite.denomination'
        db.delete_column('krunite_kircheunite', 'denomination')


        # Changing field 'KircheUnite.created'
        db.alter_column('krunite_kircheunite', 'created', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'KircheUnite.last_update'
        db.alter_column('krunite_kircheunite', 'last_update', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'krunite.kirchechecks': {
            'Meta': {'object_name': 'KircheChecks'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'osm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_address_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_denomination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_religion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wikipedia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wikipedia_infobox': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'krunite.kircheunite': {
            'Meta': {'object_name': 'KircheUnite'},
            'checks': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'kircheunite'", 'unique': 'True', 'null': 'True', 'to': "orm['krunite.KircheChecks']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.WorldBorder']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'denomination': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'world.worldborder': {
            'Meta': {'object_name': 'WorldBorder'},
            'area': ('django.db.models.fields.IntegerField', [], {}),
            'fips': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pop2005': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {}),
            'subregion': ('django.db.models.fields.IntegerField', [], {}),
            'un': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['krunite']