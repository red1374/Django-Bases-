import json

from django.shortcuts import render
from geekshop.views import getFileData
from .models import ProductCategory, Product


def getOtherProducts():
    with open('other_products.json') as data_file:
        data = json.load(data_file)

    return data


def products(request, pk=None):
    print(pk)

    content = {
        'title': 'продукты',
        'links_menu': ProductCategory.objects.all(),
        'menu_items': getFileData('menu_items.json'),
        # 'other_products': getOtherProducts()
        'other_products': Product.objects.all()[:3]
    }
    return render(request, 'products.html', context=content)
