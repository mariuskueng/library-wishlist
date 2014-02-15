# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Copy.branch' to match new field type.
        db.rename_column(u'library_wishlist_copy', 'branch', 'branch_id')
        # Changing field 'Copy.branch'
        db.alter_column(u'library_wishlist_copy', 'branch_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['library_wishlist.Branch']))
        # Adding index on 'Copy', fields ['branch']
        db.create_index(u'library_wishlist_copy', ['branch_id'])


    def backwards(self, orm):
        # Removing index on 'Copy', fields ['branch']
        db.delete_index(u'library_wishlist_copy', ['branch_id'])


        # User chose to not deal with backwards NULL issues for 'Copy.branch'
        raise RuntimeError("Cannot reverse this migration. 'Copy.branch' and its values cannot be restored.")

    models = {
        u'library_wishlist.branch': {
            'Meta': {'object_name': 'Branch'},
            'adress': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'opening_hours': ('django.db.models.fields.TextField', [], {})
        },
        u'library_wishlist.copy': {
            'Meta': {'object_name': 'Copy'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branches'", 'null': 'True', 'to': u"orm['library_wishlist.Branch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'copies'", 'null': 'True', 'to': u"orm['library_wishlist.Item']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'library_wishlist.item': {
            'Meta': {'ordering': "['-created', 'status']", 'object_name': 'Item'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 15, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['library_wishlist']