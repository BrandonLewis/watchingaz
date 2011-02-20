# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Metadata'
        db.create_table('base_metadata', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('legislature_name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('lower_chamber_name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('upper_chamber_name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('lower_chamber_title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('upper_chamber_title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('lower_chamber_term', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('upper_chamber_term', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('latest_dump_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('latest_dump_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Metadata'])

        # Adding model 'Term'
        db.create_table('base_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('start_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True)),
            ('end_year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True)),
            ('metadata', self.gf('django.db.models.fields.related.ForeignKey')(related_name='terms', to=orm['base.Metadata'])),
        ))
        db.send_create_signal('base', ['Term'])

        # Adding model 'Session'
        db.create_table('base_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['base.Term'])),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Session'])

        # Adding model 'SessionDetail'
        db.create_table('base_sessiondetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('session', self.gf('django.db.models.fields.related.OneToOneField')(related_name='session_details', unique=True, to=orm['base.Session'])),
            ('s_id', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('metadata', self.gf('django.db.models.fields.related.ForeignKey')(related_name='session_details', to=orm['base.Metadata'])),
        ))
        db.send_create_signal('base', ['SessionDetail'])


    def backwards(self, orm):
        
        # Deleting model 'Metadata'
        db.delete_table('base_metadata')

        # Deleting model 'Term'
        db.delete_table('base_term')

        # Deleting model 'Session'
        db.delete_table('base_session')

        # Deleting model 'SessionDetail'
        db.delete_table('base_sessiondetail')


    models = {
        'base.metadata': {
            'Meta': {'object_name': 'Metadata'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'latest_dump_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latest_dump_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'legislature_name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'lower_chamber_name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'lower_chamber_term': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'lower_chamber_title': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'upper_chamber_name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'upper_chamber_term': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'upper_chamber_title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'base.session': {
            'Meta': {'object_name': 'Session'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['base.Term']"})
        },
        'base.sessiondetail': {
            'Meta': {'object_name': 'SessionDetail'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_details'", 'to': "orm['base.Metadata']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            's_id': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'session_details'", 'unique': 'True', 'to': "orm['base.Session']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'base.term': {
            'Meta': {'object_name': 'Term'},
            'end_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['base.Metadata']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'})
        }
    }

    complete_apps = ['base']
