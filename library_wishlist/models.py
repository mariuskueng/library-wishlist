# coding=utf-8
from django.db import models
from django.utils.timezone import now
from parser import search_catalog


class Item(models.Model):
    text = models.CharField('Text', max_length=200)
    name = models.CharField('Name', max_length=200, blank=True)
    author = models.CharField('Autor', max_length=200, blank=True)
    status = models.BooleanField('Status', default=False, blank=True)
    image = models.URLField('Bild', blank=True)
    created = models.DateTimeField('Hinzugefügt', blank=True, default=now())
    completed = models.BooleanField('Completed', default=False, blank=True)
    searchIndex = models.IntegerField('Suchindex', default=0, blank=True)

    class Meta:
        ordering = ['-status','-created']
        verbose_name = 'Medium'
        verbose_name_plural = 'Medien'

    def __unicode__(self):
        return self.text


    def createCopies(self, item={}):
        if not item:
            return

        if isinstance(item, list):
            item = item[self.searchIndex]
            if item['item']['author']:
                self.author = item['item']['author']
            if item['item']['name']:
                self.name = item['item']['name']
            self.status = item['item']['status']
            self.image = item['item']['image']
            self.searchIndex = item['index']
        else:
            if item['author']:
                self.author = item['author']
            if item['name']:
                self.name = item['name']
            self.status = item['status']
            self.image = item['image']

        existingCopies = Copy.objects.filter(item=self)

        if item['copies']:
            for i, c in enumerate(item['copies']):
                if existingCopies:
                    existingCopies[i].branch = Branch.objects.get(name=c['branch'])
                    existingCopies[i].status = c['status']
                    existingCopies[i].location = c['location']
                    existingCopies[i].save()
                else:
                    copy = Copy(
                        item = self,
                        branch = Branch.objects.get(name=c['branch']),
                        status = c.get('status'),
                        location = c['location']
                    )
                    copy.save()

        self.setItemStatus()

        self.save()

    def setItemStatus(self):
        self.status = False
        for c in self.copies.all():
            if c.status == True:
                self.status = True

    def updateCopies(self):
        catalogItem = search_catalog(self.text)
        self.createCopies(catalogItem)
        self.save()


class Copy(models.Model):
    item = models.ForeignKey('Item', null=True, related_name='copies')
    branch = models.ForeignKey('Branch', null=True, blank=True, related_name='branches')
    status = models.BooleanField('Status', default=False)
    location = models.CharField('Standort', max_length=200, blank=True)
    # signature = models.CharField('Zweigstelle', max_length=200)
    # return_date = models.DateTimeField(u'Rückgabedatum', null=True, blank=True)


    def __unicode__(self):
        return 'Exemplar'


class Branch(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('Slug', unique=True, null=True, blank=True)
    adress = models.TextField('Adresse')
    opening_hours = models.TextField('Öffnungszeiten')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Zweigstelle'
        verbose_name_plural = 'Zweigstellen'
