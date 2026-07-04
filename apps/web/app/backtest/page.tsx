import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { getBacktestData, getOpportunity } from "@/lib/api";

export default async function BacktestResults() {
  const [top, backtestRows] = await Promise.all([getOpportunity("UVIX"), getBacktestData("UVIX")]);

  return (
    <AppShell title="Backtest Results">
      <section className="rounded border border-line bg-panel/90 p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="text-sm uppercase tracking-wide text-steel">{top.symbol} strategy</div>
            <h2 className="text-3xl font-black">{top.pattern} qualified setup filter</h2>
            <div className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
              Backtests now measure only historical periods that match the active trend, momentum, volatility, volume, and key-level setup filter.
            </div>
          </div>
          <Metric label="Best Window" value={top.window} tone="mint" />
        </div>
        <div className="mt-5 grid gap-3">
          {backtestRows.map((row) => (
            <div key={row.window} className="grid gap-3 rounded border border-line bg-ink/45 p-4 md:grid-cols-8">
              <Metric label="Window" value={row.window} />
              <Metric label="Trades" value={String(row.trades)} />
              <Metric label="Qualified Accuracy" value={row.winRate} tone="amber" />
              <Metric label="Raw Win Rate" value={row.rawWinRate ?? row.winRate} tone="mint" />
              <Metric label="Expected Return" value={row.expectedReturn ?? row.avgReturn} tone="mint" />
              <Metric label="Avg Return" value={row.avgReturn} tone="mint" />
              <Metric label="Drawdown" value={row.drawdown} />
              <Metric label="Profit Factor" value={row.profitFactor} />
              <div className="md:col-span-8">
                <div className="rounded border border-line bg-panel/60 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-steel">
                  {row.filter ?? "Qualified setup only"}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
