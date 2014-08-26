# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RedditCredentials'
        db.create_table('verifier_redditcredentials', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reddit_username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=256)),
            ('reddit_password', self.gf('django.db.models.fields.CharField')(blank=True, max_length=256)),
        ))
        db.send_create_signal('verifier', ['RedditCredentials'])

        # Adding model 'Subreddit'
        db.create_table('verifier_subreddit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('credentials', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['verifier.RedditCredentials'])),
        ))
        db.send_create_signal('verifier', ['Subreddit'])

        # Adding model 'Gender'
        db.create_table('verifier_gender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('verifier', ['Gender'])

        # Adding model 'GenderSubreddit'
        db.create_table('verifier_gendersubreddit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['verifier.Gender'])),
            ('subreddit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['verifier.Subreddit'])),
            ('flair_css', self.gf('django.db.models.fields.CharField')(blank=True, max_length=128, null=True)),
            ('flair_text', self.gf('django.db.models.fields.CharField')(blank=True, max_length=128, null=True)),
        ))
        db.send_create_signal('verifier', ['GenderSubreddit'])

        # Adding unique constraint on 'GenderSubreddit', fields ['gender', 'subreddit']
        db.create_unique('verifier_gendersubreddit', ['gender_id', 'subreddit_id'])

        # Adding model 'Verification'
        db.create_table('verifier_verification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['verifier.Gender'])),
            ('verified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('verified_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('verifier', ['Verification'])


    def backwards(self, orm):
        # Removing unique constraint on 'GenderSubreddit', fields ['gender', 'subreddit']
        db.delete_unique('verifier_gendersubreddit', ['gender_id', 'subreddit_id'])

        # Deleting model 'RedditCredentials'
        db.delete_table('verifier_redditcredentials')

        # Deleting model 'Subreddit'
        db.delete_table('verifier_subreddit')

        # Deleting model 'Gender'
        db.delete_table('verifier_gender')

        # Deleting model 'GenderSubreddit'
        db.delete_table('verifier_gendersubreddit')

        # Deleting model 'Verification'
        db.delete_table('verifier_verification')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'verifier.gender': {
            'Meta': {'object_name': 'Gender'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'subreddits': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['verifier.Subreddit']", 'symmetrical': 'False', 'through': "orm['verifier.GenderSubreddit']"})
        },
        'verifier.gendersubreddit': {
            'Meta': {'object_name': 'GenderSubreddit', 'unique_together': "(('gender', 'subreddit'),)"},
            'flair_css': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128', 'null': 'True'}),
            'flair_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128', 'null': 'True'}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['verifier.Gender']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['verifier.Subreddit']"})
        },
        'verifier.redditcredentials': {
            'Meta': {'object_name': 'RedditCredentials'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reddit_password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'reddit_username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'})
        },
        'verifier.subreddit': {
            'Meta': {'object_name': 'Subreddit'},
            'credentials': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['verifier.RedditCredentials']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'verifier.verification': {
            'Meta': {'object_name': 'Verification'},
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['verifier.Gender']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'verified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'verified_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['verifier']