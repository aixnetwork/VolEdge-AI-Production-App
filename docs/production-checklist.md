# Production Checklist

## Required Before Launch

- Replace `SampleMarketDataProvider` in `apps/api/app/providers.py` with a licensed market data provider implementation.
- Supported market data values are `sample-provider-ready`, `yfinance`, `polygon`, `twelve-data`, and `finnhub`.
- Use `yfinance` only for delayed/research data. Use a licensed provider before marketing signals as real-time production intelligence.
- Set `NEXT_PUBLIC_API_BASE_URL` in Vercel.
- Set `CORS_ORIGINS` in the API deployment to the exact Vercel domain.
- Run `database/schema.sql` in Supabase.
- Set `STORE_BACKEND=supabase` after `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are configured.
- Configure Supabase Auth redirect URLs for web and mobile.
- Store provider keys in deployment secrets, never in source control.
- Confirm `TRADING_ENABLED=false` for version 1.

## API Readiness

- `GET /api/status` returns app version, environment, market data provider, CORS origins, and trading safety status.
- All recommendation responses include entry, stop, target, risk/reward, historical accuracy, confidence level, and explanation.
- Alerts are decision support only.

## Verification

Run:

```bash
pip install -r apps/api/requirements.txt
pytest apps/api/tests
pnpm --dir apps/web install --no-frozen-lockfile
pnpm --dir apps/web build
```

On this desktop runtime, prepend the bundled Node directory to `PATH` before running the web build if the shell cannot find `node`.

## Production Data Rule

Do not market accuracy as live production accuracy until OHLCV data comes from the configured provider and backtests are run on that provider's normalized bars.
