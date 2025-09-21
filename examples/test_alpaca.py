from src.broker_alpaca import AlpacaBroker

def main():
    broker = AlpacaBroker()

    # Get account info
    account = broker.get_account()
    print("Account status:", account["status"])
    print("Cash available:", account["cash"])

    # Get latest price
    symbol = "AAPL"
    price = broker.get_latest_price(symbol)
    print(f"Latest {symbol} price:", price)

    # Place test paper order
    order = broker.place_order(symbol=symbol, qty=1, side="buy")
    print("Order response:", order)

    # Get positions
    positions = broker.get_positions()
    print("Open positions:", positions)

if __name__ == "__main__":
    main()
