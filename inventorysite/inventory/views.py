from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect


from .models import Item, Category

def increment(request, item_id):
    p = get_object_or_404(Item, pk=item_id)
    p.increment()
    p.save()
    return HttpResponseRedirect(reverse('inventory:categorydetail', args=(p.category_id,)))

def results(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'inventory:categorydetail', item.category.id)


class AjaxableResponseMixin(object):

    def form_invalid(self,form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self,form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = model_to_dict(self.object)
            return JsonResponse(data)
        else:
            return response


# CATEGORY VIEWS
class CategoryListView(ListView):
    model = Category
    template_name = "inventory/category_list.html"

class CategoryDetailView(DetailView):
    model = Category


class CreateCategoryView(CreateView):
    model = Category
    fields = ['parent', 'name', 'description']

    def get_success_url(self):
        return reverse('inventory:categorydetail', args=(self.object.pk,))


class UpdateCategoryView(UpdateView):
    model = Category
    fields = ['parent', 'name', 'description']
    success_url = reverse_lazy('inventory:categorylist')


class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('inventory:deletesuccess')


# ITEM VIEWS
class ItemListView(ListView):
    model = Item


class CreateItemView(CreateView):
    model = Item
    fields = ['name', 'quantity', 'sku', 'category']
    template_name = 'inventory/add_item.html'

    def get_success_url(self):

        return reverse('inventory:categorydetail', args=(self.object.category.pk,))


class UpdateItemView(AjaxableResponseMixin, UpdateView):
    model = Item
    fields = ['name', 'quantity', 'sku', 'category']


    def get_success_url(self):
        return reverse('inventory:categorylist')

class DeleteItemView(DeleteView):
    model = Item
    success_url = reverse_lazy('inventory:deletesuccess')

