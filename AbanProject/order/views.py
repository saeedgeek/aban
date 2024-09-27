# order/views.py
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BuySymbolSerializer, SuccessResponseSerializer, ErrorResponseSerializer, UserCryptoSerializer
from .validators import validate_symbol, validate_order_id, validate_user_exists, validate_user_balance
from .redis_manager import RedisManager
from .models import User, UserCrypto, Order

# Import symbol prices from validators
from .validators import SYMBOL_PRICES


class BuySymbolView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BuySymbolSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['orderId']
            user_id = serializer.validated_data['user_id']
            symbol_name = serializer.validated_data['symbol_name']
            amount = serializer.validated_data['amount']

            try:
                # Run validations
                validate_symbol(symbol_name)
                validate_order_id(order_id)
                validate_user_exists(user_id)

                # Get the price per unit for the symbol
                price_per_unit = SYMBOL_PRICES[symbol_name]

                # Calculate total cost
                total_cost = amount * price_per_unit

                # Get user instance
                user = User.objects.get(pk=user_id)

                # Validate user's balance
                validate_user_balance(user, total_cost)

                # Deduct the total cost from user's balance
                user.balance -= total_cost
                user.save()

                # Update or create UserCrypto entry
                user_crypto, created = UserCrypto.objects.get_or_create(
                    user=user,
                    symbol_name=symbol_name,
                    defaults={'amount': amount}
                )
                if not created:
                    user_crypto.amount += amount
                    user_crypto.save()

                # Create the order entry
                order = Order(
                    orderId=order_id,
                    user=user,
                    symbol_name=symbol_name,
                    amount=amount,
                    order_type='buy'
                )
                order.save()

                RedisManager().save_sell_order(symbol_name, amount)

                success_serializer = SuccessResponseSerializer({
                    'message': f"{order.order_type.capitalize()}ed {amount} of {symbol_name} for order {order_id}",
                    'user_crypto': UserCryptoSerializer(user_crypto).data
                })
                return Response(success_serializer.data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                error_serializer = ErrorResponseSerializer({'error': str(e)})
                return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
