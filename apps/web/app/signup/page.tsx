import Link from "next/link";
import { ArrowLeft, CheckCircle2, LockKeyhole } from "lucide-react";

export default function SignupPage() {
  return (
    <main className="min-h-screen bg-ink px-4 py-6 text-white sm:px-6">
      <header className="mx-auto flex max-w-5xl items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <span className="grid h-10 w-10 place-items-center rounded bg-mint text-lg font-black text-ink">V</span>
          <span className="text-lg font-black">VolEdge AI</span>
        </Link>
        <Link href="/dashboard" className="inline-flex h-10 items-center rounded border border-line px-4 text-sm font-bold text-white">
          Free Demo
        </Link>
      </header>

      <section className="mx-auto grid min-h-[calc(100vh-88px)] max-w-5xl gap-8 py-12 lg:grid-cols-[1fr_440px] lg:items-center">
        <div>
          <Link href="/" className="inline-flex items-center gap-2 text-sm font-bold text-steel">
            <ArrowLeft size={17} /> Back
          </Link>
          <h1 className="mt-6 max-w-2xl text-5xl font-black leading-tight">Start with the free VolEdge AI demo.</h1>
          <p className="mt-5 max-w-xl text-lg leading-8 text-slate-300">
            Create an account request for ETF swing-trade alerts, qualified accuracy views, raw win rate tracking, and manual approval workflows.
          </p>
          <div className="mt-7 grid gap-3 text-base leading-7 text-slate-200">
            <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Trade-ready and Watch signals separated clearly.</div>
            <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Raw win rate, conservative accuracy, and profit factor visible.</div>
            <div className="flex gap-3"><CheckCircle2 className="mt-1 shrink-0 text-mint" size={20} /> Alert-only mode with no automatic trading.</div>
          </div>
        </div>

        <form className="rounded border border-line bg-panel p-5">
          <div className="flex items-center gap-3">
            <LockKeyhole className="text-amber" size={22} />
            <div>
              <h2 className="text-2xl font-black">Sign up</h2>
              <div className="text-sm text-steel">Free demo first. No card required.</div>
            </div>
          </div>

          <div className="mt-6 grid gap-4">
            <label className="grid gap-2">
              <span className="text-sm font-bold text-steel">Name</span>
              <input className="h-12 rounded border border-line bg-ink px-3 text-white outline-none focus:border-mint" name="name" placeholder="Your name" />
            </label>
            <label className="grid gap-2">
              <span className="text-sm font-bold text-steel">Email</span>
              <input className="h-12 rounded border border-line bg-ink px-3 text-white outline-none focus:border-mint" name="email" placeholder="you@example.com" type="email" />
            </label>
            <label className="grid gap-2">
              <span className="text-sm font-bold text-steel">Trading focus</span>
              <select className="h-12 rounded border border-line bg-ink px-3 text-white outline-none focus:border-mint" name="focus" defaultValue="ETF swing trading">
                <option>ETF swing trading</option>
                <option>Volatility ETFs</option>
                <option>Crypto ETFs</option>
                <option>Sector rotation</option>
              </select>
            </label>
          </div>

          <button className="mt-6 h-12 w-full rounded bg-mint font-black text-ink" type="button">
            Request Access
          </button>
          <Link href="/dashboard" className="mt-3 inline-flex h-12 w-full items-center justify-center rounded border border-line font-bold text-white">
            Open Free Demo
          </Link>
          <p className="mt-4 text-sm leading-6 text-steel">
            This form is ready for a CRM or email provider connection. The demo is available now.
          </p>
        </form>
      </section>
    </main>
  );
}
