from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from library_wishlist.api import ItemResource

item_resource = ItemResource()

from library_wishlist.views import IndexView, BranchView, createItem, completeItem

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(item_resource.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^branches/(?P<slug>[-\w]+)/$',  BranchView.as_view(), name="branch_view"),
    url(r'^item/$', createItem, name='new_item'),
    url(r'^item/(?P<id>[0-9]+)/', completeItem, name='edit_item'),
)
