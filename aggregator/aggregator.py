from aggregator.fetchers import fetch_coinbase_book, fetch_gemini_book, fetch_kraken_book
from aggregator.merger import merge_books
from aggregator.engine.order import Order
from aggregator.engine.order_book import OrderBook
import time

class OrderBookAggregator:
    def __init__(self):
        self.books = []
        self.order_book = OrderBook()

    def fetch_all(self):
        print("Fetching order books...")
        self.books = [
            fetch_coinbase_book(),
            fetch_gemini_book(),
            fetch_kraken_book(),
        ]

    def _entry_to_order(self, entry, side, order_id, timestamp):
        return Order(
            order_id=str(order_id),
            timestamp=timestamp,
            side=side,
            price=entry["price"],
            quantity=entry["quantity"],
            source=entry.get("source", "unknown")
    )
    
    def _build_order_book(self, merged):
        order_book = OrderBook()
        timestamp = time.time()
        order_id_counter = 0
    
        for side in ["asks", "bids"]:
            for entry in merged[side]:
                order = self.entry_to_order(entry, "sell" if side == "asks" else "buy", order_id_counter, timestamp)
                order_book.add_order(order)
                order_id_counter += 1
    
        order_book.sort_orders()
        return order_book
    
    def get_price_summary(self, quantity):
        merged = merge_books(*self.books)
        order_book = OrderBook()

        timestamp = time.time()

        order_id_counter = 0
        for entry in merged["asks"]:
            order = Order(
                order_id=str(order_id_counter),
                timestamp=timestamp,
                side="sell",
                price=entry["price"],
                quantity=entry["quantity"],
                source=entry.get("source", "unknown")
        )
            order_book.add_order(order)
            order_id_counter += 1
        
        for entry in merged["bids"]:
            order = Order(
                order_id=str(order_id_counter),
                timestamp=timestamp,
                side="buy",
                price=entry["price"],
                quantity=entry["quantity"],
                source=entry.get("source", "unknown")
            )
            order_book.add_order(order)
            order_id_counter += 1
        order_book.sort_orders()
        buy_cost = order_book.get_price_for_quantity("sell", quantity)
        sell_return = order_book.get_price_for_quantity("buy", quantity)
        return buy_cost, sell_return

       

    def print_summary(self, quantity):
        (buy_cost, buy_orders), (sell_return, sell_orders) = self.get_price_summary(quantity)

        print(f"\nResults for {quantity} BTC:")
        if buy_cost is not None:
            print(f"  Buy cost:  ${buy_cost:,.2f}")
            print(f"  Orders used (buy):")
            for order in buy_orders:
                print(f"    - {order['quantity']} BTC @ ${order['price']:,.2f} from {order['source']}")

        else:
            print("  Not enough ask liquidity to buy.")

        if sell_return is not None:
            print(f"  Sell return: ${sell_return:,.2f}")
            print(f"  Orders used (sell):")
            for order in sell_orders:
                print(f"    - {order['quantity']} BTC @ ${order['price']:,.2f} from {order['source']}")
        else:
            print("  Not enough bid liquidity to sell.")