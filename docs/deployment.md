# Deployment Guide

## Frontend: Vercel

1. Set the project root to `apps/web`.
2. Add `NEXT_PUBLIC_API_BASE_URL` with the deployed FastAPI URL.
3. Use `pnpm install --no-frozen-lockfile` as the install command.
4. Use `pnpm build` as the build command.

## Backend: Render or Railway

1. Set the service root to `apps/api`.
2. Install with `pip install -r requirements.txt`.
3. Start with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add market data credentials as provider-specific environment variables.
5. Set `CORS_ORIGINS` to the Vercel frontend origin.
6. Set `STORE_BACKEND=supabase` after Supabase credentials are configured.

## Database: Supabase

1. Create a Supabase project.
2. Run `database/schema.sql`.
3. Enable Supabase Auth for web and mobile clients.

## Market Data

The backend ships with a deterministic sample adapter and implemented adapter classes for Polygon, Twelve Data, and Finnhub. Production deployments should set `MARKET_DATA_PROVIDER` and the matching provider API key before presenting live alerts.
