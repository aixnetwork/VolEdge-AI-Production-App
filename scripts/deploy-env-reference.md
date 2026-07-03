# Deployment Environment Reference

## API

Set these in Render or Railway:

```text
ENVIRONMENT=production
CORS_ORIGINS=https://YOUR_VERCEL_DOMAIN
MARKET_DATA_PROVIDER=sample-provider-ready
STORE_BACKEND=memory
TRADING_ENABLED=false
```

For live data:

```text
MARKET_DATA_PROVIDER=polygon
POLYGON_API_KEY=...
```

or:

```text
MARKET_DATA_PROVIDER=twelve-data
TWELVE_DATA_API_KEY=...
```

or:

```text
MARKET_DATA_PROVIDER=finnhub
FINNHUB_API_KEY=...
```

For Supabase persistence:

```text
STORE_BACKEND=supabase
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

## Web

Set this in Vercel:

```text
NEXT_PUBLIC_API_BASE_URL=https://YOUR_API_DOMAIN
```
