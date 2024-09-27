# order/models.py
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UserCrypto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cryptos')
    symbol_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} of {self.symbol_name} owned by {self.user.username}"


class Order(models.Model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    orderId = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    symbol_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['orderId']),
        ]

    def __str__(self):
        return f"Order {self.orderId} - {self.order_type}"
