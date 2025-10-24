from django.contrib import admin
from .models import Bouquet

@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'bouquet_type', 'flowers_sort')
    list_filter = ('bouquet_type', 'flowers_sort')
    search_fields = ('name', 'flowers_sort')