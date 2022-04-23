# import json

from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.conf import settings
from django.core.cache import cache

from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache

from .models import ProductCategory, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_catalog_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_activ=True)


def get_hot_product():
    return Product.objects.filter(is_active=True).order_by('?').first()


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]

    return same_products


@method_decorator(cache_page(3600), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    ordering = ('price',)
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()

        if self.kwargs.get('pk') is None:
            return query_set

        if self.kwargs['pk'] == 0:
            return query_set.filter(is_active=True)
        else:
            return query_set.filter(category__pk=self.kwargs['pk'], is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category = None
        if self.kwargs.get('pk') is not None:
            category = ProductCategory.objects.filter(pk=self.kwargs['pk']).first()

        if category is None:
            category = ProductCategory(name='все', pk=0)

        context['title'] = 'продукты "'

        if self.kwargs.get('pk') is not None:
            context['title'] = 'продукты "' + category.name + '"'
            context['page_url'] = 'products:page'
            context['page_pk'] = self.kwargs['pk']
            self.template_name = 'products/products_list.html'
        else:
            context['hot_product'] = get_hot_product()
            context['same_products'] = get_same_products(context['hot_product'])

        context['category'] = category
        context['catalog_menu'] = get_catalog_menu()

        return context


class ProductView(DetailView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['title'] = self.object.name
        context['catalog_menu'] = get_catalog_menu()

        return context
