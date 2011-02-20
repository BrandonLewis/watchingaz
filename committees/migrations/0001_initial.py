# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Committee'
        db.create_table('committees_committee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committees.Committee'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('chamber', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('leg_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('page_views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('committees', ['Committee'])

        # Adding model 'CommitteeSource'
        db.create_table('committees_committeesource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', to=orm['committees.Committee'])),
        ))
        db.send_create_signal('committees', ['CommitteeSource'])

        # Adding model 'CommitteeMembers'
        db.create_table('committees_committeemembers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committees.Committee'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('committees', ['CommitteeMembers'])


    def backwards(self, orm):
        
        # Deleting model 'Committee'
        db.delete_table('committees_committee')

        # Deleting model 'CommitteeSource'
        db.delete_table('committees_committeesource')

        # Deleting model 'CommitteeMembers'
        db.delete_table('committees_committeemembers')


    models = {
        'committees.committee': {
            'Meta': {'object_name': 'Committee'},
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leg_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Person']", 'through': "orm['committees.CommitteeMembers']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'page_views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['committees.Committee']", 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'committees.committeemembers': {
            'Meta': {'object_name': 'CommitteeMembers'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['committees.Committee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'committees.committeesource': {
            'Meta': {'object_name': 'CommitteeSource'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'to': "orm['committees.Committee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
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
        }
    }

    complete_apps = ['committees']
