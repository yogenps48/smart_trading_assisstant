from src.broker_alpaca import AlpacaBroker
from src.paper_trading_engine import PaperTradingEngine
from src.strategy import generate_signals
from src.indicators import add_rsi

def strategy_wrapper(df, fast_sma=20, slow_sma=50, rsi_threshold=70):
    """
    Wrap Phase 1 strategy for live trading.
    Adds RSI, then applies generate_signals().
    """
    df = add_rsi(df, length=14)
    df = generate_signals(df, fast_sma=fast_sma, slow_sma=slow_sma, rsi_threshold=rsi_threshold)
    return df

def main():
    broker = AlpacaBroker()
    engine = PaperTradingEngine(broker, symbol="AAPL", qty=1, poll_interval=60)
    engine.run(strategy_wrapper, strategy_kwargs={"fast_sma": 20, "slow_sma": 50, "rsi_threshold": 70})

if __name__ == "__main__":
    main()
