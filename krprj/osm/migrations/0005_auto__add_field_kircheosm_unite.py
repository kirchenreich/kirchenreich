# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KircheOsm.unite'
        db.add_column('osm_kircheosm', 'unite',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['krunite.KircheUnite'], null=True, blank=True),
                      keep_default=False)

        # Adding index on 'KircheOsm', fields ['osm_id']
#        db.create_index('osm_kircheosm', ['osm_id'])


    def backwards(self, orm):
        # Removing index on 'KircheOsm', fields ['osm_id']
        db.delete_index('osm_kircheosm', ['osm_id'])

        # Deleting field 'KircheOsm.unite'
#        db.delete_column('osm_kircheosm', 'unite_id')


    models = {
        'krunite.kirchechecks': {
            'Meta': {'object_name': 'KircheChecks'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
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
            'checks': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['krunite.KircheChecks']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['world.WorldBorder']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'})
        },
        'osm.kircheosm': {
            'Meta': {'object_name': 'KircheOsm'},
            'addional_fields': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'denomination': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'osm_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'unite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['krunite.KircheUnite']", 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['osm']
