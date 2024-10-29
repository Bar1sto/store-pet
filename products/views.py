from lib2to3.fixes.fix_input import context
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from products.models import ProductCategory, Product, Basket
from django.core.paginator import Paginator
from users.models import User


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        return context


class ProdictsListView(ListView):
    model = Product
    template_name = 'products/products.html'

    paginate_by = 3

    def get_queryset(self):
        queryset = super(ProdictsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self,*, object_list=None,**kwargs):
        context = super(ProdictsListView,self).get_context_data()
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#         }
#     return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    
    
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(requeest, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(requeest.META['HTTP_REFERER'])