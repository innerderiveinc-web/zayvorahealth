"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

interface Message {
  id: string;
  sender: string;
  role: string;
  text: string;
  time: string;
  isMe: boolean;
}

const INITIAL_MESSAGES: Message[] = [
  { id: "1", sender: "Hakeem Dr. Irfan Ashraf", role: "Senior Tabeeb", text: "As-salamu alaykum Hamza. How is the morning knee stiffness after 5 days of Majun Suranjan?", time: "Yesterday, 4:15 PM", isMe: false },
  { id: "2", sender: "Hamza Farooqi", role: "Patient", text: "Wa alaykum as-salam Doctor. The acute throbbing has reduced significantly, but there is still slight heaviness while climbing stairs.", time: "Yesterday, 4:30 PM", isMe: true },
  { id: "3", sender: "Hakeem Dr. Irfan Ashraf", role: "Senior Tabeeb", text: "That is expected during the Tanqiya stage. Continue the ginger infusion vehicle (Anupan) and perform the quad exercises. We will evaluate for Stage 2 next week.", time: "Yesterday, 4:45 PM", isMe: false }
];

export default function PatientMessagesPage() {
  const [messages, setMessages] = useState<Message[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState("");

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const newMsg: Message = {
      id: Date.now().toString(),
      sender: "Hamza Farooqi",
      role: "Patient",
      text: input.trim(),
      time: "Just now",
      isMe: true
    };
    setMessages([...messages, newMsg]);
    setInput("");
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">💬 Secure Clinical Messaging</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Direct encrypted asynchronous channel with Hakeem Dr. Irfan Ashraf
          </p>
        </div>

        <div className="bg-[var(--card)] rounded-2xl border border-[var(--border)] h-[520px] flex flex-col justify-between overflow-hidden shadow-sm">
          {/* Chat Header */}
          <div className="p-4 border-b border-[var(--border)] flex items-center gap-3 bg-slate-900/50">
            <div className="w-10 h-10 rounded-full bg-emerald-950/60 border border-emerald-500/40 flex items-center justify-center text-lg">
              👨‍⚕️
            </div>
            <div>
              <h3 className="font-bold text-white text-sm">Hakeem Dr. Irfan Ashraf</h3>
              <p className="text-xs text-emerald-400">Senior Tabeeb • Clinical Lead • ZAYVORA Central Hospital</p>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 p-5 overflow-y-auto space-y-4">
            {messages.map(m => (
              <div key={m.id} className={`flex flex-col ${m.isMe ? "items-end" : "items-start"}`}>
                <div className={`max-w-md p-3.5 rounded-2xl text-xs leading-relaxed ${
                  m.isMe ? "bg-emerald-600 text-white rounded-br-none shadow" : "bg-slate-800 text-slate-200 rounded-bl-none border border-[var(--border)]"
                }`}>
                  <span className="font-bold block mb-1 text-[10px] opacity-80">{m.sender}</span>
                  {m.text}
                </div>
                <span className="text-[10px] text-[var(--text-muted)] mt-1 px-1">{m.time}</span>
              </div>
            ))}
          </div>

          {/* Chat Input */}
          <form onSubmit={sendMessage} className="p-4 border-t border-[var(--border)] flex gap-2 bg-slate-900/50">
            <input
              type="text"
              placeholder="Type your medical query for Hakeem Dr. Irfan Ashraf..."
              value={input}
              onChange={e => setInput(e.target.value)}
              className="flex-1 bg-slate-800 border border-[var(--border)] rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
            <button
              type="submit"
              className="px-5 py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-bold text-xs rounded-xl shadow transition"
            >
              Send Message
            </button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
