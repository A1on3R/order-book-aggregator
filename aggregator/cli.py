#!/usr/bin/env python3
import argparse
from aggregator.aggregator import OrderBookAggregator

def main():
    parser = argparse.ArgumentParser(description="Order Book Aggregator")
    parser.add_argument("--quantity", type=float, default=10.0, help="BTC quantity to buy/sell")
    args = parser.parse_args()

    agg = OrderBookAggregator()
    agg.fetch_all()
    agg.print_summary(args.quantity)

if __name__ == "__main__":
    main()