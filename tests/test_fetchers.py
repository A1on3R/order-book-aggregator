from aggregator.fetchers import fetch_coinbase_book
from aggregator.fetchers import fetch_gemini_book
from aggregator.fetchers import fetch_kraken_book
from unittest.mock import patch

@patch("aggregator.fetchers.requests.get")
def test_fetch_coinbase_book(mock_get):
    # Mock the JSON response
    mock_get.return_value.json.return_value = {
        "bids": [["30000.00", "1.5", "1"]],
        "asks": [["30100.00", "2.25", "1"]],
    }

    book = fetch_coinbase_book()
    
    assert book["bids"] == [{"price": 30000.0, "quantity": 1.5, "source": "Coinbase"}]
    assert book["asks"] == [{"price": 30100.0, "quantity": 2.25, "source": "Coinbase"}]

@patch("aggregator.fetchers.requests.get")
def test_fetch_coinbase_book_missing_fields(mock_get):
    mock_get.return_value.json.return_value = {}
    book = fetch_coinbase_book()
    assert book == {"bids": [], "asks": []}

@patch("aggregator.fetchers.requests.get")
def test_fetch_coinbase_book_bad_entry_structure(mock_get):
    mock_get.return_value.json.return_value = {
        "bids": [["30000.00"]],  # too short
        "asks": [["30100.00", "bad_quantity", "1"]]  # bad quantity
    }
    book = fetch_coinbase_book()
    assert book == {"bids": [], "asks": []}

@patch("aggregator.fetchers.requests.get")
def test_fetch_coinbase_book_mixed_valid_and_invalid(mock_get):
    mock_get.return_value.json.return_value = {
        "bids": [["30000.00", "1.5", "1"], ["bad", "data"]],
        "asks": [["30100.00", "2.25", "1"], ["30101", "bad_quantity", "1"]]
    }
    book = fetch_coinbase_book()
    assert book["bids"] == [{"price": 30000.0, "quantity": 1.5, "source": "Coinbase"}]
    assert book["asks"] == [{"price": 30100.0, "quantity": 2.25, "source": "Coinbase"}]


    from aggregator.fetchers import fetch_gemini_book

@patch("aggregator.fetchers.requests.get")
def test_fetch_gemini_book_valid(mock_get):
    mock_get.return_value.json.return_value = {
        "bids": [{"price": "30000.00", "amount": "1.2"}],
        "asks": [{"price": "30100.00", "amount": "2.4"}]
    }

    book = fetch_gemini_book()
    assert book["bids"] == [{"price": 30000.0, "quantity": 1.2, "source": "Gemini"}]
    assert book["asks"] == [{"price": 30100.0, "quantity": 2.4, "source": "Gemini"}]

@patch("aggregator.fetchers.requests.get")
def test_fetch_gemini_book_with_bad_data(mock_get):
    mock_get.return_value.json.return_value = {
        "bids": [{"price": "bad", "amount": "1.2"}, {"price": "30000.00"}],
        "asks": [{"price": "30100.00", "amount": "2.4"}, {"amount": "bad"}]
    }

    book = fetch_gemini_book()
    assert book["bids"] == []
    assert book["asks"] == [{"price": 30100.0, "quantity": 2.4, "source": "Gemini"}]

@patch("aggregator.fetchers.requests.get")
def test_fetch_kraken_book_valid(mock_get):
    mock_get.return_value.json.return_value = {
        "error": [],
        "result": {
            "XXBTZUSD": {
                "bids": [["30000.00", "0.9", 1234567890]],
                "asks": [["30100.00", "1.5", 1234567891]]
            }
        }
    }

    book = fetch_kraken_book()
    assert book["bids"] == [{"price": 30000.0, "quantity": 0.9, "source": "Kraken"}]
    assert book["asks"] == [{"price": 30100.0, "quantity": 1.5, "source": "Kraken"}]

@patch("aggregator.fetchers.requests.get")
def test_fetch_kraken_book_with_error(mock_get):
    mock_get.return_value.json.return_value = {
        "error": ["Some error"],
        "result": {}
    }

    book = fetch_kraken_book()
    assert book == {"bids": [], "asks": []}