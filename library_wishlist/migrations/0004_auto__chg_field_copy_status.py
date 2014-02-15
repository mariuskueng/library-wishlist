# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Copy.status'
        db.alter_column(u'library_wishlist_copy', 'status', self.gf('django.db.models.fields.BooleanField')())

    def backwards(self, orm):

        # Changing field 'Copy.status'
        db.alter_column(u'library_wishlist_copy', 'status', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'library_wishlist.copy': {
            'Meta': {'object_name': 'Copy'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'copies'", 'null': 'True', 'to': u"orm['library_wishlist.Item']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'library_wishlist.item': {
            'Meta': {'object_name': 'Item'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['library_wishlist']