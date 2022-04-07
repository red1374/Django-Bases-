from geekshop.utils import get_price_format, get_file_data


def top_menu(request):
    return {
        'menu_items': get_file_data('menu_items.json')
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
