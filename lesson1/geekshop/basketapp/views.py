from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from django.urls import reverse
from products.models import Product

from geekshop.views import getFileData

from geekshop.utils import is_ajax


@login_required
def basket(request):
    title = 'корзина'
    basket_items = request.user.basket.order_by('product__category')
    menu_items = getFileData('menu_items.json')

    content = {
        'title': title,
        'menu_items': menu_items,
        'basket_items': basket_items,
        'total': get_total(request)
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, pk=None):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('basket:view'))

    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_total(request):
    basket = []
    qty = 0
    sum = 0
    if request.user.is_authenticated:
        basket = request.user.basket.all()

    for item in basket:
        qty += item.quantity
        sum += item.get_item_total()

    return {
        'qty': qty,
        'sum': int(sum)
    }


@login_required
def edit(request, pk, quantity):
    # request.is_ajax()
    if is_ajax(request):
        quantity = int(quantity)
        basket_item = Basket.objects.filter(pk=int(pk)).first()
        cost = 0

        if basket_item is None:
            return JsonResponse({
                'status': 'error',
                'basket_item': {
                    'id': int(pk),
                    'cost': cost
                },
            })

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
            cost = int(basket_item.get_item_total())
        else:
            basket_item.delete()

        result = {
            'basket_item': {
                'id': int(pk),
                'cost': cost
            },
            'itog': get_total(request),
        }

        # result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse(result)
