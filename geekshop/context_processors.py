from geekshop.utils import get_price_format, get_file_data

import environ

env = environ.Env()
environ.Env.read_env()


def top_menu(request):
    menu_items = {}
    if env('DEBUG') == 'TRUE':
        menu_items = get_file_data('geekshop/json/menu_items.json')
    else:
        menu_items = get_file_data('geekshop/json/menu_items_prod.json')

    return {
        'menu_items': menu_items
    }


def basket(request):
    basket = []
    qty = 0
    sum = 0
    if request.user.is_authenticated:
        basket = request.user.basket.all()

    for item in basket:
        qty += item.quantity
        sum += item.get_item_total()

    return {
        'basket': {
            'qty': qty,
            'sum': get_price_format(int(sum))
        }
    }
