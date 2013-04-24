from django.contrib import admin
from library_wishlist.models import Item, Copy


class CopyInline(admin.TabularInline):
    model = Copy
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    inlines = [
            CopyInline
        ]

admin.site.register(Item, ItemAdmin)
