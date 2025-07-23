from aggregator.engine.order import Order

def test_order_creation():
    order = Order(order_id="1", side="buy", price=100.0, quantity=1.5)

    assert order.order_id == "1"
    assert order.side == "buy"
    assert order.price == 100.0
    assert order.quantity == 1.5