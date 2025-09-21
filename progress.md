# Smart Trading Assistant — Project Progress Tracker

This document tracks the exact status of the project so progress is clear and no steps are missed.

---

## ✅ Phase 1: Backtesting (Complete)
- [x] Data fetcher (Yahoo Finance, cached to CSV)
- [x] Indicators (RSI, SMA, MACD via `pandas_ta`)
- [x] Strategy (SMA crossover + RSI filter)
- [x] Simple backtest engine (cash, equity curve, trade log)
- [x] Streamlit demo UI for backtesting
- [ ] Unit tests for components (optional future task)

---

## 🚧 Phase 2: Broker Integration (Zerodha)
Goal: Connect to real Zerodha Kite API for quotes & paper trading.

- [ ] Install & configure `kiteconnect` library
- [ ] Store API key/secret in `.env` file
- [ ] Generate & store access token securely
- [ ] Fetch live market quotes (equity & F&O)
- [ ] Place mock orders (buy/sell) with Zerodha sandbox or small qty
- [ ] Implement paper trading engine (simulate fills, P&L)
- [ ] Error handling & logging

---

## 🔜 Phase 3: Risk Management & Order Sizing
- [ ] Position sizing rules (fixed, % risk, Kelly, etc.)
- [ ] Stop-loss & take-profit logic
- [ ] Daily drawdown limits
- [ ] Portfolio-level risk management

---

## 🔜 Phase 4: Logging & Reporting
- [ ] Trade logs to CSV/DB
- [ ] Performance metrics (Sharpe, max drawdown, win rate)
- [ ] Generate PDF/HTML reports

---

## 🔜 Phase 5: Streamlit UI for Live Trading
- [ ] Login/auth flow
- [ ] Live dashboard (positions, equity curve, open trades)
- [ ] Start/stop trading button
- [ ] Configurable strategies via UI

---

## 🔜 Phase 6: Deployment
- [ ] Run as background service or container
- [ ] Secure deployment (Docker, VM, or cloud)
- [ ] Monitoring & alerts (email/Slack/Telegram)

---

# Notes
- Use **incremental development**: finish each small step before moving on.
- Keep broker API keys in `.env` (never in GitHub).
- Backtesting & paper trading must be stable **before live trading**.
