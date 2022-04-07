from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from products.models import Product


def basket(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def add(request, pk=None):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    content = {}
    return render(request, 'basketapp/basket.html', content)


def get_total(request):
    basket = []
    qty = 0
    sum = 0
    if request.user.is_authenticated:
        basket = request.user.basket.all()

    for item in basket:
        total = item.get_item_total()
        qty += total['qty']
        sum += total['sum']

    return {
        'qty': qty,
        'sum': sum
    }
