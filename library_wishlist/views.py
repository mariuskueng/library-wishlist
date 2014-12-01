from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth.models import User
import json

from parser import search_catalog
from library_wishlist.models import Item, Branch

class IndexView(TemplateView):
    template_name = "library_wishlist/item_list.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            context['user_id'] = self.request.user.id
            context['username'] = self.request.user.username
            context['branches'] = Branch.objects.all()
            context['items'] = Item.objects.filter(completed=False, user=self.request.user)

        return context


class BranchView(TemplateView):
    template_name = "library_wishlist/item_list.html"

    def get_context_data(self, **kwargs):

        context = super(BranchView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            currentBranch = Branch.objects.get(slug=kwargs['slug'])
            context['currentBranch'] = currentBranch
            context['username'] = self.request.user.username
            context['items'] = []

            itemQuerySet = Item.objects.filter(
                                completed=False,
                                copies__branch=currentBranch,
                                copies__status=True,
                                user=self.request.user
                            )
            # show items only once which are in more than one branch
            for item in itemQuerySet:
                if item not in context['items']:
                    context['items'].append(item)

            context['branches'] = Branch.objects.all()

        return context


def createItem(request):

    if request.user.is_authenticated():
        if request.POST:
            text = text=request.POST['text']
            searchItem = search_catalog(text)
            user_id = int(request.POST['user_id'])

            if searchItem:

                for item in searchItem:
                    item['user_id'] = user_id

                if isinstance(searchItem, list):
                    return HttpResponse(json.dumps(searchItem), content_type="application/json")
                else:
                    item = Item(
                        text=text,
                        user=User.objects.get(id=user_id)
                    )
                    item.save()
                    item.createCopies(searchItem)

                    response = render_to_string('library_wishlist/item.html', {'i': item})
                    return HttpResponse(response, content_type="text/html")
            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def createSearchResultItem(request):

    if request.user.is_authenticated():
        if request.is_ajax and request.method == "POST":
            json_str = request.body.decode(encoding='UTF-8')
            data = json.loads(json_str)

            searchItem = data.get("item")
            searchIndex = data.get("index")
            user_id = int(data.get("user_id"))

            item = Item(
                text=searchItem.get("name"),
                user=User.objects.get(id=user_id),
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

    if request.user.is_authenticated():

        if request.POST:
            if item.user.id == request.user.id:
                item.completed = request.POST['completed']
                item.save()
                return HttpResponse('OK.', content_type="text/plain")
            else:
                raise Http404
        else:
            response = render_to_string('library_wishlist/item.html', {'i': item})
            return HttpResponse(response, content_type="text/plain")
