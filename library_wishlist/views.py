from django.views.generic import ListView
from library_wishlist.models import Item


class ItemListView(ListView):
    model = Item
