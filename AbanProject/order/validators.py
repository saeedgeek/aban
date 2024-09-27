# order/validators.py

from rest_framework.exceptions import ValidationError
from .models import Order, User

# Define symbol prices
SYMBOL_PRICES = {
    'BTC': 30000.00,
    'ETH': 2000.00,
    'ABC': 5.00,
    # Add more symbols and their prices here
}


def validate_symbol(symbol_name):
    if symbol_name not in SYMBOL_PRICES:
        raise ValidationError("Invalid symbol name or price not found")


def validate_order_id(order_id):
    if Order.objects.filter(orderId=order_id).exists():
        raise ValidationError("Order ID already exists")


def validate_user_exists(user_id):
    if not User.objects.filter(pk=user_id).exists():
        raise ValidationError("User not found")


def validate_user_balance(user, total_cost):
    if user.balance < total_cost:
        raise ValidationError("Insufficient balance")
