# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field type on 'BillAction'
        db.delete_table('bills_billaction_type')


    def backwards(self, orm):
        
        # Adding M2M table for field type on 'BillAction'
        db.create_table('bills_billaction_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billaction', models.ForeignKey(orm['bills.billaction'], null=False)),
            ('actiontype', models.ForeignKey(orm['bills.actiontype'], null=False))
        ))
        db.create_unique('bills_billaction_type', ['billaction_id', 'actiontype_id'])


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
        'base.term': {
            'Meta': {'object_name': 'Term'},
            'end_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'terms'", 'to': "orm['base.Metadata']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'start_year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True'})
        },
        'bills.absentvote': {
            'Meta': {'object_name': 'AbsentVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.actiontype': {
            'Meta': {'object_name': 'ActionType'},
            'full_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('watchingaz.lib.models.multifield.MultiSelectField', [], {'max_length': '200'})
        },
        'bills.amendment': {
            'Meta': {'object_name': 'Amendment'},
            'adopted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'amendments'", 'to': "orm['bills.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'bills.bill': {
            'Meta': {'object_name': 'Bill'},
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'final_disposition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'page_views_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bills'", 'to': "orm['base.Session']"}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Person']", 'through': "orm['bills.Sponsor']", 'symmetrical': 'False'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bills.BillSubject']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'bills.billaction': {
            'Meta': {'object_name': 'BillAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'actor': ('django.db.models.fields.TextField', [], {}),
            'atype': ('watchingaz.lib.models.multifield.MultiSelectField', [], {'max_length': '200'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['bills.Bill']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bills.billpageview': {
            'Meta': {'object_name': 'BillPageView'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'page_views'", 'to': "orm['bills.Bill']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'bills.billsource': {
            'Meta': {'object_name': 'BillSource'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sources'", 'to': "orm['bills.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'bills.billstatus': {
            'Meta': {'object_name': 'BillStatus'},
            'bill': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'status'", 'unique': 'True', 'to': "orm['bills.Bill']"}),
            'concur': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'concur_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_read_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gov_date': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduced': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'other_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'passed_gov': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'passed_other': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'passed_primary': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'primary_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'bills.billsubject': {
            'Meta': {'object_name': 'BillSubject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occurrence_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'bills.billvote': {
            'Meta': {'object_name': 'BillVote'},
            'abs_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['bills.Bill']"}),
            'chamber': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['committees.Committee']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'exc_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'no_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'no_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'no_votes'", 'to': "orm['people.Person']", 'through': "orm['bills.NoVote']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'nv_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'other_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'other_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'other_votes'", 'to': "orm['people.Person']", 'through': "orm['bills.OtherVote']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'present_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'yes_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'yes_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'yes_votes'", 'to': "orm['people.Person']", 'through': "orm['bills.YesVote']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        'bills.document': {
            'Meta': {'object_name': 'Document'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': "orm['bills.Bill']"}),
            'doc_id': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'doc_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'bills.excusedvote': {
            'Meta': {'object_name': 'ExcusedVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.notvote': {
            'Meta': {'object_name': 'NotVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.novote': {
            'Meta': {'object_name': 'NoVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.othervote': {
            'Meta': {'object_name': 'OtherVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.presentvote': {
            'Meta': {'object_name': 'PresentVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'}),
            'scraped_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'bills.title': {
            'Meta': {'object_name': 'Title'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alternate_titles'", 'to': "orm['bills.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'bills.vacantvote': {
            'Meta': {'object_name': 'VacantVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.version': {
            'Meta': {'object_name': 'Version'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['bills.Bill']"}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'bills.versiontext': {
            'Meta': {'object_name': 'VersionText'},
            'node_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.Version']"})
        },
        'bills.votesource': {
            'Meta': {'object_name': 'VoteSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
        'bills.yesvote': {
            'Meta': {'object_name': 'YesVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.BillVote']"})
        },
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
            'transparencydata_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'votesmart_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bills']
