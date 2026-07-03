import { CheckCircle2, ShieldAlert, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { SignalBar } from "@/components/SignalBar";
import { getAccuracyData } from "@/lib/api";

function gateTone(status: string) {
  return status === "Trade Ready" ? "border-mint/50 text-mint" : "border-amber/50 text-amber";
}

export default async function AccuracyDetail() {
  const { top, rows, usingFallback } = await getAccuracyData();

  return (
    <AppShell title="Historical Accuracy Detail">
      {usingFallback ? (
        <div className="mb-4 rounded border border-amber/40 bg-amber/10 px-4 py-3 text-sm text-amber">
          Demo accuracy data is active. Live qualified accuracy appears after the API connects.
        </div>
      ) : null}

      <section className="mb-5 rounded border border-mint/35 bg-panel/95 p-5">
        <div className="flex flex-wrap items-start justify-between gap-5">
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <TrendingUp className="text-mint" size={21} />
              <div className="text-sm uppercase tracking-wide text-steel">Highest Qualified Historical Accuracy</div>
            </div>
            <div className="mt-2 flex flex-wrap items-end gap-3">
              <span className="text-5xl font-black">{top.symbol}</span>
              <span className={`mb-1 rounded border px-2 py-1 text-xs font-bold uppercase ${gateTone(top.gateStatus)}`}>
                {top.gateStatus}
              </span>
              <span className="pb-1 text-xl font-black text-white">{top.pattern}</span>
            </div>
            <p className="mt-3 max-w-4xl text-base leading-7 text-slate-200">{top.explanation}</p>
          </div>
          <div className="grid min-w-[300px] grid-cols-2 gap-4">
            <Metric label="Qualified Accuracy" value={`${top.qualifiedAccuracy}%`} tone="amber" />
            <Metric label="Raw Win Rate" value={`${top.rawWinRate}%`} tone="mint" />
            <Metric label="Expected Value" value={top.expectedValue} tone="mint" />
            <Metric label="Profit Factor" value={top.profitFactor} />
          </div>
        </div>
        <div className="mt-5 grid gap-4 border-t border-line pt-5 md:grid-cols-4">
          <Metric label="Historical Matches" value={String(top.matches)} />
          <Metric label="Best Window" value={top.bestWindow} />
          <Metric label="Risk/Reward" value={top.riskReward} tone={top.gateStatus === "Trade Ready" ? "mint" : "amber"} />
          <Metric label="Sample Confidence" value={top.confidence} />
        </div>
      </section>

      <section className="grid gap-4">
        {rows.map((row) => (
          <article key={row.symbol} className="rounded border border-line bg-panel/85 p-5">
            <div className="grid gap-5 lg:grid-cols-[1fr_220px_220px] lg:items-start">
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded border border-line px-2 py-1 text-xs font-bold uppercase text-steel">Rank {row.rank}</span>
                  <span className={`rounded border px-2 py-1 text-xs font-bold uppercase ${gateTone(row.gateStatus)}`}>
                    {row.gateStatus}
                  </span>
                  <span className="rounded border border-line px-2 py-1 text-xs font-bold uppercase text-steel">{row.recommendation}</span>
                </div>
                <div className="mt-3 flex flex-wrap items-end gap-3">
                  <h2 className="text-4xl font-black">{row.symbol}</h2>
                  <div className="pb-1 text-xl font-black text-white">{row.category}</div>
                </div>
                <div className="mt-2 text-sm text-steel">{row.pattern} / {row.bestWindow}</div>
                <div className="mt-4">
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="font-semibold text-amber">Qualified Accuracy</span>
                    <span className="font-black text-amber">{row.qualifiedAccuracy}%</span>
                  </div>
                  <SignalBar value={row.qualifiedAccuracy} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 lg:grid-cols-1">
                <Metric label="Raw Win Rate" value={`${row.rawWinRate}%`} tone="mint" />
                <Metric label="Matches" value={String(row.matches)} />
                <Metric label="Confidence" value={row.confidence} />
              </div>

              <div className="grid grid-cols-2 gap-4 lg:grid-cols-1">
                <Metric label="Expected Value" value={row.expectedValue} tone="mint" />
                <Metric label="Profit Factor" value={row.profitFactor} />
                <Metric label="Risk/Reward" value={row.riskReward} tone={row.gateStatus === "Trade Ready" ? "mint" : "amber"} />
              </div>
            </div>

            <div className="mt-5 grid gap-3 border-t border-line pt-5 md:grid-cols-3">
              <div className="flex items-center gap-3">
                {row.gateStatus === "Trade Ready" ? <CheckCircle2 className="text-mint" size={20} /> : <ShieldAlert className="text-amber" size={20} />}
                <Metric label="Gate Status" value={row.gateStatus} tone={row.gateStatus === "Trade Ready" ? "mint" : "amber"} />
              </div>
              <Metric label="Average Return" value={row.averageReturn} tone="mint" />
              <Metric label="Max Drawdown" value={row.maxDrawdown} />
            </div>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
