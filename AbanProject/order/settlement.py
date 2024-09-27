# order/settlement.py

from decimal import Decimal
from .models import Order, UserCrypto, User
from .validators import SYMBOL_PRICES


class GlobalBroker:
    def __init__(self, settlement_threshold=100):
        self.settlement_threshold = Decimal(settlement_threshold)

    def process_settlement(self, orders, total_value):
        for order_tuple in orders:
            user_id, amount, order_id = eval(order_tuple)
            order = Order.objects.get(orderId=order_id)
            user_crypto = UserCrypto.objects.get(user=order.user, symbol_name=order.symbol_name)

            if user_crypto.amount >= Decimal(amount):
                user_crypto.amount -= Decimal(amount)
                user_crypto.save()

                # Add the value to the user's balance
                order.user.balance += Decimal(amount) * SYMBOL_PRICES[order.symbol_name]
                order.user.save()

                # Mark the order as settled
                order.settled = True
                order.save()

                print(f"Settled order ID: {order.orderId} for user: {order.user.username}")

        print(f"Total settled value for symbol {order.symbol_name}: ${total_value}")
