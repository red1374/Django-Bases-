from django.shortcuts import render
from products.models import TestModel
from datetime import datetime

from products.models import Product

from geekshop.utils import get_file_data


def index(request):
    new_products = Product.objects.order_by('?')[2:6]
    content = {
        'title': 'главная',
        'new_products': new_products,
    }
    return render(request, 'index.html', context=content)


def contacts(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'contacts.html', context=content)


def upload_to_base(request):
    categories = get_file_data('new_product_sections.json')
    for item in categories:
        name = item['name'] + ' (' + str(datetime.now()) + ')'
        category = TestModel(name=name, description=item['description'])
        category.save()

    content = {
        'added': len(categories),
        'total': TestModel.objects.count()
    }
    return render(request, 'upload.html', context=content)
