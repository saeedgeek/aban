# order/serializers.py
from rest_framework import serializers
from .models import User, UserCrypto, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'balance', 'created_at']


class UserCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCrypto
        fields = ['id', 'user', 'symbol_name', 'amount', 'acquired_at']


class BuySymbolSerializer(serializers.Serializer):
    orderId = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()
    symbol_name = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['orderId', 'user', 'symbol_name', 'amount', 'order_type', 'created_at']


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)
    user_crypto = UserCryptoSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=200)
