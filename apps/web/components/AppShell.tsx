import Link from "next/link";
import { Activity, Bell, Gauge, History, LineChart, Radar, Settings, ShieldCheck, Star, Waves } from "lucide-react";
import { referenceTaglines } from "@/lib/mock-data";

const navItems = [
  { href: "/", label: "Radar", icon: Radar },
  { href: "/etf/UVIX", label: "ETF", icon: Gauge },
  { href: "/sectors", label: "Sectors", icon: Activity },
  { href: "/accuracy", label: "Accuracy", icon: History },
  { href: "/patterns", label: "Patterns", icon: Waves },
  { href: "/backtest", label: "Backtest", icon: LineChart },
  { href: "/alerts", label: "Alerts", icon: Bell },
  { href: "/watchlist", label: "Watchlist", icon: Star },
  { href: "/risk", label: "Risk", icon: ShieldCheck },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function AppShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <main className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 hidden w-24 border-r border-line bg-ink/85 px-3 py-5 backdrop-blur lg:block">
        <Link href="/" className="mb-7 grid h-12 place-items-center rounded bg-mint text-lg font-black text-ink">
          V
        </Link>
        <nav className="grid gap-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                className="grid h-12 place-items-center rounded border border-transparent text-steel hover:border-line hover:text-white"
                title={item.label}
              >
                <Icon size={20} />
              </Link>
            );
          })}
        </nav>
      </aside>

      <section className="mx-auto max-w-7xl px-4 py-5 lg:pl-32">
        <header className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-sm font-semibold text-mint">VolEdge AI</div>
            <h1 className="text-2xl font-bold tracking-normal sm:text-3xl">{title}</h1>
            <div className="mt-1 text-sm text-steel">{referenceTaglines.alternate}</div>
          </div>
          <div className="rounded border border-line bg-panel px-4 py-2 text-sm font-semibold text-white">Alert-only mode</div>
        </header>
        {children}
      </section>
    </main>
  );
}
