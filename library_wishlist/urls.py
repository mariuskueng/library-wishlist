from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from library_wishlist.api import EntryResource

entry_resource = EntryResource()

from library_wishlist.views import ItemListView

urlpatterns = patterns('',
    url(r'^$', ItemListView.as_view(), name='home'),
    # url(r'^library_wishlist/', include('library_wishlist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(entry_resource.urls)),
)
