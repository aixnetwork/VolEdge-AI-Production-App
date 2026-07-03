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
            <h2 className="text-3xl font-black">{top.pattern} with manual approval</h2>
          </div>
          <Metric label="Best Window" value={top.window} tone="mint" />
        </div>
        <div className="mt-5 grid gap-3">
          {backtestRows.map((row) => (
            <div key={row.window} className="grid gap-3 rounded border border-line bg-ink/45 p-4 md:grid-cols-6">
              <Metric label="Window" value={row.window} />
              <Metric label="Trades" value={String(row.trades)} />
              <Metric label="Win Rate" value={row.winRate} tone="amber" />
              <Metric label="Avg Return" value={row.avgReturn} tone="mint" />
              <Metric label="Drawdown" value={row.drawdown} />
              <Metric label="Profit Factor" value={row.profitFactor} />
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
