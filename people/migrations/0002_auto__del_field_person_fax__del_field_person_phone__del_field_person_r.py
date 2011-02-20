# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Person.fax'
        db.delete_column('people_person', 'fax')

        # Deleting field 'Person.phone'
        db.delete_column('people_person', 'phone')

        # Deleting field 'Person.room'
        db.delete_column('people_person', 'room')

        # Adding field 'Person.office_address'
        db.add_column('people_person', 'office_address', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Person.office_phone'
        db.add_column('people_person', 'office_phone', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)

        # Adding field 'Person.office_fax'
        db.add_column('people_person', 'office_fax', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Person.fax'
        db.add_column('people_person', 'fax', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)

        # Adding field 'Person.phone'
        db.add_column('people_person', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True), keep_default=False)

        # Adding field 'Person.room'
        db.add_column('people_person', 'room', self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True), keep_default=False)

        # Deleting field 'Person.office_address'
        db.delete_column('people_person', 'office_address')

        # Deleting field 'Person.office_phone'
        db.delete_column('people_person', 'office_phone')

        # Deleting field 'Person.office_fax'
        db.delete_column('people_person', 'office_fax')


    models = {
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'leg_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'nimsp_candidate_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'office_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'office_fax': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'office_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'page_views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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
