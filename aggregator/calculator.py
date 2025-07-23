def get_price_for_quantity(order_list, quantity_needed):
    total = 0.0
    remaining = quantity_needed
    used_orders = []

    for order in order_list:
        qty = min(order["quantity"], remaining)
        total += qty * order["price"]
        used_orders.append({
            "price": order["price"],
            "quantity": qty,
            "source": order.get("source", "Unknown")
        })
        remaining -= qty
        if remaining <= 0:
            return total, used_orders
    return None, []