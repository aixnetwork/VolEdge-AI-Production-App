"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Bell, History, LineChart, Radar, Settings, ShieldCheck, Star, Waves } from "lucide-react";

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

  return (
    <nav className="grid gap-1">
      {navItems.map((item) => {
        const Icon = item.icon;
        const active = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        const className = active
          ? "flex h-11 cursor-default items-center gap-3 rounded border border-mint/35 bg-mint/12 px-3 text-mint"
          : "flex h-11 items-center gap-3 rounded border border-transparent px-3 text-steel transition hover:border-line hover:bg-panel/70 hover:text-white";

        if (active) {
          return (
            <div key={item.href} className={className} aria-current="page" title={`${item.label} current page`}>
              <Icon size={18} />
              <span className="truncate text-sm font-bold">{item.label}</span>
            </div>
          );
        }

        return (
          <Link key={item.href} href={item.href} prefetch className={className} title={item.label}>
            <Icon size={18} />
            <span className="truncate text-sm font-bold">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
