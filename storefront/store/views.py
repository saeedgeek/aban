from django.shortcuts import render
from .models import *
from django.db.models import Max, Min, Avg, Count, Sum, F, Value


# Create your views here.

def ShowProduct(request):
    res = Product.objects.annotate(
        totalAmount=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))
    ).order_by('-totalAmount').values('title', 'totalAmount')[:5]
    return render(request, 'hello.html', {'count': res})
