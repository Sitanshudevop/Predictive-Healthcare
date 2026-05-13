import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Activity, Brain, BarChart3, BookOpen,
  Menu, X
} from "lucide-react";

const NAV_ITEMS = [
  { label: "Dashboard", path: "/dashboard", icon: Activity },
  { label: "Diagnostic Engine", path: "/diagnose", icon: Brain },

  { label: "Disease Library", path: "/library", icon: BookOpen },
];

export default function Navbar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50">
      <div className="glass-panel mx-4 mt-3 px-6 py-3 flex items-center justify-between"
           style={{ borderRadius: "16px" }}>
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-cyan-600 flex items-center justify-center shadow-cyan-glow group-hover:shadow-lg transition-all">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-bold tracking-tight" style={{ color: '#F4F4F5' }}>
            Predictive Healthcare
          </span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                  active
                    ? "text-cyan-400 bg-cyan-500/10"
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
                }`}
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
          <Link
            to="/system-health"
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              location.pathname === "/system-health"
                ? "text-violet-400 bg-violet-500/10"
                : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            System Health
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden p-2 rounded-lg hover:bg-white/[0.04] transition-all"
        >
          {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Nav */}
      {mobileOpen && (
        <div className="md:hidden glass-panel mx-4 mt-2 p-3" style={{ borderRadius: "16px" }}>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  active
                    ? "text-cyan-400 bg-cyan-500/10"
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
                }`}
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
          <Link
            to="/system-health"
            onClick={() => setMobileOpen(false)}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
              location.pathname === "/system-health"
                ? "text-violet-400 bg-violet-500/10"
                : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.04]"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            System Health
          </Link>
        </div>
      )}
    </nav>
  );
}
