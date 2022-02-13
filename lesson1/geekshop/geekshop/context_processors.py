from geekshop.utils import get_price_formated


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
            'sum': get_price_formated(int(sum))
        }
    }
