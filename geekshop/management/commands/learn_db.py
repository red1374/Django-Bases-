from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from ordersapp.models import OrderItem
from geekshop.utils import get_price_format
from products.models import Product


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


class Command(BaseCommand):
    def handle(self, *args, **options):
        # test_products = Product.objects.filter(
        #     Q(category__name='офис') |
        #     Q(category__name='модерн')
        # )
        # print(len(test_products))
        # # print(test_products)
        # db_profile_by_type('learn db', '', connection.queries)

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        DISCOUNTS = {
            1: 0.3,
            2: 0.15,
            3: 0.05
        }
        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)
        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)
        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition, then=F('product__price') * F('quantity') * DISCOUNTS[1])
        action_2__price = When(action_2__condition, then=F('product__price') * F('quantity') * DISCOUNTS[2])
        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * DISCOUNTS[3])

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        print(f'{"Тип":3} | {"Заказ":5} | {"Наименование товара":24} | {"Скидка":20} | {"Даты созд. / обновления"}')
        for orderitem in test_orders:
            price = f'{get_price_format(orderitem.total_price)} руб.'
            discount = f'{DISCOUNTS[orderitem.action_order] * 100}'
            print(f'{orderitem.action_order:3} | {orderitem.order.pk:5} | '
                  f'{orderitem.product.name:24} | {discount:3}% - '
                  f'{price:12} | '
                  f'{orderitem.order.updated.strftime("%Y-%m-%d")} - {orderitem.order.created.strftime("%Y-%m-%d")}')
