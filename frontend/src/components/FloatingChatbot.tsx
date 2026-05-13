import { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send, Bot, User, Loader2, Sparkles, Minimize2 } from "lucide-react";

interface Message {
  id: number;
  role: "user" | "bot";
  text: string;
  timestamp: Date;
}

const QUICK_REPLIES = [
  "What diseases can you predict?",
  "How accurate are the models?",
  "What data do you need for diabetes risk?",
  "Is my data private?",
];

const BOT_RESPONSES: Record<string, string> = {
  "default": "I'm your Predictive Healthcare Assistant, your AI health guide. I can help with symptom checks, explain prediction results, or guide you through the diagnostic engine. What would you like to know?",
  "diseases": "Predictive Healthcare can predict **11 conditions**: General Disease (132+ conditions), Diabetes, Heart Disease, Breast Cancer, Liver Disease, Kidney Disease, Pneumonia (via X-ray), Skin Lesions (7 types), Mental Health Risk, and Severity Scoring. Plus NLP-based symptom extraction!",
  "accurate": "Our models achieve strong accuracy:\n• Breast Cancer: **98.3%**\n• General Disease: **96.2%**\n• Kidney: **95.1%**\n• Pneumonia CNN: **94.6%**\n• Heart: **91.5%**\n\nAll models are validated with holdout test sets.",
  "diabetes": "For diabetes risk assessment, I need 8 parameters:\n1. Number of pregnancies\n2. Glucose level (mg/dL)\n3. Blood pressure (mm Hg)\n4. Skin thickness (mm)\n5. Insulin level (mu U/ml)\n6. BMI\n7. Diabetes pedigree function\n8. Age\n\nHead to **Diagnostic Engine → Biometrics** to start!",
  "private": "Absolutely! Your data is kept private:\n• **No account required** — fully anonymous usage\n• **Browser-only storage** — history stays in localStorage\n• **No server-side data** — predictions are not stored remotely\n• No third-party data sharing\n• Rate-limited API for fair usage",
};

function getResponse(text: string): string {
  const lower = text.toLowerCase();
  if (lower.includes("disease") || lower.includes("predict") || lower.includes("condition")) return BOT_RESPONSES.diseases;
  if (lower.includes("accura") || lower.includes("how good") || lower.includes("reliable")) return BOT_RESPONSES.accurate;
  if (lower.includes("diabetes") || lower.includes("sugar") || lower.includes("glucose")) return BOT_RESPONSES.diabetes;
  if (lower.includes("privat") || lower.includes("data") || lower.includes("secure") || lower.includes("safe")) return BOT_RESPONSES.private;
  if (lower.includes("hello") || lower.includes("hi") || lower.includes("hey")) return "Hello! 👋 I'm the Predictive Healthcare Assistant. Ask me about our prediction models, how to use the diagnostic engine, or anything health-related!";
  if (lower.includes("symptom") || lower.includes("check")) return "Great question! Go to **Diagnostic Engine → NLP Symptom Parser** and describe your symptoms in plain English. Our AI will extract medical entities and run predictions across multiple models.";
  if (lower.includes("help") || lower.includes("how")) return "Here's how to use Predictive Healthcare:\n1. **NLP Tab**: Describe symptoms in text\n2. **Biometrics Tab**: Enter lab values\n3. **Image Lab**: Upload X-rays or skin photos\n\nEach tab handles different ML models. Need help with a specific one?";
  return "I can help with:\n• Understanding prediction results\n• Navigating the diagnostic engine\n• Disease information from our library\n• Data privacy questions\n\nWhat would you like to know more about?";
}

export default function FloatingChatbot() {
  const [open, setOpen] = useState(false);
  const [minimized, setMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 0, role: "bot", text: BOT_RESPONSES.default, timestamp: new Date() },
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, typing]);

  useEffect(() => {
    if (open && !minimized) inputRef.current?.focus();
  }, [open, minimized]);

  const sendMessage = (text: string) => {
    if (!text.trim()) return;
    const userMsg: Message = { id: Date.now(), role: "user", text, timestamp: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setTyping(true);

    setTimeout(() => {
      const resp = getResponse(text);
      setMessages((prev) => [...prev, { id: Date.now() + 1, role: "bot", text: resp, timestamp: new Date() }]);
      setTyping(false);
    }, 800 + Math.random() * 600);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  // Render markdown-like bold text
  const renderText = (text: string) => {
    return text.split("\n").map((line, i) => (
      <span key={i}>
        {line.split(/(\*\*.*?\*\*)/).map((part, j) =>
          part.startsWith("**") && part.endsWith("**")
            ? <strong key={j} className="text-cyan-300 font-semibold">{part.slice(2, -2)}</strong>
            : <span key={j}>{part}</span>
        )}
        {i < text.split("\n").length - 1 && <br />}
      </span>
    ));
  };

  return (
    <>
      {/* FAB */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 flex items-center justify-center shadow-cyan-glow hover:shadow-lg transition-all hover:scale-105 active:scale-95 group"
          id="chatbot-fab"
        >
          <MessageCircle className="w-6 h-6 text-white" />
          {/* Notification dot */}
          <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 border-2 border-slate-950 animate-pulse" />
        </button>
      )}

      {/* Chat Window */}
      {open && (
        <div
          className={`fixed bottom-6 right-6 z-50 w-[380px] rounded-2xl overflow-hidden glass-card border border-white/[0.08] shadow-glass flex flex-col transition-all duration-300 ${
            minimized ? "h-14" : "h-[520px]"
          }`}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06] bg-slate-900/50 flex-shrink-0 cursor-pointer" onClick={() => minimized && setMinimized(false)}>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500/20 to-cyan-500/10 flex items-center justify-center">
                <Bot className="w-4 h-4 text-cyan-400" />
              </div>
              <div>
                <p className="text-sm font-semibold text-white">Predictive Healthcare Assistant</p>
                {!minimized && <p className="text-[10px] text-emerald-400 flex items-center gap-1"><span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />Online</p>}
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button onClick={(e) => { e.stopPropagation(); setMinimized(!minimized); }} className="p-1.5 rounded-lg hover:bg-white/[0.06] transition-colors">
                <Minimize2 className="w-3.5 h-3.5 text-slate-400" />
              </button>
              <button onClick={() => setOpen(false)} className="p-1.5 rounded-lg hover:bg-white/[0.06] transition-colors">
                <X className="w-3.5 h-3.5 text-slate-400" />
              </button>
            </div>
          </div>

          {!minimized && (
            <>
              {/* Messages */}
              <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex gap-2 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                    {msg.role === "bot" && (
                      <div className="w-7 h-7 rounded-lg bg-cyan-500/10 flex items-center justify-center flex-shrink-0 mt-1">
                        <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                      </div>
                    )}
                    <div className={`max-w-[260px] px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${
                      msg.role === "user"
                        ? "bg-cyan-500/15 text-cyan-100 rounded-br-md"
                        : "bg-white/[0.04] text-slate-300 rounded-bl-md"
                    }`}>
                      {renderText(msg.text)}
                    </div>
                    {msg.role === "user" && (
                      <div className="w-7 h-7 rounded-lg bg-violet-500/10 flex items-center justify-center flex-shrink-0 mt-1">
                        <User className="w-3.5 h-3.5 text-violet-400" />
                      </div>
                    )}
                  </div>
                ))}
                {typing && (
                  <div className="flex gap-2 items-start">
                    <div className="w-7 h-7 rounded-lg bg-cyan-500/10 flex items-center justify-center flex-shrink-0">
                      <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                    </div>
                    <div className="bg-white/[0.04] px-4 py-3 rounded-2xl rounded-bl-md">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: "0ms" }} />
                        <span className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: "150ms" }} />
                        <span className="w-2 h-2 rounded-full bg-slate-500 animate-bounce" style={{ animationDelay: "300ms" }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Quick Replies */}
              {messages.length <= 1 && (
                <div className="px-4 pb-2 flex flex-wrap gap-1.5">
                  {QUICK_REPLIES.map((q, i) => (
                    <button
                      key={i}
                      onClick={() => sendMessage(q)}
                      className="text-[11px] px-2.5 py-1.5 rounded-lg bg-white/[0.03] border border-white/[0.06] text-slate-400 hover:text-cyan-400 hover:border-cyan-500/20 transition-all"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              )}

              {/* Input */}
              <form onSubmit={handleSubmit} className="p-3 border-t border-white/[0.06] flex gap-2 flex-shrink-0">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about symptoms, models..."
                  className="glass-input py-2.5 text-sm flex-1"
                />
                <button type="submit" disabled={!input.trim() || typing} className="btn-primary px-3 py-2.5 disabled:opacity-30">
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </>
          )}
        </div>
      )}
    </>
  );
}
