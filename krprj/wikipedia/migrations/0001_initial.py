# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryWikipedia'
        db.create_table('wikipedia_categorywikipedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('wikipedia', ['CategoryWikipedia'])

        # Adding model 'LanguageWikipedia'
        db.create_table('wikipedia_languagewikipedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('wikipedia', ['LanguageWikipedia'])

        # Adding model 'ValueStore'
        db.create_table('wikipedia_valuestore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('wikipedia', ['ValueStore'])

        # Adding model 'KircheWikipedia'
        db.create_table('wikipedia_kirchewikipedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('infobox', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('contents', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('wikipedia', ['KircheWikipedia'])

        # Adding M2M table for field categories on 'KircheWikipedia'
        db.create_table('wikipedia_kirchewikipedia_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kirchewikipedia', models.ForeignKey(orm['wikipedia.kirchewikipedia'], null=False)),
            ('categorywikipedia', models.ForeignKey(orm['wikipedia.categorywikipedia'], null=False))
        ))
        db.create_unique('wikipedia_kirchewikipedia_categories', ['kirchewikipedia_id', 'categorywikipedia_id'])

        # Adding M2M table for field languages on 'KircheWikipedia'
        db.create_table('wikipedia_kirchewikipedia_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kirchewikipedia', models.ForeignKey(orm['wikipedia.kirchewikipedia'], null=False)),
            ('languagewikipedia', models.ForeignKey(orm['wikipedia.languagewikipedia'], null=False))
        ))
        db.create_unique('wikipedia_kirchewikipedia_languages', ['kirchewikipedia_id', 'languagewikipedia_id'])

        # Adding M2M table for field values on 'KircheWikipedia'
        db.create_table('wikipedia_kirchewikipedia_values', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kirchewikipedia', models.ForeignKey(orm['wikipedia.kirchewikipedia'], null=False)),
            ('valuestore', models.ForeignKey(orm['wikipedia.valuestore'], null=False))
        ))
        db.create_unique('wikipedia_kirchewikipedia_values', ['kirchewikipedia_id', 'valuestore_id'])


    def backwards(self, orm):
        # Deleting model 'CategoryWikipedia'
        db.delete_table('wikipedia_categorywikipedia')

        # Deleting model 'LanguageWikipedia'
        db.delete_table('wikipedia_languagewikipedia')

        # Deleting model 'ValueStore'
        db.delete_table('wikipedia_valuestore')

        # Deleting model 'KircheWikipedia'
        db.delete_table('wikipedia_kirchewikipedia')

        # Removing M2M table for field categories on 'KircheWikipedia'
        db.delete_table('wikipedia_kirchewikipedia_categories')

        # Removing M2M table for field languages on 'KircheWikipedia'
        db.delete_table('wikipedia_kirchewikipedia_languages')

        # Removing M2M table for field values on 'KircheWikipedia'
        db.delete_table('wikipedia_kirchewikipedia_values')


    models = {
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
        }
    }

    complete_apps = ['wikipedia']