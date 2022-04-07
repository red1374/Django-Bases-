import json

from django.shortcuts import render

from geekshop.views import getTopMenu


def getOtherProducts():
    with open('other_products.json') as data_file:
        data = json.load(data_file)

    return data


def products(request):
    links_menu = [
        {'href': 'products/', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
        'menu_items': getTopMenu(),
        'other_products': getOtherProducts()
    }
    return render(request, 'products.html', context=content)
