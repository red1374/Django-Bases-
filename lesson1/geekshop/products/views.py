# import json

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def get_other_products():
#     with open('other_products.json') as data_file:
#         data = json.load(data_file)
#
#     return data


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
    page_size = 3

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
            'category': category,
            'products': products_paginator,
        }

        return render(request, 'products/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'catalog_menu': get_catalog_menu(),
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'products/products.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    content = {
        'title': product.name,
        'catalog_menu': get_catalog_menu(),
        'product': product,
    }

    return render(request, 'products/product.html', content)
