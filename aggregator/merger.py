def merge_books(*books):
    merged_bids = []
    merged_asks = []

    for book in books:
        merged_bids.extend(book.get("bids", []))
        merged_asks.extend(book.get("asks", []))

    merged_bids.sort(key=lambda o: -o["price"])  # highest price first
    merged_asks.sort(key=lambda o: o["price"])   # lowest price first

    return {"bids": merged_bids, "asks": merged_asks}