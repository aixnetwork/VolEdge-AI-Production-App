# API Contract

All recommendations are alert-only and require manual approval.

## Required endpoints

- `GET /api/radar`
- `GET /api/intelligence/{symbol}`
- `GET /api/patterns/{symbol}`
- `GET /api/accuracy/{symbol}`
- `GET /api/backtest/{symbol}`
- `GET /api/sectors/radar`
- `GET /api/sectors/{sector}`
- `GET /api/alerts`
- `POST /api/alerts`
- `GET /api/watchlist`
- `POST /api/watchlist`
- `GET /api/risk`
- `GET /api/status`

## Scoring

VolEdge Score uses:

- 30% Historical Accuracy
- 25% Pattern Strength
- 20% Volatility Setup
- 15% Momentum Confirmation
- 10% Risk/Reward

Historical accuracy is calculated from OHLCV bars. Production must use licensed market data before presenting live alerts.

## Intelligence response core metrics

`GET /api/intelligence/{symbol}` includes the four reference home-screen metrics:

- `vol_edge_score`
- `historical_accuracy`
- `confidence_level`
- `risk_reward`

## Production providers

Set `MARKET_DATA_PROVIDER` to one of:

- `sample-provider-ready`
- `polygon`
- `twelve-data`
- `finnhub`

Set `STORE_BACKEND=supabase` to persist alerts and watchlist records through Supabase REST.
