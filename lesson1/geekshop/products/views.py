# import json

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from geekshop.views import getFileData

from basketapp.views import get_total

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def get_other_products():
#     with open('other_products.json') as data_file:
#         data = json.load(data_file)
#
#     return data

def get_basket(user):
    if user.is_authenticated:
        return user.basket.all()
    else:
        return []


def get_hot_product():
    return Product.objects.filter(is_active=True).order_by('?').first()


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category, is_active=True). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


def get_catalog_menu():
    return ProductCategory.objects.filter(is_active=True)


def products(request, pk=None, page=1):
    title = 'продукты'
    menu_items = getFileData('menu_items.json')
    page_size = 3

    basket = get_total(request)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все'}
            products = Product.objects.filter(is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            title += ' : ' + category.name.title()
            products = Product.objects.filter(category__pk=pk, is_active=True).order_by('price')

        paginator = Paginator(products, page_size)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'catalog_menu': get_catalog_menu(),
            'menu_items': menu_items,
            'category': category,
            'products': products_paginator,
            'basket': basket
        }

        return render(request, 'products/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'catalog_menu': get_catalog_menu(),
        'menu_items': menu_items,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'products/products.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = get_total(request)
    menu_items = getFileData('menu_items.json')

    content = {
        'title': product.name,
        'catalog_menu': get_catalog_menu(),
        'product': product,
        'basket': basket,
        'menu_items': menu_items,
    }

    return render(request, 'products/product.html', content)
