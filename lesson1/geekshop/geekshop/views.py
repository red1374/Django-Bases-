import json

from django.shortcuts import render
from products.models import TestModel
from datetime import datetime

from products.models import Product


def getFileData(file_name=''):
    if not file_name:
        return False

    with open(file_name) as data_file:
        data = json.load(data_file)

    return data


def index(request):
    new_products = Product.objects.order_by('?')[2:6]
    content = {
        'title': 'главная',
        'new_products': new_products,
        'menu_items': getFileData('menu_items.json')
    }
    return render(request, 'index.html', context=content)


def contacts(request):
    content = {
        'title': 'контакты',
        'menu_items': getFileData('menu_items.json')
    }
    return render(request, 'contacts.html', context=content)


def uploadToBase(request):
    categories = getFileData('new_product_sections.json')
    for item in categories:
        name = item['name'] + ' (' + str(datetime.now()) + ')'
        category = TestModel(name=name, description=item['description'])
        category.save()

    content = {
        'added': len(categories),
        'total': TestModel.objects.count()
    }
    return render(request, 'upload.html', context=content)
