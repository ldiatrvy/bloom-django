from decimal import Decimal
from django.db import models
from django.utils import timezone


class Stocks(models.Model):
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Условия')
    promo = models.CharField('Промокод', max_length=10, unique=True)
    discount_percent = models.DecimalField('Процент скидки', max_digits=5, decimal_places=2, default=0)
    min_order_amount = models.DecimalField('Минимальная сумма заказа', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    first_order_only = models.BooleanField('Только для первого заказа', default=False)
    date = models.DateField('Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def is_active(self):
        """Проверка, что акция активна по дате"""
        return self.date <= timezone.now().date()
    
    def check_conditions(self, user, cart_total: Decimal):
        from cart.models import Order
        if not self.is_active():
            return False, "Промокод неактивен"
        if self.first_order_only:
            if Order.objects.filter(user=user).exists():
                return False, "Промокод действует только на первый заказ"
        if cart_total < self.min_order_amount:
            return False, f"Минимальная сумма заказа для применения промокода: {self.min_order_amount} ₽"
        return True, ""


