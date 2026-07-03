import { Activity, CheckCircle2, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { OpportunityCard } from "@/components/OpportunityCard";
import { SignalBar } from "@/components/SignalBar";
import { getRadarData, getSectorData } from "@/lib/api";
import { productArchitecture, referenceTaglines } from "@/lib/mock-data";

export default async function Home() {
  const [{ top, opportunities, usingFallback }, sectors] = await Promise.all([getRadarData(), getSectorData()]);

  return (
    <AppShell title="Opportunity Radar">
      {usingFallback ? (
        <div className="mb-4 rounded border border-amber/40 bg-amber/10 px-4 py-3 text-sm text-amber">
          Demo data is active. Set NEXT_PUBLIC_API_BASE_URL to connect live API intelligence.
        </div>
      ) : null}
      <section className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
        <div className="rounded border border-line bg-panel/90 p-5 shadow-2xl shadow-black/20">
          <div className="mb-4 flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-sm uppercase tracking-wide text-steel">Top Opportunity</div>
              <div className="mt-1 text-sm font-semibold text-mint">{referenceTaglines.primary}</div>
              <div className="mt-1 flex items-end gap-3">
                <span className="text-5xl font-black sm:text-7xl">{top.symbol}</span>
                <span className="pb-2 text-sm font-semibold text-mint">{top.category}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm uppercase tracking-wide text-steel">VolEdge Score</div>
              <div className="text-7xl font-black leading-none text-mint sm:text-8xl">{top.score}</div>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-4">
            <Metric label="Historical Accuracy" value={`${top.accuracy}%`} tone="amber" />
            <Metric label="Confidence Level" value={top.confidence} tone="mint" />
            <Metric label="Risk/Reward" value={top.riskReward} tone="amber" />
            <Metric label="Recommendation" value={top.recommendation} />
          </div>

          <div className="mt-5 grid gap-4 border-t border-line pt-5 md:grid-cols-[1fr_0.85fr]">
            <p className="text-base leading-7 text-slate-200">{top.explanation}</p>
            <div className="grid grid-cols-2 gap-3">
              <Metric label="Entry" value={top.entry} />
              <Metric label="Stop Loss" value={top.stop} />
              <Metric label="Target" value={top.target} tone="mint" />
              <Metric label="Risk/Reward" value={top.riskReward} tone="amber" />
            </div>
          </div>

          <button className="mt-5 inline-flex h-12 w-full items-center justify-center gap-2 rounded bg-mint px-5 font-bold text-ink sm:w-auto">
            <CheckCircle2 size={19} /> Manual Approval
          </button>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-bold">Sector Volatility Radar</h2>
            <Activity className="text-mint" size={20} />
          </div>
          <div className="grid gap-3">
            {sectors.map((sector) => (
              <div key={sector.symbol} className="rounded border border-line bg-ink/45 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="font-semibold">{sector.sector}</div>
                    <div className="text-sm text-steel">{sector.symbol} / {sector.signal}</div>
                  </div>
                  <div className="text-3xl font-black text-mint">{sector.score}</div>
                </div>
                <div className="mt-3">
                  <SignalBar value={sector.score} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-5 grid gap-4 xl:grid-cols-[1fr_360px]">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-lg font-bold">Top Ranked ETF Opportunities</h2>
            <TrendingUp className="text-mint" size={20} />
          </div>
          <div className="grid gap-3 md:grid-cols-2">
            {opportunities.map((item) => (
              <OpportunityCard key={item.symbol} item={item} />
            ))}
          </div>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <h2 className="text-lg font-bold">Portfolio Risk</h2>
          <div className="mt-4 grid gap-4">
            <Metric label="Exposure Bias" value="Volatility Long" tone="amber" />
            <Metric label="Correlation Watch" value="SOXL / QQQ" />
            <Metric label="Platform Mode" value="Decision Support" tone="mint" />
          </div>
          <div className="mt-5 rounded border border-line bg-ink/50 p-4 text-sm leading-6 text-slate-200">
            No automatic trading is enabled. Every recommendation requires manual approval and includes entry, stop, target, risk/reward, historical accuracy, and explanation.
          </div>
        </div>
      </section>

      <section className="mt-5 rounded border border-line bg-panel/80 p-5">
        <h2 className="text-lg font-bold">Intelligence Architecture</h2>
        <div className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {productArchitecture.map((item) => (
            <div key={item} className="rounded border border-line bg-ink/45 px-4 py-3 text-sm font-semibold text-slate-200">
              {item}
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
