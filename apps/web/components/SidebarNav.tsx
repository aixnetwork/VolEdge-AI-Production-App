"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { Activity, Bell, History, LineChart, Loader2, Radar, Settings, ShieldCheck, Star, Waves } from "lucide-react";

const navItems = [
  { href: "/", label: "Radar", icon: Radar },
  { href: "/watchlist", label: "Watchlist", icon: Star },
  { href: "/sectors", label: "Sectors", icon: Activity },
  { href: "/accuracy", label: "Accuracy", icon: History },
  { href: "/patterns", label: "Patterns", icon: Waves },
  { href: "/backtest", label: "Backtest", icon: LineChart },
  { href: "/alerts", label: "Alerts", icon: Bell },
  { href: "/risk", label: "Risk", icon: ShieldCheck },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function SidebarNav() {
  const pathname = usePathname();
  const [pendingHref, setPendingHref] = useState<string | null>(null);

  useEffect(() => {
    setPendingHref(null);
  }, [pathname]);

  return (
    <nav className="grid gap-1">
      {navItems.map((item) => {
        const Icon = item.icon;
        const routeActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        const pending = pendingHref === item.href && !routeActive;
        const className = routeActive
          ? "flex h-11 cursor-default items-center gap-3 rounded border border-mint/35 bg-mint/12 px-3 text-mint"
          : pending
          ? "flex h-11 cursor-progress items-center gap-3 rounded border border-mint/25 bg-mint/8 px-3 text-mint"
          : "flex h-11 items-center gap-3 rounded border border-transparent px-3 text-steel transition hover:border-line hover:bg-panel/70 hover:text-white";

        if (routeActive) {
          return (
            <div key={item.href} className={className} aria-current="page" title={`${item.label} current page`}>
              <Icon size={18} />
              <span className="truncate text-sm font-bold">{item.label}</span>
            </div>
          );
        }

        return (
          <Link
            key={item.href}
            href={item.href}
            prefetch
            className={className}
            title={item.label}
            aria-busy={pending ? "true" : undefined}
            onClick={() => setPendingHref(item.href)}
          >
            {pending ? <Loader2 className="animate-spin" size={18} /> : <Icon size={18} />}
            <span className="truncate text-sm font-bold">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
