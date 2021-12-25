import os
import json

from django.core.management.base import BaseCommand
from collections import defaultdict

from products.models import ProductCategory, Product
from authapp.models import ShopUser

JSON_PATH = 'geekshop\json'


def load_from_json(file_name):
    path_to_file = os.path.join(JSON_PATH, file_name + '.json')
    with open(path_to_file, 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        if not categories:
            print('Empty "categories.json" file!')
            return False

        ProductCategory.objects.all().delete()

        new_categories = defaultdict()
        for category in categories:
            new_category = ProductCategory.objects.create(**category)
            new_categories[category['name']] = new_category

        products = load_from_json('products')
        if not products:
            print('Empty "products.json" file!')
            return False

        Product.objects.all().delete()
        for product in products:
            if not new_categories[product["category"]]:
                continue

            product['category'] = new_categories[product["category"]]
            Product.objects.create(**product)

        # Создаем суперпользователя при помощи менеджера модели
        if not ShopUser.objects.filter(username='django'):
            ShopUser.objects.create_superuser('django', 'support@pleshakov.org', 'geekbrains', age=37)
