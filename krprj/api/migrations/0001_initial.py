# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Changes'
        db.create_table('api_changes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_xml', self.gf('django.db.models.fields.TextField')()),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('api', ['Changes'])


    def backwards(self, orm):
        # Deleting model 'Changes'
        db.delete_table('api_changes')


    models = {
        'api.changes': {
            'Meta': {'object_name': 'Changes'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_xml': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['api']