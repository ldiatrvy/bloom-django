from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Bouquet
from .forms import CartUpdateForm, OrderForm
from discount.models import Stocks
from django.http import JsonResponse  
from decimal import Decimal
from .models import Cart, Order, OrderItem
from decimal import Decimal
from .forms import OrderForm


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    discount_percent = Decimal(str(request.session.get('discount_percent', 0)))
    discount_amount = (cart.total_price() * discount_percent) / 100
    total_price_with_discount = cart.total_price() - discount_amount

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            final_price = total_price_with_discount
            delivery_address = form.cleaned_data['delivery_address']
            phone_number = form.cleaned_data['phone_number']
            comment_value = form.cleaned_data.get('comment') or 'Отсутствует'

            order = Order.objects.create(
                user=request.user,
                total_price=final_price,
                delivery_address=delivery_address,
                phone_number=phone_number,
                comment=comment_value,
                status='processing',
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    bouquet=item.bouquet,
                    quantity=item.quantity,
                    price_per_item=item.bouquet.price,
                )
            cart.items.all().delete()

            request.session['discount_percent'] = 0
            request.session['promo_code'] = ''
            request.session['discount_error'] = ''

            return redirect('/register/profile/')

    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total_price_with_discount': total_price_with_discount,
        'promo_code': request.session.get('promo_code', ''),
        'discount_error': request.session.get('discount_error', ''),
        'form': form,
    }
    
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_add(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, id=bouquet_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        bouquet=bouquet,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        message = f'Количество "{bouquet.name}" увеличено в корзине'
    else:
        message = f'"{bouquet.name}" добавлен в корзину'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': message, 'quantity': cart_item.quantity})

    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'main'))


@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        form = CartUpdateForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Корзина обновлена')
            return redirect('cart_detail')
    
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, bouquet_id):
    try:
        cart_item = CartItem.objects.get(bouquet_id=bouquet_id, cart__user=request.user)
        bouquet_name = cart_item.bouquet.name
        cart_item.delete()
        messages.success(request, f'"{bouquet_name}" удален из корзины')
    except CartItem.DoesNotExist:
        messages.error(request, 'Элемент корзины не найден')
    
    return redirect('cart:cart_detail')

@login_required
def cart_clear(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Корзина очищена')
    return redirect('cart:cart_detail')

@login_required
def cart_decrease(request, bouquet_id):
    """Уменьшить количество товара в корзине на 1"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, bouquet_id=bouquet_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f'Количество "{cart_item.bouquet.name}" уменьшено')
        else:
            bouquet_name = cart_item.bouquet.name
            cart_item.delete()
            messages.success(request, f'"{bouquet_name}" удален из корзины')
            
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, 'Товар не найден в корзине')
    
    return redirect(request.META.get('HTTP_REFERER', 'main'))


@login_required
def apply_discount(request):
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code', '').strip()
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_price = cart.total_price()

        try:
            stock = Stocks.objects.get(promo=promo_code)
            valid, msg = stock.check_conditions(request.user, total_price)
            if valid:
                request.session['discount_percent'] = float(stock.discount_percent)
                request.session['promo_code'] = promo_code
                request.session['discount_error'] = ''
                messages.success(request, f'Промокод "{promo_code}" применён. Скидка {stock.discount_percent}%')
            else:
                request.session['discount_percent'] = 0
                request.session['promo_code'] = ''
                request.session['discount_error'] = msg
                messages.error(request, msg)
        except Stocks.DoesNotExist:
            request.session['discount_percent'] = 0
            request.session['promo_code'] = ''
            request.session['discount_error'] = 'Промокод не найден.'
            messages.error(request, 'Промокод не найден.')

        return redirect('cart:cart_detail')