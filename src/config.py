import os
from dotenv import load_dotenv

load_dotenv()

# Alpaca
ALPACA_API_KEY_ID = os.getenv("ALPACA_API_KEY_ID")
ALPACA_API_SECRET_KEY = os.getenv("ALPACA_API_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
