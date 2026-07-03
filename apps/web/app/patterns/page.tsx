import { Activity, BrainCircuit, Target, TrendingDown, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { Metric } from "@/components/Metric";
import { SignalBar } from "@/components/SignalBar";
import { getPatternData } from "@/lib/api";

function directionTone(direction: string) {
  if (direction === "Bearish") {
    return "border-amber/50 text-amber";
  }
  if (direction === "Bullish") {
    return "border-mint/50 text-mint";
  }
  return "border-line text-white";
}

function probabilityTone(bullish: number, bearish: number) {
  return bullish >= bearish ? "mint" : "amber";
}

export default async function PatternDetail() {
  const { patterns, usingFallback } = await getPatternData();
  const top = patterns[0];

  return (
    <AppShell title="Pattern Recognition Detail">
      {usingFallback ? (
        <div className="mb-4 rounded border border-amber/40 bg-amber/10 px-4 py-3 text-sm text-amber">
          Demo pattern data is active. Live API prediction detail appears after Render is connected.
        </div>
      ) : null}

      {top ? (
        <section className="mb-5 rounded border border-mint/35 bg-panel/95 p-5">
          <div className="flex flex-wrap items-start justify-between gap-5">
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <BrainCircuit className="text-mint" size={21} />
                <div className="text-sm uppercase tracking-wide text-steel">Highest AI Chart Prediction</div>
              </div>
              <div className="mt-2 flex flex-wrap items-end gap-3">
                <span className="text-5xl font-black">{top.symbol}</span>
                <span className={`mb-1 rounded border px-2 py-1 text-xs font-bold uppercase ${directionTone(top.direction)}`}>
                  {top.direction}
                </span>
                <span className="pb-1 text-2xl font-black text-mint">{top.predictedMove}</span>
              </div>
              <p className="mt-3 max-w-4xl text-base leading-7 text-slate-200">{top.summary}</p>
            </div>
            <div className="grid min-w-[280px] grid-cols-2 gap-4">
              <Metric label="AI Prediction Score" value={`${top.predictionScore}`} tone="mint" />
              <Metric label="Historical Accuracy" value={`${top.historicalAccuracy}%`} tone="amber" />
              <Metric label="Current Price" value={top.currentPrice} />
              <Metric label="Key Level" value={top.keyLevel} />
            </div>
          </div>
          <div className="mt-5 grid gap-4 border-t border-line pt-5 md:grid-cols-2">
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-semibold text-mint">Breakout Probability</span>
                <span className="font-black text-mint">{top.breakoutProbability}%</span>
              </div>
              <SignalBar value={top.breakoutProbability} />
            </div>
            <div>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-semibold text-amber">Breakdown Probability</span>
                <span className="font-black text-amber">{top.breakdownProbability}%</span>
              </div>
              <SignalBar value={top.breakdownProbability} />
            </div>
          </div>
        </section>
      ) : null}

      <section className="grid gap-4">
        {patterns.map((pattern, index) => {
          const primaryTone = probabilityTone(pattern.breakoutProbability, pattern.breakdownProbability);
          return (
            <article key={`${pattern.symbol}-${pattern.name}`} className="rounded border border-line bg-panel/85 p-5">
              <div className="grid gap-5 xl:grid-cols-[1fr_220px_220px] xl:items-start">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded border border-line px-2 py-1 text-xs font-bold uppercase text-steel">Rank {index + 1}</span>
                    <span className={`rounded border px-2 py-1 text-xs font-bold uppercase ${directionTone(pattern.direction)}`}>
                      {pattern.direction}
                    </span>
                    <span className="rounded border border-line px-2 py-1 text-xs font-bold uppercase text-steel">
                      {pattern.confidence} confidence
                    </span>
                  </div>
                  <div className="mt-3 flex flex-wrap items-end gap-3">
                    <h2 className="text-4xl font-black">{pattern.symbol}</h2>
                    <div className="pb-1 text-xl font-black text-white">{pattern.name}</div>
                  </div>
                  <div className="mt-3 text-base leading-7 text-slate-200">{pattern.summary}</div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {pattern.evidence.map((item) => (
                      <span key={item} className="rounded border border-line bg-ink/50 px-3 py-2 text-xs font-semibold text-slate-200">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 xl:grid-cols-1">
                  <Metric label="Prediction Score" value={`${pattern.predictionScore}`} tone={primaryTone} />
                  <Metric label="Pattern Quality" value={`${pattern.quality}`} tone="mint" />
                  <Metric label="Historical Accuracy" value={`${pattern.historicalAccuracy}%`} tone="amber" />
                </div>

                <div className="grid gap-4">
                  <div className="rounded border border-line bg-ink/45 p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold text-mint">
                      <TrendingUp size={17} /> Breakout
                    </div>
                    <div className="mt-2 flex items-center justify-between gap-3">
                      <span className="text-3xl font-black text-mint">{pattern.breakoutProbability}%</span>
                      <span className="text-right text-sm text-steel">{pattern.keyLevel}</span>
                    </div>
                    <div className="mt-3"><SignalBar value={pattern.breakoutProbability} /></div>
                  </div>
                  <div className="rounded border border-line bg-ink/45 p-4">
                    <div className="flex items-center gap-2 text-sm font-semibold text-amber">
                      <TrendingDown size={17} /> Breakdown
                    </div>
                    <div className="mt-2 flex items-center justify-between gap-3">
                      <span className="text-3xl font-black text-amber">{pattern.breakdownProbability}%</span>
                      <span className="text-right text-sm text-steel">{pattern.currentPrice}</span>
                    </div>
                    <div className="mt-3"><SignalBar value={pattern.breakdownProbability} /></div>
                  </div>
                </div>
              </div>

              <div className="mt-5 grid gap-3 border-t border-line pt-5 md:grid-cols-3">
                <div className="flex items-center gap-3">
                  <Target className="text-mint" size={20} />
                  <Metric label="Trigger Level" value={pattern.keyLevel} />
                </div>
                <Metric label="Latest Price" value={pattern.currentPrice} />
                <div className="flex items-center gap-3">
                  <Activity className="text-amber" size={20} />
                  <Metric label="Predicted Move" value={pattern.predictedMove} tone={primaryTone} />
                </div>
              </div>
            </article>
          );
        })}
      </section>
    </AppShell>
  );
}
