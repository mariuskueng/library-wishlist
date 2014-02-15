from django.contrib import admin
from library_wishlist.models import Item, Copy, Branch
from parser import search_catalog

class BranchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CopyInline(admin.TabularInline):
    model = Copy
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    list_display = [ 'text', 'name', 'author', 'completed', 'status', 'created']
    list_filter = ['completed', 'status', 'copies__branch']
    inlines = [
            CopyInline
        ]

    def save_model(self, request, obj, form, change):
        obj.updateCopies()

admin.site.register(Item, ItemAdmin)
admin.site.register(Branch, BranchAdmin)
