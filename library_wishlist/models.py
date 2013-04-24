from django.db import models
from django.conf import settings


class Item(models.Model):
    name = models.CharField('Name', max_length=200)
    author = models.CharField('Autor', max_length=200)

    def __unicode__(self):
        return self.name


class Copy(models.Model):
    item = models.ForeignKey('Item', null=True, related_name='copies')
    branch = models.IntegerField('Zweigstelle', choices=settings.BRANCHES)
    status = models.IntegerField('Status', choices=settings.STATES)
