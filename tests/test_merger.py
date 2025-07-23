from aggregator.merger import merge_books

def test_merge_books_combines_and_sorts():
    b1 = {"bids": [{"price": 30000, "quantity": 1}], "asks": [{"price": 30100, "quantity": 1}]}
    b2 = {"bids": [{"price": 31000, "quantity": 2}], "asks": [{"price": 29900, "quantity": 3}]}

    merged = merge_books(b1, b2)

    assert merged["bids"] == [
        {"price": 31000, "quantity": 2},
        {"price": 30000, "quantity": 1}
    ]

    assert merged["asks"] == [
        {"price": 29900, "quantity": 3},
        {"price": 30100, "quantity": 1}
    ]