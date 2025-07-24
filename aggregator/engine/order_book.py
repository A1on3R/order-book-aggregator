class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []

    def add_order(self, order):
        side = order.side.lower()
        
        if side == "buy":
            self.bids.append(order)
            
        else:    
            self.asks.append(order)
    
    def sort_orders(self):
        self.bids.sort(key=lambda o: (-o.price, o.timestamp))  # Highest price first
        self.asks.sort(key=lambda o: (o.price, o.timestamp))
    
    def get_price_for_quantity(self, side: str, quantity_needed: float):
        orders = self.bids if side == "buy" else self.asks
        total = 0.0
        remaining = quantity_needed
        used_orders = []

        for order in orders:
            qty = min(order.quantity, remaining)
            total += qty * order.price
            used_orders.append({
                "price": order.price,
                "quantity": qty,
                "source": getattr(order, "source", "unknown")
            })
            remaining -= qty
            if remaining <= 0:
                return total, used_orders

        return None, []