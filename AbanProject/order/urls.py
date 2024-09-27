from django.urls import path
from .views import BuySymbolView

urlpatterns = [
    path('buy/', BuySymbolView.as_view(), name='buy_symbol'),
]
