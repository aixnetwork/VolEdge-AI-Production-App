# Product Scope

## Version 1

VolEdge AI version 1 is an ETF intelligence and alert platform. It identifies ranked ETF opportunities, explains the top opportunity, and provides a manual trade plan with entry, stop loss, target, risk/reward, historical accuracy, and supporting pattern context.

## Required screens

- Home / Opportunity Radar
- ETF Detail
- Sector Volatility Radar
- Historical Accuracy Detail
- Pattern Recognition Detail
- Backtest Results
- Alerts
- Watchlist
- Portfolio Risk
- Settings

The initial web app composes these core workflows into one focused dashboard. Future iterations can split them into dedicated routes without changing the API contract.

The current web build includes dedicated routes for each required screen:

- `/`
- `/etf/UVIX`
- `/sectors`
- `/accuracy`
- `/patterns`
- `/backtest`
- `/alerts`
- `/watchlist`
- `/risk`
- `/settings`

## Safety

No automatic trading is included. The product is decision support only.
