# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KircheChecks'
        db.create_table('krunite_kirchechecks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('osm_name', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('osm_religion', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('osm_denomination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('osm_address_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wikipedia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wikipedia_infobox', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('krunite', ['KircheChecks'])

        # Adding model 'KircheUnite'
        db.create_table('krunite_kircheunite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['world.WorldBorder'], null=True, blank=True)),
            ('checks', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['krunite.KircheChecks'], unique=True, null=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('krunite', ['KircheUnite'])


    def backwards(self, orm):
        # Deleting model 'KircheChecks'
        db.delete_table('krunite_kirchechecks')

        # Deleting model 'KircheUnite'
        db.delete_table('krunite_kircheunite')


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