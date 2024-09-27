# order/redis_manager.py

import redis
from django.conf import settings
from decimal import Decimal
from .validators import SYMBOL_PRICES

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


class RedisManager:
    def __init__(self):
        self.client = redis_client
        self.thresholds = {symbol: Decimal(100) / price for symbol, price in SYMBOL_PRICES.items()}

    def save_crypto_symbol(self, symbol_name, amount):
        key = f"crypto:{symbol_name}"
        new_amount = self.increase_amount(key, amount)

        if new_amount >= self.thresholds[symbol_name]:
            self.settle_orders(symbol_name, new_amount * SYMBOL_PRICES[symbol_name])

    def increase_amount(self, key, amount):
        while True:
            try:
                with self.client.pipeline() as pipe:
                    pipe.watch(key)
                    current_amount = Decimal(pipe.get(key) or 0)
                    new_amount = current_amount + Decimal(amount)
                    pipe.multi()
                    pipe.set(key, str(new_amount))
                    pipe.execute()
                return new_amount
            except redis.WatchError:
                # Another process modified the key, retry
                continue

    def settle_orders(self, symbol_name, total_value):
        key = f"crypto:{symbol_name}"

        while True:
            try:
                with self.client.pipeline() as pipe:
                    pipe.watch(key)

                    # For settle logic, we might consider calling an external system or performing some operations
                    # Here simulating that by just resetting the amount in Redis
                    pipe.multi()
                    pipe.set(key, '0')
                    pipe.execute()

                print(f"Total settled value for symbol {symbol_name}: ${total_value}")
                # Call your external settlement function here, e.g., self.some_external_settlement(symbol_name, total_value)
                break  # Exit the while loop if transaction succeeded
            except redis.WatchError:
                # Another process modified the key, retry
                continue

