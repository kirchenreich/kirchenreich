# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KircheWikipedia.unite'
        db.add_column('wikipedia_kirchewikipedia', 'unite',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['krunite.KircheUnite'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'KircheWikipedia.unite'
        db.delete_column('wikipedia_kirchewikipedia', 'unite_id')


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
        'wikipedia.categorywikipedia': {
            'Meta': {'object_name': 'CategoryWikipedia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'wikipedia.kirchewikipedia': {
            'Meta': {'object_name': 'KircheWikipedia'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories+'", 'symmetrical': 'False', 'to': "orm['wikipedia.CategoryWikipedia']"}),
            'contents': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infobox': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'languages+'", 'symmetrical': 'False', 'to': "orm['wikipedia.LanguageWikipedia']"}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'unite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['krunite.KircheUnite']", 'null': 'True', 'blank': 'True'}),
            'values': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'values+'", 'symmetrical': 'False', 'to': "orm['wikipedia.ValueStore']"})
        },
        'wikipedia.languagewikipedia': {
            'Meta': {'object_name': 'LanguageWikipedia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wikipedia.valuestore': {
            'Meta': {'object_name': 'ValueStore'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
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

    complete_apps = ['wikipedia']