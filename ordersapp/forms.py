from django import forms
from .models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
       model = Order
       exclude = ('user',)

    def __init__(self, *args, **kwargs):
       super(OrderForm, self).__init__(*args, **kwargs)
       for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)
    summ = forms.CharField(label='сумма', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control field-' + field_name

        self.fields['product'].queryset = Product.objects.filter(quantity__gte=1)