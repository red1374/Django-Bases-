import json

from django.shortcuts import render


def getTopMenu():
    with open('menu_items.json') as data_file:
        data = json.load(data_file)

    return data


def index(request):
    content = {
        'title': 'главная',
        'menu_items': getTopMenu()
    }
    return render(request, 'index.html', context=content)


def contacts(request):
    content = {
        'title': 'контакты',
        'menu_items': getTopMenu()
    }
    return render(request, 'contacts.html', context=content)
