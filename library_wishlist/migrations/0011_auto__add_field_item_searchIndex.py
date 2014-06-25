# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.searchIndex'
        db.add_column(u'library_wishlist_item', 'searchIndex',
                      self.gf('django.db.models.fields.IntegerField')(default=-1, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.searchIndex'
        db.delete_column(u'library_wishlist_item', 'searchIndex')


    models = {
        u'library_wishlist.branch': {
            'Meta': {'object_name': 'Branch'},
            'adress': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'opening_hours': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'library_wishlist.copy': {
            'Meta': {'object_name': 'Copy'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'branches'", 'null': 'True', 'to': u"orm['library_wishlist.Branch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'copies'", 'null': 'True', 'to': u"orm['library_wishlist.Item']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'library_wishlist.item': {
            'Meta': {'ordering': "['-status', '-created']", 'object_name': 'Item'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 25, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'searchIndex': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['library_wishlist']