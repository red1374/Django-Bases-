from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from products.models import Product
from .models import Order, OrderItem

from .forms import OrderItemForm
from geekshop.utils import is_ajax


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = self.request.user.basket.all()
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                # Empty current basket
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # Remove empty order
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['summ'] = form.instance.get_product_cost()
        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:orders_list')


class OrderRead(DetailView):
    model = Order
    extra_context = {'title': 'заказ/просмотр'}


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))


# @receiver(pre_save, sender=OrderItem)
# @receiver(pre_save, sender=Basket)
# def product_quantity_update_save(sender, update_fields, instance, **kwargs):
#     if update_fields is 'quantity' or 'product':
#         if instance.pk:
#             instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
#         else:
#             instance.product.quantity -= instance.quantity
#         instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    product_id = int(pk)
    result = {
        'status': 'error',
        'product_id': product_id,
        'price': 0,
    }

    if is_ajax(request) and product_id > 0:
        product_item = Product.objects.filter(pk=pk).first()

        if product_item is None:
            return JsonResponse(result)

        result['price'] = product_item.price
        result['status'] = 'success'

    return JsonResponse(result)
