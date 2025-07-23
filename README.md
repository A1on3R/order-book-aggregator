# Order Book Aggregator CLI

A Python command-line tool that fetches live order books for BTC/USD from multiple exchanges (Coinbase, Gemini, Kraken), aggregates the data, and calculates the cost or return for buying or selling a specific quantity of BTC.

---

## 📦 Features

- Fetches real-time bid/ask order book data from:
  - Coinbase
  - Gemini
  - Kraken
- Aggregates books for better price analysis
- Calculates:
  - **Buy Cost**: how much USD it costs to buy a specified quantity of BTC
  - **Sell Return**: how much USD you'd get for selling a specified quantity of BTC
- CLI interface for quick access
- Fully tested with `pytest`

---

## 🔧 Installation

1. **Clone or unzip the project** into a folder.

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate         # On Windows: venv\Scripts\activate

3. **Install (User Only)**
   ```bash
   pip install .

4. **Install and run tests (Developer)**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   pytest

5. **Run Program**
   ```bash
   which orderbook             # To make sure it installed
   orderbook                   # default is for 10 Bitcoin
   orderbook --quantity 1.3    #The amount of bitcoin as a double/float as an arg
