from django.shortcuts import render
from .models import Stocks
from django.views.generic import DetailView


def discount_home(request):
    discount=Stocks.objects.order_by('-date')
    return render(request,'discount/discount_home.html',{'discount':discount})


class DiscountDetailView(DetailView):
    model=Stocks
    template_name='discount/details_view.html'
    context_object_name='discount'