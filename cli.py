import argparse
import aggregator.fetchers as fetchers
from aggregator.merger import merge_books
from aggregator.calculator import get_price_for_quantity

def main():
    parser = argparse.ArgumentParser(description="Order Book Aggregator")
    parser.add_argument("--quantity", type=float, default=10.0, help="BTC quantity to buy/sell")
    args = parser.parse_args()

    # Fetch from exchanges
    print("Fetching order books...")
    coinbase = fetchers.fetch_coinbase_book()
    gemini = fetchers.fetch_gemini_book()
    kraken = fetchers.fetch_kraken_book()

    # Merge books
    merged = merge_books(coinbase, gemini, kraken)

    # Calculate total price
    buy_price = get_price_for_quantity(merged["asks"], args.quantity)
    sell_price = get_price_for_quantity(merged["bids"], args.quantity)

    # Print result
    print(f"\nResults for {args.quantity} BTC:")
    if buy_price is not None:
        print(f"  Buy cost:  ${buy_price:,.2f}")
    else:
        print("  Not enough asks to buy that quantity.")

    if sell_price is not None:
        print(f"  Sell return: ${sell_price:,.2f}")
    else:
        print("  Not enough bids to sell that quantity.")

if __name__ == "__main__":
    main()