from django.shortcuts import render
from .models import Bouquet
from cart.models import Cart
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


def index(request):
    bouquets = Bouquet.objects.all()
    query = request.GET.get('q')
    if query:
        query_lower = query.lower()
        type_mapping = {
            'бумага': 'paper',
            'коробка': 'box',
        }
        q_objects = Q()
        q_objects |= Q(name__iregex=query)
        q_objects |= Q(description__iregex=query)
        q_objects |= Q(flowers_sort__iregex=query)
        for ru_term, db_value in type_mapping.items():
            if ru_term in query_lower:
                q_objects |= Q(bouquet_type=db_value)
                break
        
        bouquets = bouquets.filter(q_objects)
    packaging = request.GET.get('packaging')
    if packaging and packaging != 'all':
        bouquets = bouquets.filter(bouquet_type=packaging)
    sort = request.GET.get('sort', 'default')
    if sort == 'price_asc':
        bouquets = bouquets.order_by('price')
    elif sort == 'price_desc':
        bouquets = bouquets.order_by('-price')
    cart_quantities = {}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            for bouquet in bouquets:
                cart_quantities[bouquet.id] = cart.get_item_quantity(bouquet.id)
        except Cart.DoesNotExist:
            pass
    context = {
        'bouquets': bouquets,
        'cart_quantities': cart_quantities,
        'search_query': query,
        'current_sort': sort,
    }
    return render(request, 'main/catalog_flow.html', context)

def description(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart_quantities = {}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Можно получить количество для текущего букета
            cart_quantities[bouquet.id] = cart.get_item_quantity(bouquet.id)
        except Cart.DoesNotExist:
            pass
    context = {
        'bouquet': bouquet,
        'cart_quantities': cart_quantities,
    }
    return render(request, 'main/description.html', context)

