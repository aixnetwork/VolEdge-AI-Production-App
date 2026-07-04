import Link from "next/link";
import { ArrowRight, BarChart3, CheckCircle2, LineChart, LockKeyhole, Radar, ShieldCheck, Sparkles } from "lucide-react";

const bars = [46, 58, 52, 72, 66, 84, 61, 76, 88, 70, 82, 94, 78, 86, 73, 91];
const signals = [
  { label: "USO", action: "Strong Sell", value: "73.5%" },
  { label: "XLF", action: "Strong Buy", value: "72.7%" },
  { label: "UVIX", action: "Strong Sell", value: "72.6%" }
];
const proof = [
  { label: "Qualified accuracy", value: "72%+" },
  { label: "Raw win rate", value: "86%+" },
  { label: "Risk/reward", value: "2.1:1" }
];
const workflow = [
  { icon: Radar, title: "Find", text: "Scan leveraged ETFs, sectors, volatility, crypto ETFs, bonds, commodities, and broad market names." },
  { icon: BarChart3, title: "Validate", text: "Separate raw win rate from conservative qualified accuracy, sample size, profit factor, and drawdown." },
  { icon: ShieldCheck, title: "Gate", text: "Downgrade weak setups to Watch before they can appear as trade-ready buy or sell ideas." }
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-ink text-white">
      <section className="relative min-h-[92vh] overflow-hidden border-b border-line">
        <div className="absolute inset-0 bg-[#071017]" />
        <div className="absolute inset-0 opacity-90">
          <div className="absolute inset-x-0 bottom-0 h-[62%] border-t border-line/70 bg-panel/40">
            <div className="absolute inset-0 grid grid-cols-[repeat(16,minmax(0,1fr))] items-end gap-2 px-4 pb-0 sm:px-10">
              {bars.map((height, index) => (
                <div key={index} className="flex h-full items-end">
                  <div className={index % 4 === 0 ? "w-full bg-amber/65" : "w-full bg-mint/70"} style={{ height: `${height}%` }} />
                </div>
              ))}
            </div>
            <div className="absolute left-[8%] top-[18%] h-px w-[84%] bg-mint/70" />
            <div className="absolute left-[14%] top-[35%] h-px w-[68%] bg-amber/60" />
          </div>
          <div className="absolute right-4 top-24 grid w-[min(440px,calc(100vw-2rem))] gap-3 sm:right-10">
            {signals.map((signal) => (
              <div key={signal.label} className="rounded border border-line bg-ink/85 p-4 shadow-2xl shadow-black/25">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <div className="text-sm font-bold text-steel">{signal.label}</div>
                    <div className={signal.action.includes("Buy") ? "mt-1 text-xl font-black text-mint" : "mt-1 text-xl font-black text-amber"}>
                      {signal.action}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-bold uppercase text-steel">Accuracy</div>
                    <div className="text-3xl font-black">{signal.value}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <header className="relative z-10 mx-auto flex max-w-7xl items-center justify-between px-4 py-5 sm:px-6">
          <Link href="/" className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded bg-mint text-lg font-black text-ink">V</span>
            <span className="text-lg font-black">VolEdge AI</span>
          </Link>
          <nav className="flex items-center gap-2">
            <Link href="/dashboard" className="hidden h-10 items-center rounded border border-line px-4 text-sm font-bold text-white sm:inline-flex">
              Free Demo
            </Link>
            <Link href="/signup" className="inline-flex h-10 items-center gap-2 rounded bg-mint px-4 text-sm font-black text-ink">
              Sign Up <ArrowRight size={17} />
            </Link>
          </nav>
        </header>

        <div className="relative z-10 mx-auto flex min-h-[calc(92vh-84px)] max-w-7xl items-center px-4 pb-16 pt-10 sm:px-6">
          <div className="max-w-3xl">
            <div className="mb-5 inline-flex items-center gap-2 rounded border border-mint/40 bg-ink/75 px-3 py-2 text-sm font-bold text-mint">
              <Sparkles size={17} /> Alert-only ETF swing intelligence
            </div>
            <h1 className="max-w-3xl text-5xl font-black leading-[1.02] text-white sm:text-7xl">
              VolEdge AI
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-200 sm:text-xl">
              Find trade-ready ETF swings with qualified accuracy, raw win rate, risk/reward, profit factor, and manual approval built into every signal.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/dashboard" className="inline-flex h-12 items-center gap-2 rounded bg-mint px-5 text-sm font-black text-ink">
                Start Free Demo <ArrowRight size={18} />
              </Link>
              <Link href="/signup" className="inline-flex h-12 items-center gap-2 rounded border border-line bg-ink/80 px-5 text-sm font-bold text-white">
                Create Account
              </Link>
            </div>
            <div className="mt-8 grid max-w-2xl gap-3 sm:grid-cols-3">
              {proof.map((item) => (
                <div key={item.label} className="rounded border border-line bg-ink/80 p-4">
                  <div className="text-3xl font-black text-mint">{item.value}</div>
                  <div className="mt-1 text-sm font-semibold text-steel">{item.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="border-b border-line bg-panel/60 px-4 py-14 sm:px-6">
        <div className="mx-auto grid max-w-7xl gap-4 md:grid-cols-3">
          {workflow.map((item) => {
            const Icon = item.icon;
            return (
              <article key={item.title} className="rounded border border-line bg-ink/60 p-5">
                <Icon className="text-mint" size={24} />
                <h2 className="mt-4 text-2xl font-black">{item.title}</h2>
                <p className="mt-3 leading-7 text-slate-300">{item.text}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="px-4 py-14 sm:px-6">
        <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1fr_420px] lg:items-center">
          <div>
            <div className="text-sm font-bold uppercase text-mint">Built for swing-trade decisions</div>
            <h2 className="mt-3 max-w-3xl text-4xl font-black sm:text-5xl">See the difference between a high score and a trade-ready setup.</h2>
            <div className="mt-6 grid gap-3 text-base leading-7 text-slate-200">
              <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Raw win rate and conservative accuracy are shown separately.</div>
              <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Weak setups are held on Watch before they become recommendations.</div>
              <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Entry, stop, target, risk/reward, and explanation stay visible before approval.</div>
            </div>
          </div>
          <div className="rounded border border-line bg-panel p-5">
            <div className="flex items-center gap-3">
              <LockKeyhole className="text-amber" size={22} />
              <div>
                <h3 className="text-2xl font-black">Free demo access</h3>
                <div className="text-sm text-steel">No automatic trading. Manual approval only.</div>
              </div>
            </div>
            <div className="mt-5 grid gap-3">
              <Link href="/dashboard" className="inline-flex h-12 items-center justify-center gap-2 rounded bg-mint px-5 font-black text-ink">
                Open Free Demo <LineChart size={18} />
              </Link>
              <Link href="/signup" className="inline-flex h-12 items-center justify-center gap-2 rounded border border-line px-5 font-bold text-white">
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
