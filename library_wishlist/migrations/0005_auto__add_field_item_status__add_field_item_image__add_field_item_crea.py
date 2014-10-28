# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Item.status'
        db.add_column(u'library_wishlist_item', 'status',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Item.image'
        db.add_column(u'library_wishlist_item', 'image',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Item.created'
        db.add_column(u'library_wishlist_item', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Item.status'
        db.delete_column(u'library_wishlist_item', 'status')

        # Deleting field 'Item.image'
        db.delete_column(u'library_wishlist_item', 'image')

        # Deleting field 'Item.created'
        db.delete_column(u'library_wishlist_item', 'created')


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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 2, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['library_wishlist']
