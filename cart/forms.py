from django import forms
from .models import CartItem
import re
from django.core.exceptions import ValidationError
from .models import Order, OrderItem
from django.forms.models import inlineformset_factory


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
    )

class CartUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'})
        }

class OrderForm(forms.Form):
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}), label='Адрес доставки')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}), label='Номер телефона')
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Комментарий к заказу (необязательно)'}), required=False, label='Комментарий')
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        pattern = re.compile(r'^\+?\d{10,15}$')
        if not pattern.match(phone):
            raise ValidationError("Номер телефона должен содержать от 10 до 15 цифр, возможно с + в начале.")
        return phone

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('bouquet', 'quantity', 'price_per_item'), extra=1, can_delete=True)