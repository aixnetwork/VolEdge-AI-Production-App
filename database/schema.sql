create table if not exists etfs (
  symbol text primary key,
  name text not null,
  category text not null,
  leverage integer default 1,
  active boolean default true
);

create table if not exists ohlcv_bars (
  id bigint generated always as identity primary key,
  symbol text references etfs(symbol),
  bar_date date not null,
  open numeric not null,
  high numeric not null,
  low numeric not null,
  close numeric not null,
  volume bigint not null,
  unique(symbol, bar_date)
);

create table if not exists signals (
  id uuid primary key default gen_random_uuid(),
  symbol text references etfs(symbol),
  pattern text not null,
  vol_edge_score numeric not null,
  historical_accuracy numeric not null,
  expected_return numeric not null,
  suggested_entry numeric not null,
  suggested_stop numeric not null,
  suggested_target numeric not null,
  risk_reward numeric not null,
  explanation text not null,
  created_at timestamptz default now()
);

create table if not exists alerts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  symbol text references etfs(symbol),
  condition text not null,
  threshold numeric not null,
  active boolean default true,
  created_at timestamptz default now()
);

create table if not exists watchlist_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  symbol text references etfs(symbol),
  created_at timestamptz default now(),
  unique(user_id, symbol)
);

create table if not exists backtest_runs (
  id uuid primary key default gen_random_uuid(),
  symbol text references etfs(symbol),
  strategy text not null,
  trades integer not null,
  win_rate numeric not null,
  expected_return numeric not null,
  max_drawdown numeric not null,
  profit_factor numeric not null,
  created_at timestamptz default now()
);

create table if not exists portfolio_positions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid,
  symbol text references etfs(symbol),
  quantity numeric not null default 0,
  average_cost numeric,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists sector_volatility_snapshots (
  id uuid primary key default gen_random_uuid(),
  symbol text references etfs(symbol),
  sector text not null,
  sector_volatility_score numeric not null,
  recommendation text not null,
  atr_expansion numeric not null,
  realized_volatility_spike numeric not null,
  volume_surge numeric not null,
  relative_strength_vs_spy numeric not null,
  created_at timestamptz default now()
);
