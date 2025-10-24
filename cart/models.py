from django.db import models
from django.contrib.auth.models import User
from main.models import Bouquet


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f"Корзина {self.user.username}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_item_quantity(self, bouquet_id):
        try:
            item = self.items.get(bouquet_id=bouquet_id)
            return item.quantity
        except CartItem.DoesNotExist:
            return 0
        
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name='Букет')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name}"
    
    def total_price(self):
        return self.quantity * self.bouquet.price
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'bouquet']

class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    comment = models.TextField(verbose_name='Комментарий', default='Отсутствует',blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return f"Заказ #{self.id} пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name='Букет')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')

    def __str__(self):
        return f"{self.quantity} x {self.bouquet.name} (Заказ #{self.order.id})"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

