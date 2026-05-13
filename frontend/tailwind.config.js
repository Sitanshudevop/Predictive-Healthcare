/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        slate: {
          950: "#020617",
          900: "#0f172a",
          850: "#131d36",
          800: "#1e293b",
          700: "#334155",
        },
        cyan: {
          400: "#22d3ee",
          500: "#06b6d4",
          600: "#0891b2",
        },
        violet: {
          400: "#a78bfa",
          500: "#8b5cf6",
        },
        emerald: {
          400: "#34d399",
          500: "#10b981",
        },
        rose: {
          400: "#fb7185",
          500: "#f43f5e",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      backgroundImage: {
        "glass-gradient": "linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)",
        "cyan-glow": "radial-gradient(ellipse at 50% 0%, rgba(6,182,212,0.15) 0%, transparent 60%)",
        "hero-gradient": "radial-gradient(ellipse at 30% 20%, rgba(6,182,212,0.12) 0%, transparent 50%), radial-gradient(ellipse at 70% 80%, rgba(139,92,246,0.08) 0%, transparent 50%)",
      },
      boxShadow: {
        glass: "0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05)",
        "glass-sm": "0 4px 16px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05)",
        "cyan-glow": "0 0 20px rgba(6,182,212,0.3)",
        "violet-glow": "0 0 20px rgba(139,92,246,0.3)",
      },
      backdropBlur: {
        xs: "2px",
      },
      animation: {
        "pulse-slow": "pulse 3s ease-in-out infinite",
        "float": "float 6s ease-in-out infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        glow: {
          "0%": { boxShadow: "0 0 5px rgba(6,182,212,0.2)" },
          "100%": { boxShadow: "0 0 20px rgba(6,182,212,0.4)" },
        },
      },
    },
  },
  plugins: [],
};
