# import json

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from geekshop.views import getFileData

from basketapp.views import get_total


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
    return Product.objects.order_by('?').first()


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


def products(request, pk=None):
    title = 'продукты'
    catalog_menu = ProductCategory.objects.all()
    menu_items = getFileData('menu_items.json')

    basket = get_total(request)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            title += ' : ' + category.name.title()
            products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'catalog_menu': catalog_menu,
            'menu_items': menu_items,
            'category': category,
            'products': products,
            'basket': basket
        }

        return render(request, 'products/products_list.html', content)

    content = {
        'title': title,
        'catalog_menu': catalog_menu,
        'menu_items': menu_items,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'products/products.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    catalog_menu = ProductCategory.objects.all()
    basket = get_total(request)
    menu_items = getFileData('menu_items.json')

    content = {
        'title': product.name,
        'catalog_menu': catalog_menu,
        'product': product,
        'basket': basket,
        'menu_items': menu_items,
    }

    return render(request, 'products/product.html', content)
