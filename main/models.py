from django.db import models

class Bouquet(models.Model):
    TYPE_CHOICES = [
        ('box', 'В коробке'),
        ('paper', 'В бумаге'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название букета")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    bouquet_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='paper', verbose_name="Тип упаковки")
    flowers_sort = models.CharField(max_length=255, verbose_name="Сорт цветов", default='')
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='bouquets/', blank=False, null=False, verbose_name="Изображение")

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return self.name
