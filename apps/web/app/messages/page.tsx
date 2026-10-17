"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

interface Message {
  id: string;
  senderId: string;
  senderName: string;
  senderRole: "doctor" | "patient" | "nurse" | "pharmacist";
  text: string;
  timestamp: string;
  isSelf: boolean;
  isClinicalNote?: boolean;
}

interface Conversation {
  id: string;
  participantName: string;
  participantRole: string;
  participantAvatar: string;
  mrn?: string;
  mizaj?: string;
  unreadCount: number;
  lastMessage: string;
  lastMessageTime: string;
  online: boolean;
  category: "patient" | "team" | "urgent";
}

const INITIAL_CONVERSATIONS: Conversation[] = [
  {
    id: "conv-1",
    participantName: "Hamza Farooqi",
    participantRole: "Patient • Waja-ul-Mafasil",
    participantAvatar: "HF",
    mrn: "MRN-2026-0814",
    mizaj: "Barid Balghami",
    unreadCount: 2,
    lastMessage: "Doctor sahab, knee stiffness is much less today after day 3 of warm Roghan-e-Babbuna massage.",
    lastMessageTime: "10:42 AM",
    online: true,
    category: "patient",
  },
  {
    id: "conv-2",
    participantName: "Ayesha Siddiqui",
    participantRole: "Patient • PCOS & Insulin Resistance",
    participantAvatar: "AS",
    mrn: "MRN-2026-0921",
    mizaj: "Har Safrawi",
    unreadCount: 0,
    lastMessage: "Uploaded fasting lipid profile and LH/FSH report from Lal Pathlabs.",
    lastMessageTime: "Yesterday",
    online: false,
    category: "patient",
  },
  {
    id: "conv-3",
    participantName: "Zainab Ali (Chief Pharmacist)",
    participantRole: "Dispensary • Mudabbar Gate",
    participantAvatar: "ZA",
    unreadCount: 1,
    lastMessage: "Batch B2-2026 Suranjan Talkh verified. Mudabbar Certificate uploaded to audit ledger.",
    lastMessageTime: "09:15 AM",
    online: true,
    category: "team",
  },
  {
    id: "conv-4",
    participantName: "Sana Khan (OPD Reception)",
    participantRole: "Reception Desk • Token Counter",
    participantAvatar: "SK",
    unreadCount: 0,
    lastMessage: "Token T-104 Hamza Farooqi has checked in and is seated in Waiting Area 2.",
    lastMessageTime: "10:15 AM",
    online: true,
    category: "team",
  },
  {
    id: "conv-5",
    participantName: "Bilal Ahmad",
    participantRole: "Patient • Zo'f-e-Kabid",
    participantAvatar: "BA",
    mrn: "MRN-2026-0744",
    mizaj: "Har Damawi",
    unreadCount: 0,
    lastMessage: "Can I take Majun Dabeed-ul-Ward with lukewarm water before breakfast?",
    lastMessageTime: "Sep 14",
    online: false,
    category: "patient",
  },
];

const INITIAL_MESSAGES: Record<string, Message[]> = {
  "conv-1": [
    {
      id: "m-1",
      senderId: "pat-1",
      senderName: "Hamza Farooqi",
      senderRole: "patient",
      text: "Assalamu Alaikum Doctor Sahab. I started the prescribed medicines yesterday evening.",
      timestamp: "Yesterday, 06:30 PM",
      isSelf: false,
    },
    {
      id: "m-2",
      senderId: "dr-1",
      senderName: "Dr. Irfan Ashraf",
      senderRole: "doctor",
      text: "Wa Alaikum Assalam Hamza. Excellent. Remember to follow the dietary guidelines: strict restriction on cold, fermented foods (Balgham-inducing diet). Lukewarm water only.",
      timestamp: "Yesterday, 07:10 PM",
      isSelf: true,
      isClinicalNote: true,
    },
    {
      id: "m-3",
      senderId: "pat-1",
      senderName: "Hamza Farooqi",
      senderRole: "patient",
      text: "Doctor sahab, knee stiffness is much less today after day 3 of warm Roghan-e-Babbuna massage.",
      timestamp: "10:42 AM",
      isSelf: false,
    },
    {
      id: "m-4",
      senderId: "pat-1",
      senderName: "Hamza Farooqi",
      senderRole: "patient",
      text: "Should I continue the Arq-e-Badiyan 25ml twice daily or increase the dose?",
      timestamp: "10:44 AM",
      isSelf: false,
    },
  ],
};

export default function MessagesPage() {
  const [conversations, setConversations] = useState<Conversation[]>(INITIAL_CONVERSATIONS);
  const [selectedConvId, setSelectedConvId] = useState<string>("conv-1");
  const [messages, setMessages] = useState<Record<string, Message[]>>(INITIAL_MESSAGES);
  const [inputText, setInputText] = useState("");
  const [filterCategory, setFilterCategory] = useState<"all" | "patient" | "team">("all");
  const [searchQuery, setSearchQuery] = useState("");

  const activeConv = conversations.find((c) => c.id === selectedConvId) || conversations[0];
  const activeMessages = messages[selectedConvId] || [];

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const newMsg: Message = {
      id: "msg-" + Date.now(),
      senderId: "dr-current",
      senderName: "Dr. Irfan Ashraf",
      senderRole: "doctor",
      text: inputText.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      isSelf: true,
    };

    setMessages((prev) => ({
      ...prev,
      [selectedConvId]: [...(prev[selectedConvId] || []), newMsg],
    }));

    setConversations((prev) =>
      prev.map((c) =>
        c.id === selectedConvId
          ? { ...c, lastMessage: newMsg.text, lastMessageTime: "Just now", unreadCount: 0 }
          : c
      )
    );

    setInputText("");
  };

  const handleInsertTemplate = (templateText: string) => {
    setInputText((prev) => (prev ? `${prev} ${templateText}` : templateText));
  };

  const filteredConversations = conversations.filter((c) => {
    const matchesCat = filterCategory === "all" || c.category === filterCategory;
    const matchesSearch =
      c.participantName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.lastMessage.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.mrn && c.mrn.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCat && matchesSearch;
  });

  return (
    <AppShell activeRole="doctor">
      <div className="flex flex-col h-[calc(100vh-8.5rem)] min-h-[550px] -m-4 sm:-m-6 bg-[var(--background)]">
        
        {/* Top Header Bar */}
        <div className="px-4 py-3 border-b border-[var(--border)] bg-[var(--panel)] flex flex-wrap items-center justify-between gap-3 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 text-base">
              💬
            </div>
            <div>
              <h1 className="text-sm font-bold text-white tracking-tight flex items-center gap-2">
                Clinical Messages & Care Team Outreach
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-[10px] font-mono">
                  Encrypted & ABDM Compliant
                </span>
              </h1>
              <p className="text-[11px] text-[var(--muted)]">
                Direct secure channel between clinicians, registered patients, pharmacy staff, and care coordinators.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <Link
              href="/telemedicine"
              className="px-3 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold flex items-center gap-1.5 transition"
            >
              <span>📹</span> Start Telemedicine
            </Link>
            <Link
              href="/doctor/calendar"
              className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-[var(--muted)] hover:text-white font-medium border border-[var(--border)] transition"
            >
              <span>📅</span> Schedule Visit
            </Link>
          </div>
        </div>

        {/* Messaging Workspace Grid */}
        <div className="flex-1 flex overflow-hidden">
          
          {/* Left Panel: Conversation List (320px) */}
          <div className="w-80 border-r border-[var(--border)] bg-[var(--panel)] flex flex-col shrink-0">
            
            {/* Search & Filter Bar */}
            <div className="p-3 border-b border-[var(--border)] space-y-2">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search chats, patients, MRN..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-[var(--background)] border border-[var(--border)] rounded-xl px-3 py-1.5 pl-8 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
                />
                <span className="absolute left-2.5 top-2 text-[var(--muted)] text-xs">🔍</span>
              </div>

              {/* Filter Tabs */}
              <div className="flex items-center bg-[var(--background)] p-0.5 rounded-lg border border-[var(--border)] text-[11px]">
                <button
                  onClick={() => setFilterCategory("all")}
                  className={`flex-1 py-1 rounded text-center font-medium transition ${
                    filterCategory === "all" ? "bg-[var(--elevated)] text-teal-300 font-bold" : "text-[var(--muted)] hover:text-white"
                  }`}
                >
                  All ({conversations.length})
                </button>
                <button
                  onClick={() => setFilterCategory("patient")}
                  className={`flex-1 py-1 rounded text-center font-medium transition ${
                    filterCategory === "patient" ? "bg-[var(--elevated)] text-teal-300 font-bold" : "text-[var(--muted)] hover:text-white"
                  }`}
                >
                  Patients
                </button>
                <button
                  onClick={() => setFilterCategory("team")}
                  className={`flex-1 py-1 rounded text-center font-medium transition ${
                    filterCategory === "team" ? "bg-[var(--elevated)] text-teal-300 font-bold" : "text-[var(--muted)] hover:text-white"
                  }`}
                >
                  Care Team
                </button>
              </div>
            </div>

            {/* List */}
            <div className="flex-1 overflow-y-auto divide-y divide-[var(--border)]">
              {filteredConversations.map((conv) => {
                const isSelected = conv.id === selectedConvId;
                return (
                  <button
                    key={conv.id}
                    onClick={() => setSelectedConvId(conv.id)}
                    className={`w-full text-left p-3 flex items-start gap-3 transition ${
                      isSelected
                        ? "bg-teal-500/10 border-l-4 border-l-teal-500 text-white"
                        : "hover:bg-[var(--elevated)] text-[var(--text)]"
                    }`}
                  >
                    <div className="relative shrink-0">
                      <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 text-teal-300 font-bold flex items-center justify-center text-xs">
                        {conv.participantAvatar}
                      </div>
                      {conv.online && (
                        <span className="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-2 ring-[var(--panel)]"></span>
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-0.5">
                        <span className="text-xs font-bold text-white truncate">{conv.participantName}</span>
                        <span className="text-[10px] text-[var(--muted)] shrink-0">{conv.lastMessageTime}</span>
                      </div>
                      <div className="text-[11px] text-[var(--muted)] truncate mb-1">{conv.participantRole}</div>
                      <p className="text-[11px] text-[var(--muted)] line-clamp-1 leading-snug">
                        {conv.lastMessage}
                      </p>

                      {conv.mrn && (
                        <div className="flex items-center gap-1.5 mt-1 text-[9px]">
                          <span className="font-mono bg-[var(--background)] px-1.5 py-0.2 rounded border border-[var(--border)] text-teal-300">
                            {conv.mrn}
                          </span>
                          {conv.mizaj && (
                            <span className="text-emerald-400 bg-emerald-500/10 px-1.5 py-0.2 rounded border border-emerald-500/20">
                              {conv.mizaj}
                            </span>
                          )}
                        </div>
                      )}
                    </div>

                    {conv.unreadCount > 0 && (
                      <span className="shrink-0 w-5 h-5 rounded-full bg-teal-500 text-slate-950 font-bold text-[10px] flex items-center justify-center">
                        {conv.unreadCount}
                      </span>
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Center/Right Panel: Active Conversation Thread */}
          <div className="flex-1 flex flex-col bg-[var(--background)] overflow-hidden">
            
            {/* Conversation Top Context Bar */}
            <div className="p-3 px-4 border-b border-[var(--border)] bg-[var(--panel)] flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 text-teal-300 font-bold flex items-center justify-center text-xs">
                  {activeConv.participantAvatar}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xs font-bold text-white">{activeConv.participantName}</h2>
                    {activeConv.online ? (
                      <span className="text-[10px] text-emerald-400 flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Online
                      </span>
                    ) : (
                      <span className="text-[10px] text-[var(--muted)]">Offline</span>
                    )}
                  </div>
                  <p className="text-[10px] text-[var(--muted)]">{activeConv.participantRole}</p>
                </div>
              </div>

              {/* Patient Quick Action Pills */}
              <div className="flex items-center gap-2 text-xs">
                {activeConv.mrn && (
                  <>
                    <Link
                      href="/doctor/patients"
                      className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-[var(--muted)] hover:text-white text-[11px] transition"
                    >
                      📋 EMR 360
                    </Link>
                    <Link
                      href="/doctor/nuskha"
                      className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-teal-300 hover:text-teal-200 text-[11px] transition"
                    >
                      📝 Author Rx
                    </Link>
                    <Link
                      href="/telemedicine"
                      className="px-2.5 py-1 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-[11px] flex items-center gap-1 transition"
                    >
                      <span>📹</span> Video Call
                    </Link>
                  </>
                )}
              </div>
            </div>

            {/* Messages Scroll Area */}
            <div className="flex-1 p-4 overflow-y-auto space-y-3">
              <div className="text-center my-2">
                <span className="text-[10px] text-[var(--muted)] bg-[var(--panel)] px-3 py-1 rounded-full border border-[var(--border)]">
                  Messages are end-to-end encrypted under 21 CFR Part 11 and ISO 27001
                </span>
              </div>

              {activeMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex flex-col ${msg.isSelf ? "items-end" : "items-start"}`}
                >
                  <div className="flex items-center gap-1.5 mb-1 px-1">
                    <span className="text-[10px] font-bold text-slate-400">{msg.senderName}</span>
                    <span className="text-[9px] text-[var(--muted)]">{msg.timestamp}</span>
                    {msg.isClinicalNote && (
                      <span className="px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 text-[9px] font-bold">
                        Clinical Advisory
                      </span>
                    )}
                  </div>

                  <div
                    className={`max-w-lg p-3 rounded-2xl text-xs leading-relaxed ${
                      msg.isSelf
                        ? "bg-teal-700/80 text-white rounded-br-xs border border-teal-600/40"
                        : "bg-[var(--panel)] text-[var(--text)] rounded-bl-xs border border-[var(--border)]"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Clinical Quick Responses / Suggestion Pills */}
            <div className="px-4 py-2 bg-[var(--panel)] border-t border-[var(--border)] flex items-center gap-1.5 overflow-x-auto text-[10px]">
              <span className="text-[var(--muted)] shrink-0 font-bold">Quick Templates:</span>
              <button
                onClick={() => handleInsertTemplate("Continue current dosage for 5 more days and report morning fasting pulse.")}
                className="px-2 py-1 rounded-lg bg-[var(--background)] hover:bg-[var(--elevated)] border border-[var(--border)] text-[var(--muted)] hover:text-white shrink-0 transition"
              >
                + Dosage Confirmation
              </button>
              <button
                onClick={() => handleInsertTemplate("Strict parhez: avoid sour, fried, and cold items to prevent Balgham aggravation.")}
                className="px-2 py-1 rounded-lg bg-[var(--background)] hover:bg-[var(--elevated)] border border-[var(--border)] text-[var(--muted)] hover:text-white shrink-0 transition"
              >
                + Dietetic Parhez
              </button>
              <button
                onClick={() => handleInsertTemplate("Please upload latest Kidney Function & Serum Uric Acid reports before next visit.")}
                className="px-2 py-1 rounded-lg bg-[var(--background)] hover:bg-[var(--elevated)] border border-[var(--border)] text-[var(--muted)] hover:text-white shrink-0 transition"
              >
                + Request Lab Report
              </button>
              <button
                onClick={() => handleInsertTemplate("Token confirmed. Please take seat outside OPD Room 3 for physical pulse examination.")}
                className="px-2 py-1 rounded-lg bg-[var(--background)] hover:bg-[var(--elevated)] border border-[var(--border)] text-[var(--muted)] hover:text-white shrink-0 transition"
              >
                + OPD Token Callout
              </button>
            </div>

            {/* Input Composer Form */}
            <form onSubmit={handleSendMessage} className="p-3 border-t border-[var(--border)] bg-[var(--panel)] flex items-center gap-2">
              <input
                type="text"
                placeholder={`Reply to ${activeConv.participantName}... (Press Enter to send)`}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="flex-1 bg-[var(--background)] border border-[var(--border)] rounded-xl px-4 py-2.5 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
              />
              <button
                type="submit"
                className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition"
              >
                <span>Send</span>
                <span>📤</span>
              </button>
            </form>

          </div>
        </div>

      </div>
    </AppShell>
  );
}
