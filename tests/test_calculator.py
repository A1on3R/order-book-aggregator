import time
from aggregator.engine.order import Order
from aggregator.engine.order_book import OrderBook

def make_orderbook(orders, side):
    ob = OrderBook()
    timestamp = time.time()
    for i, entry in enumerate(orders):
        order = Order(
            order_id=str(i),
            timestamp=timestamp,
            side=side,
            price=entry["price"],
            quantity=entry["quantity"]
        )
        ob.add_order(order)
    return ob

def test_price_calculation_exact_quantity():
    asks = [
        {"price": 10000, "quantity": 5},
        {"price": 10100, "quantity": 5}
    ]
    ob = make_orderbook(asks, side="sell")
    result, _ = ob.get_price_for_quantity("sell", 10)
    assert result == (5 * 10000 + 5 * 10100)

def test_insufficient_liquidity_returns_none():
    asks = [
        {"price": 10000, "quantity": 3},
        {"price": 10100, "quantity": 2}
    ]
    ob = make_orderbook(asks, side="sell")
    result, used = ob.get_price_for_quantity("sell", 10)
    assert result is None
    assert used == []

def test_partial_quantity_taken_from_multiple_levels():
    asks = [
        {"price": 10000, "quantity": 4},
        {"price": 10100, "quantity": 6}
    ]
    ob = make_orderbook(asks, side="sell")
    result, used = ob.get_price_for_quantity("sell", 7)
    expected = 4 * 10000 + 3 * 10100
    assert result == expected
    assert used == [
        {"price": 10000, "quantity": 4, "source": "unknown"},
        {"price": 10100, "quantity": 3, "source": "unknown"}
    ]

def test_sell_price_calculation_works_for_bids():
    bids = [
        {"price": 9900, "quantity": 3},
        {"price": 9800, "quantity": 4}
    ]
    ob = make_orderbook(bids, side="buy")
    result, used = ob.get_price_for_quantity("buy", 5)
    expected = 3 * 9900 + 2 * 9800
    assert result == expected
    assert used == [
        {"price": 9900, "quantity": 3, "source": "unknown"},
        {"price": 9800, "quantity": 2, "source": "unknown"}
    ]