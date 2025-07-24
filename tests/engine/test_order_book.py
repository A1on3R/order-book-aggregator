from aggregator.engine.order import Order
from aggregator.engine.order_book import OrderBook

def test_order_initialization():
    order = Order(
        order_id="abc123",
        timestamp=1234567890,
        side="buy",
        price=30000.0,
        quantity=1.5
    )

    assert order.order_id == "abc123"
    assert order.timestamp == 1234567890
    assert order.side == "buy"
    assert order.price == 30000.0
    assert order.quantity == 1.5

def test_add_order_to_orderbook():
    book = OrderBook()
    order = Order("1", "buy", 30000.0, 1.0, 0)
    book.add_order(order)

    assert book.bids[0] == order

def test_orderbook_orders_are_sorted_correctly():
    book = OrderBook()

    # Add bids (buy orders)
    book.add_order(Order("1", "buy", 30000.0, 1.0, 0))
    book.add_order(Order("2",  "buy", 31000.0, 1.0, 0))
    book.add_order(Order("3",  "buy", 30500.0, 1.0, 0))

    # Add asks (sell orders)
    book.add_order(Order("4", "sell", 32000.0, 1.0, 0))
    book.add_order(Order("5", "sell", 31500.0, 1.0, 0))
    book.add_order(Order("6", "sell", 31800.0, 1.0, 0))
    book.sort_orders()

    # Check bid order: should be 31000, 30500, 30000
    bid_prices = [order.price for order in book.bids]
    assert bid_prices == [31000.0, 30500.0, 30000.0]

    # Check ask order: should be 31500, 31800, 32000
    ask_prices = [order.price for order in book.asks]
    assert ask_prices == [31500.0, 31800.0, 32000.0]

def test_orderbook_orders_sorted_by_price_then_time():
    book = OrderBook()

    # Add buy orders: same price, different timestamps
    book.add_order(Order("1", "buy", 30000.0, 1.0, 10))
    book.add_order(Order("2", "buy", 30000.0, 1.0, 5))
    book.add_order(Order("3", "buy", 31000.0, 1.0, 1))
    book.sort_orders()

    # Bids: highest price first, then earlier timestamp
    bid_ids = [order.order_id for order in book.bids]
    assert bid_ids == ["3", "2", "1"]

    # Add sell orders
    book.add_order(Order("4", "sell", 32000.0, 1.0, 3))
    book.add_order(Order("5", "sell", 31500.0, 1.0, 2))
    book.add_order(Order("6", "sell", 31500.0, 1.0, 1))
    book.sort_orders()

    # Asks: lowest price first, then earlier timestamp
    ask_ids = [order.order_id for order in book.asks]
    assert ask_ids == ["6", "5", "4"]