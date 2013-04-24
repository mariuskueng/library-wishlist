from tastypie.resources import ModelResource
from library_wishlist.models import Item, Copy


class EntryResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'entry'
