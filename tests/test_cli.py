import subprocess
import sys
from unittest.mock import patch
import cli

# We'll run cli.py as a subprocess and mock fetchers inline
@patch("aggregator.fetchers.fetch_coinbase_book")
@patch("aggregator.fetchers.fetch_gemini_book")
@patch("aggregator.fetchers.fetch_kraken_book")
def test_cli_outputs_expected_result(mock_kraken, mock_gemini, mock_coinbase):
    # Set up mock return values
    fake_book = {
        "bids": [{"price": 30000.0, "quantity": 2.0}],
        "asks": [{"price": 30100.0, "quantity": 2.0}]
    }
    mock_coinbase.return_value = fake_book
    mock_gemini.return_value = fake_book
    mock_kraken.return_value = fake_book

    # Call the CLI as a subprocess
    result = subprocess.run(
        [sys.executable, "cli.py", "--quantity", "5"],
        capture_output=True,
        text=True
    )

    # Check output
    assert "Results for 5.0 BTC:" in result.stdout
    assert "Buy cost" in result.stdout
    assert "Sell return" in result.stdout
    assert result.returncode == 0

@patch("aggregator.fetchers.fetch_coinbase_book")
@patch("aggregator.fetchers.fetch_gemini_book")
@patch("aggregator.fetchers.fetch_kraken_book")
def test_cli_calls_each_fetcher(mock_kraken, mock_gemini, mock_coinbase):
    fake_book = {
        "bids": [{"price": 30000.0, "quantity": 1.0}],
        "asks": [{"price": 30100.0, "quantity": 1.0}]
    }
    mock_coinbase.return_value = fake_book
    mock_gemini.return_value = fake_book
    mock_kraken.return_value = fake_book

    import sys
    sys.argv = ["cli.py", "--quantity", "5"]

    cli.main()

    mock_coinbase.assert_called_once()
    mock_gemini.assert_called_once()
    mock_kraken.assert_called_once()