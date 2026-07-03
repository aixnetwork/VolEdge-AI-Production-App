import { AppShell } from "@/components/AppShell";
import { SignalBar } from "@/components/SignalBar";
import { patternSignals } from "@/lib/mock-data";

export default function PatternDetail() {
  return (
    <AppShell title="Pattern Recognition Detail">
      <section className="grid gap-4">
        {patternSignals.map((pattern) => (
          <article key={pattern.name} className="rounded border border-line bg-panel/80 p-5">
            <div className="grid gap-4 md:grid-cols-[1fr_160px_160px_160px] md:items-center">
              <div>
                <h2 className="text-2xl font-black">{pattern.name}</h2>
                <div className="mt-1 text-sm text-steel">{pattern.direction} / {pattern.confidence} confidence</div>
              </div>
              <div>
                <div className="text-xs uppercase text-steel">Quality</div>
                <div className="text-4xl font-black text-mint">{pattern.quality}</div>
              </div>
              <div>
                <div className="text-xs uppercase text-steel">Accuracy</div>
                <div className="text-4xl font-black text-amber">{pattern.accuracy}%</div>
              </div>
              <SignalBar value={pattern.quality} />
            </div>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
