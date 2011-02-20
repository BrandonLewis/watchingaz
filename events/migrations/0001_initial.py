# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('participants', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])


    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('events_event')


    models = {
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'participants': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['events']
