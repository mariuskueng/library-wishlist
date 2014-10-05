from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.db.models import Q
import json

from parser import search_catalog
from library_wishlist.models import Item, Branch

class IndexView(TemplateView):
    template_name = "library_wishlist/item_list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(completed=False) # status=True,
        context['branches'] = Branch.objects.all()
        return context


class BranchView(TemplateView):
    template_name = "library_wishlist/item_list.html"

    def get_context_data(self, **kwargs):
        currentBranch = Branch.objects.get(slug=kwargs['slug'])

        context = super(BranchView, self).get_context_data(**kwargs)
        context['currentBranch'] = currentBranch
        context['items'] = []

        itemQuerySet = Item.objects.filter(completed=False, copies__branch=currentBranch, copies__status=True)
        for item in itemQuerySet:
            if item not in context['items']:
                context['items'].append(item)

        context['branches'] = Branch.objects.all()
        return context


def createItem(request):
    if request.POST:
        text = text=request.POST['text']
        searchItem = search_catalog(text)
        if searchItem:
            if isinstance(searchItem, list):
                return HttpResponse(json.dumps(searchItem), content_type="application/json")
            else:
                item = Item(
                    text=text
                )
                item.save()
                item.createCopies(searchItem)

                response = render_to_string('library_wishlist/item.html', {'i': item})
                return HttpResponse(response, content_type="text/html")
        else:
            raise Http404
    else:
        raise Http404


def createSearchResultItem(request):
    if request.is_ajax:
        if request.method == "POST":

            json_str = request.body.decode(encoding='UTF-8')
            searchItem = json.loads(json_str)
            searchIndex = searchItem.get("index")
            searchItem = searchItem.get("item")

            item = Item(
                text=searchItem.get("name"),
                searchIndex=searchIndex
            )
            item.save()
            item.createCopies(searchItem)

            response = render_to_string('library_wishlist/item.html', {'i': item})
            return HttpResponse(response, content_type="text/html")
        else:
            raise Http404
    else:
        raise Http404


def completeItem(request, **kwargs):
    item = Item.objects.get(id=kwargs['id'])
    if request.POST:
        item.completed = request.POST['completed']
        item.save()
        return HttpResponse('OK.', content_type="text/plain")
    else:
        response = render_to_string('library_wishlist/item.html', {'i': item})
        return HttpResponse(response, content_type="text/plain")
