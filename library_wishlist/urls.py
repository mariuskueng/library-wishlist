import os
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from library_wishlist.views import IndexView, BranchView,\
        createItem, completeItem, createSearchResultItem

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login, name='login_view'),
    url(r'^logout/$', auth_views.logout, name='logout_view'),
    url('^register/', CreateView.as_view(
                template_name='registration/register.html',
                form_class=UserCreationForm,
                success_url='/'
        ), name='registration_view'),
    url(r'^branches/(?P<slug>[-\w]+)/$',  BranchView.as_view(), name="branch_view"),
    url(r'^item/$', createItem, name='new_item'),
    url(r'^item/(?P<id>[0-9]+)/', completeItem, name='edit_item'),
    url(r'^itemSearchResult/$', createSearchResultItem, name='new_search_item'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/')}),
)
