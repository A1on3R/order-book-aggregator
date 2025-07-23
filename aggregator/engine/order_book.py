class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

    def add_order(self, order):
        if order.side == "buy":
            self.bids.append(order)
            self.bids.sort(key=lambda o: (-o.price, o.timestamp))  # Highest price first
        else:
            self.asks.append(order)
            self.asks.sort(key=lambda o: (o.price,o.timestamp))  # Lowest price first