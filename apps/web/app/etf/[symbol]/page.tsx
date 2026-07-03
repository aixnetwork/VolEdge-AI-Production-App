import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { SignalBar } from "@/components/SignalBar";
import { getOpportunity } from "@/lib/api";

export default async function EtfDetail({ params }: { params: { symbol: string } }) {
  const symbol = params.symbol.toUpperCase();
  const opportunity = await getOpportunity(symbol);

  if (!opportunity) {
    notFound();
  }

  return (
    <AppShell title={`${opportunity.symbol} Intelligence`}>
      <section className="grid gap-4 lg:grid-cols-[1fr_380px]">
        <div className="rounded border border-line bg-panel/90 p-5">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="text-sm uppercase tracking-wide text-steel">{opportunity.category}</div>
              <div className="text-6xl font-black">{opportunity.symbol}</div>
              <div className="mt-2 text-lg text-slate-200">{opportunity.pattern}</div>
            </div>
            <div className="text-right">
              <div className="text-sm uppercase tracking-wide text-steel">VolEdge Score</div>
              <div className="text-8xl font-black leading-none text-mint">{opportunity.score}</div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-4">
            <Metric label="Latest Price" value={opportunity.currentPrice} />
            <Metric label="Price Change" value={opportunity.priceChangePercent} tone={opportunity.priceTone === "amber" ? "amber" : opportunity.priceTone === "mint" ? "mint" : undefined} />
            <Metric label="Historical Accuracy" value={`${opportunity.accuracy}%`} tone="amber" />
            <Metric label="Confidence Level" value={opportunity.confidence} tone="mint" />
            <Metric label="Risk/Reward" value={opportunity.riskReward} tone="amber" />
            <Metric label="Matches" value={String(opportunity.matches)} />
          </div>

          <div className="mt-6 rounded border border-line bg-ink/45 p-4">
            <div className="text-sm uppercase tracking-wide text-steel">AI Explanation</div>
            <p className="mt-2 text-base leading-7 text-slate-200">{opportunity.explanation}</p>
          </div>
        </div>

        <div className="rounded border border-line bg-panel/80 p-5">
          <h2 className="text-lg font-bold">Trade Plan</h2>
          <div className="mt-4 grid gap-4">
            <Metric label="Latest Price" value={opportunity.currentPrice} />
            <Metric label="Suggested Entry" value={opportunity.entry} />
            <Metric label="Suggested Stop Loss" value={opportunity.stop} />
            <Metric label="Suggested Target" value={opportunity.target} tone="mint" />
            <Metric label="Risk/Reward" value={opportunity.riskReward} tone="amber" />
          </div>
          <button className="mt-5 h-12 w-full rounded bg-mint font-bold text-ink">Manual Approval</button>
        </div>
      </section>

      <section className="mt-5 rounded border border-line bg-panel/80 p-5">
        <h2 className="mb-4 text-lg font-bold">Signal Stack</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {[
            ["Pattern Strength", 88],
            ["Volatility Setup", 91],
            ["Momentum Confirmation", 76]
          ].map(([label, value]) => (
            <div key={label} className="rounded border border-line bg-ink/45 p-4">
              <div className="mb-2 flex justify-between text-sm">
                <span className="text-steel">{label}</span>
                <span className="font-bold text-white">{value}</span>
              </div>
              <SignalBar value={Number(value)} />
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
