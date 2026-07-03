# Launch Commands

## 1. Create GitHub Repository

Create a blank GitHub repository named `voledge-ai`.

Then run these commands from the clean committed repo folder:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/voledge-ai.git
git push -u origin main
```

If using GitHub CLI:

```powershell
gh auth login
gh repo create YOUR_USERNAME/voledge-ai --private --source . --remote origin --push
```

## 2. Deploy API

Deploy `apps/api` to Render or Railway.

Required environment variables:

```text
ENVIRONMENT=production
CORS_ORIGINS=https://YOUR_VERCEL_DOMAIN
MARKET_DATA_PROVIDER=sample-provider-ready
STORE_BACKEND=memory
TRADING_ENABLED=false
```

For live data, change `MARKET_DATA_PROVIDER` to `polygon`, `twelve-data`, or `finnhub` and add the matching API key.

## 3. Deploy Web

Deploy `apps/web` to Vercel.

Required environment variable:

```text
NEXT_PUBLIC_API_BASE_URL=https://YOUR_API_DOMAIN
```

## 4. Enable Supabase

Run `database/schema.sql` in Supabase, then set these API environment variables:

```text
STORE_BACKEND=supabase
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
```

Keep `TRADING_ENABLED=false` for version 1.
