import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import Navbar from "./components/layout/Navbar";
import FloatingChatbot from "./components/FloatingChatbot";
import LandingPage from "./pages/LandingPage";
import DashboardPage from "./pages/DashboardPage";
import DiagnosePage from "./pages/DiagnosePage";

import LibraryPage from "./pages/LibraryPage";
import SystemHealthPage from "./pages/SystemHealthPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-950 text-slate-200">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/diagnose" element={<DiagnosePage />} />

          <Route path="/library" element={<LibraryPage />} />
          <Route path="/system-health" element={<SystemHealthPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Floating Chatbot — always visible */}
        <FloatingChatbot />

        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#1e293b",
              color: "#e2e8f0",
              border: "1px solid rgba(255,255,255,0.06)",
              borderRadius: "12px",
              fontSize: "14px",
            },
          }}
        />
      </div>
    </BrowserRouter>
  );
}
