def get_price_for_quantity(order_list, quantity_needed):
    total = 0.0
    remaining = quantity_needed

    for order in order_list:
        qty = min(order["quantity"], remaining)
        total += qty * order["price"]
        remaining -= qty
        if remaining <= 0:
            return total
    return None