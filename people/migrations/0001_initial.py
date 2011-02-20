# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('people_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('suffixes', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chamber', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(default='AZ', max_length=2)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('leg_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
            ('nimsp_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('votesmart_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('transparencydata_id', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('page_views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('people', ['Person'])

        # Adding model 'Role'
        db.create_table('people_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['people.Person'])),
            ('chamber', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(default='AZ', max_length=2)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('committee', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subcommittee', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('people', ['Role'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('people_person')

        # Deleting model 'Role'
        db.delete_table('people_role')


    models = {
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'leg_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'nimsp_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'page_views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'default': "'AZ'", 'max_length': '2'}),
            'suffixes': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'transparencydata_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'votesmart_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'people.role': {
            'Meta': {'object_name': 'Role'},
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['people.Person']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'default': "'AZ'", 'max_length': '2'}),
            'subcommittee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['people']
