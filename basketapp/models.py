from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from products.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @cached_property
    def get_item_cached(self):
        return self.user.basket.select_related()

    def get_item_total(self):
        """
        Get basket item total cost
        :return: item cost
        """
        return self.quantity * self.product.price

    @property
    def total(self):
        """
        return total quantity for user
        :return:
        """
        _items = self.get_item_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        """
        return total cost for user
        :return:
        """
        _items = self.get_item_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def save(self, *args, **kwargs):
        if self.pk:
            # New basket item value minus stored (old) value. Get difference to decrease product quantity
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)
