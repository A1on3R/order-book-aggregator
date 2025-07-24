from aggregator.fetchers import fetch_coinbase_book, fetch_gemini_book, fetch_kraken_book
from aggregator.calculator import get_price_for_quantity
from aggregator.merger import merge_books

class OrderBookAggregator:
    def __init__(self):
        self.books = []

    def fetch_all(self):
        print("Fetching order books...")
        self.books = [
            fetch_coinbase_book(),
            fetch_gemini_book(),
            fetch_kraken_book(),
        ]

    
    def get_price_summary(self, quantity):
        merged = merge_books(*self.books)
        buy_cost = get_price_for_quantity(merged["asks"], quantity)
        sell_return = get_price_for_quantity(merged["bids"], quantity)
        return buy_cost, sell_return

       

    def print_summary(self, quantity):
        (buy_cost, buy_orders), (sell_return, sell_orders) = self.get_price_summary(quantity)

        print(f"\nResults for {quantity} BTC:")
        if buy_cost is not None:
            print(f"  Buy cost:  ${buy_cost:,.2f}")
            print(f"  Orders used (buy):")
            for o in buy_orders:
                print(f"    - {o['quantity']} BTC @ ${o['price']:,.2f} from {o['source']}")

        else:
            print("  Not enough ask liquidity to buy.")

        if sell_return is not None:
            print(f"  Sell return: ${sell_return:,.2f}")
            print(f"  Orders used (sell):")
            for o in sell_orders:
                print(f"    - {o['quantity']} BTC @ ${o['price']:,.2f} from {o['source']}")
        else:
            print("  Not enough bid liquidity to sell.")