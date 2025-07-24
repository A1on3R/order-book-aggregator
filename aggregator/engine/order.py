import time

class Order:
    def __init__(self, order_id: str, side: str, price: float, quantity: float, timestamp: float = None, source: str = "unknown"):
        self.order_id = order_id
        self.side = side  # "buy" or "sell"
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp or time.time()
        self.source = source