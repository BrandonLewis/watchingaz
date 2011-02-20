# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ActionType'
        db.create_table('bills_actiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('watchingaz.lib.models.multifield.MultiSelectField')(max_length=200)),
            ('full_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('bills', ['ActionType'])

        # Adding model 'BillAction'
        db.create_table('bills_billaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['bills.Bill'])),
            ('actor', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('bills', ['BillAction'])

        # Adding M2M table for field type on 'BillAction'
        db.create_table('bills_billaction_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('billaction', models.ForeignKey(orm['bills.billaction'], null=False)),
            ('actiontype', models.ForeignKey(orm['bills.actiontype'], null=False))
        ))
        db.create_unique('bills_billaction_type', ['billaction_id', 'actiontype_id'])

        # Adding model 'Bill'
        db.create_table('bills_bill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bills', to=orm['base.Session'])),
            ('chamber', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('final_disposition', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('page_views_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bills', ['Bill'])

        # Adding M2M table for field subjects on 'Bill'
        db.create_table('bills_bill_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bill', models.ForeignKey(orm['bills.bill'], null=False)),
            ('billsubject', models.ForeignKey(orm['bills.billsubject'], null=False))
        ))
        db.create_unique('bills_bill_subjects', ['bill_id', 'billsubject_id'])

        # Adding model 'BillPageView'
        db.create_table('bills_billpageview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='page_views', to=orm['bills.Bill'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bills', ['BillPageView'])

        # Adding model 'BillStatus'
        db.create_table('bills_billstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.OneToOneField')(related_name='status', unique=True, to=orm['bills.Bill'])),
            ('introduced', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('first_read_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('passed_primary', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('primary_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('passed_other', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('other_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('concur', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('concur_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('passed_gov', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('gov_date', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('bills', ['BillStatus'])

        # Adding model 'BillVote'
        db.create_table('bills_billvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['bills.Bill'])),
            ('chamber', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['committees.Committee'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('motion', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('passed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('yes_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('no_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('other_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('exc_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('abs_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('present_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('nv_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('type', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('bills', ['BillVote'])

        # Adding model 'BillSubject'
        db.create_table('bills_billsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('occurrence_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('bills', ['BillSubject'])

        # Adding model 'BillSource'
        db.create_table('bills_billsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sources', to=orm['bills.Bill'])),
        ))
        db.send_create_signal('bills', ['BillSource'])

        # Adding model 'VoteSource'
        db.create_table('bills_votesource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
        ))
        db.send_create_signal('bills', ['VoteSource'])

        # Adding model 'Document'
        db.create_table('bills_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', to=orm['bills.Bill'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('doc_type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('doc_id', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
        ))
        db.send_create_signal('bills', ['Document'])

        # Adding model 'Amendment'
        db.create_table('bills_amendment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='amendments', to=orm['bills.Bill'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('adopted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('bills', ['Amendment'])

        # Adding model 'Sponsor'
        db.create_table('bills_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.Bill'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('scraped_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('bills', ['Sponsor'])

        # Adding model 'Title'
        db.create_table('bills_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alternate_titles', to=orm['bills.Bill'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bills', ['Title'])

        # Adding model 'Version'
        db.create_table('bills_version', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='versions', to=orm['bills.Bill'])),
            ('document_id', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
        ))
        db.send_create_signal('bills', ['Version'])

        # Adding model 'VersionText'
        db.create_table('bills_versiontext', (
            ('node_id', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.Version'])),
        ))
        db.send_create_signal('bills', ['VersionText'])

        # Adding model 'YesVote'
        db.create_table('bills_yesvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['YesVote'])

        # Adding model 'NoVote'
        db.create_table('bills_novote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['NoVote'])

        # Adding model 'OtherVote'
        db.create_table('bills_othervote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['OtherVote'])

        # Adding model 'AbsentVote'
        db.create_table('bills_absentvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['AbsentVote'])

        # Adding model 'ExcusedVote'
        db.create_table('bills_excusedvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['ExcusedVote'])

        # Adding model 'NotVote'
        db.create_table('bills_notvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['NotVote'])

        # Adding model 'PresentVote'
        db.create_table('bills_presentvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['PresentVote'])

        # Adding model 'VacantVote'
        db.create_table('bills_vacantvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bills.BillVote'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
        ))
        db.send_create_signal('bills', ['VacantVote'])


    def backwards(self, orm):
        
        # Deleting model 'ActionType'
        db.delete_table('bills_actiontype')

        # Deleting model 'BillAction'
        db.delete_table('bills_billaction')

        # Removing M2M table for field type on 'BillAction'
        db.delete_table('bills_billaction_type')

        # Deleting model 'Bill'
        db.delete_table('bills_bill')

        # Removing M2M table for field subjects on 'Bill'
        db.delete_table('bills_bill_subjects')

        # Deleting model 'BillPageView'
        db.delete_table('bills_billpageview')

        # Deleting model 'BillStatus'
        db.delete_table('bills_billstatus')

        # Deleting model 'BillVote'
        db.delete_table('bills_billvote')

        # Deleting model 'BillSubject'
        db.delete_table('bills_billsubject')

        # Deleting model 'BillSource'
        db.delete_table('bills_billsource')

        # Deleting model 'VoteSource'
        db.delete_table('bills_votesource')

        # Deleting model 'Document'
        db.delete_table('bills_document')

        # Deleting model 'Amendment'
        db.delete_table('bills_amendment')

        # Deleting model 'Sponsor'
        db.delete_table('bills_sponsor')

        # Deleting model 'Title'
        db.delete_table('bills_title')

        # Deleting model 'Version'
        db.delete_table('bills_version')

        # Deleting model 'VersionText'
        db.delete_table('bills_versiontext')

        # Deleting model 'YesVote'
        db.delete_table('bills_yesvote')

        # Deleting model 'NoVote'
        db.delete_table('bills_novote')

        # Deleting model 'OtherVote'
        db.delete_table('bills_othervote')

        # Deleting model 'AbsentVote'
        db.delete_table('bills_absentvote')

        # Deleting model 'ExcusedVote'
        db.delete_table('bills_excusedvote')

        # Deleting model 'NotVote'
        db.delete_table('bills_notvote')

        # Deleting model 'PresentVote'
        db.delete_table('bills_presentvote')

        # Deleting model 'VacantVote'
        db.delete_table('bills_vacantvote')


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
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['bills.Bill']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bills.ActionType']", 'symmetrical': 'False'})
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

    complete_apps = ['bills']
