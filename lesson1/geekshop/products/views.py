import json

from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from geekshop.views import getFileData

from basketapp.views import get_total


def getOtherProducts():
    with open('other_products.json') as data_file:
        data = json.load(data_file)

    return data


def products(request, pk=None):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    menu_items = getFileData('menu_items.json')

    basket = get_total(request)

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
            'links_menu': links_menu,
            'menu_items': menu_items,
            'category': category,
            'products': products,
            'basket': basket
        }

        return render(request, 'products_list.html', content)

    same_products = Product.objects.all()[3:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'menu_items': menu_items,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'products.html', content)
