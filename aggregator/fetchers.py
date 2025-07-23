import requests



def fetch_coinbase_book():
    url = "https://api.exchange.coinbase.com/products/BTC-USD/book?level=2"
    resp = requests.get(url)
    data = resp.json()

    def parse(entries):
        parsed = []
        for entry in entries:
            try:
                price = float(entry[0])
                size = float(entry[1])
                parsed.append({"price": price, "quantity": size, "source": "Coinbase"})
            except (IndexError, ValueError, TypeError):
                continue  # skip bad entry
        return parsed
    print("fetching coinbase book...")
    return {
        "bids": parse(data.get("bids", [])),
        "asks": parse(data.get("asks", []))
    }

def fetch_gemini_book():
    url = "https://api.gemini.com/v1/book/BTCUSD"
    resp = requests.get(url)
    data = resp.json()
    print(data)

    def parse(entries):
        parsed = []
        for entry in entries:
            try:
                price = float(entry["price"])
                size = float(entry["amount"])
                parsed.append({"price": price, "quantity": size, "source": "Gemini"})
            except (KeyError, ValueError, TypeError):
                continue
        return parsed
    print("fetching gemeni book...")
    return {
        "bids": parse(data.get("bids", [])),
        "asks": parse(data.get("asks", []))
    }


def fetch_kraken_book():
    print("fetching kraken book...")
    url = "https://api.kraken.com/0/public/Depth?pair=XBTUSD"
    resp = requests.get(url)
    data = resp.json()

  

    # Error handling
    if data.get("error"):
        return {"bids": [], "asks": []}

    book_data = list(data["result"].values())[0]  # e.g., "XXBTZUSD"

    def parse(entries):
        parsed = []
        for entry in entries:
            try:
                price = float(entry[0])
                size = float(entry[1])
                parsed.append({"price": price, "quantity": size, "source": "Kraken"})
            except (IndexError, ValueError, TypeError):
                continue
        return parsed
    
    
    return {
        "bids": parse(book_data.get("bids", [])),
        "asks": parse(book_data.get("asks", []))
    }