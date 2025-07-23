from aggregator.calculator import get_price_for_quantity
def test_price_calculation_exact_quantity():
    asks = [
        {"price": 10000, "quantity": 5},
        {"price": 10100, "quantity": 5}
    ]
    result = get_price_for_quantity(asks, 10)
    assert result == (5 * 10000 + 5 * 10100)

def test_insufficient_liquidity_returns_none():
    asks = [
        {"price": 10000, "quantity": 3},
        {"price": 10100, "quantity": 2}
    ]
    # Only 5 BTC available, but we want 10
    result = get_price_for_quantity(asks, 10)
    assert result is None

def test_partial_quantity_taken_from_multiple_levels():
    asks = [
        {"price": 10000, "quantity": 4},
        {"price": 10100, "quantity": 6}
    ]
    # Buy 7 BTC: take 4 from first, 3 from second
    result = get_price_for_quantity(asks, 7)
    expected = 4 * 10000 + 3 * 10100
    assert result == expected

def test_sell_price_calculation_works_for_bids():
    bids = [
        {"price": 9900, "quantity": 3},
        {"price": 9800, "quantity": 4}
    ]
    # Selling 5 BTC: take 3 at 9900, 2 at 9800
    result = get_price_for_quantity(bids, 5)
    expected = 3 * 9900 + 2 * 9800
    assert result == expected