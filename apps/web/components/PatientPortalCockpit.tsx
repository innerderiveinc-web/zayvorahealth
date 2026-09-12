"use client";

import React, { useState, useEffect } from "react";
import {
  portalApi,
  type TodaySchedule,
  type PortalMessage,
} from "@/lib/portalApi";

interface PatientPortalCockpitProps {
  token: string;
  patientId: string;
  patientName: string;
}

export function PatientPortalCockpit({
  token,
  patientId,
  patientName,
}: PatientPortalCockpitProps) {
  const [schedule, setSchedule] = useState<TodaySchedule | null>(null);
  const [messages, setMessages] = useState<PortalMessage[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Message compose
  const [newMessageText, setNewMessageText] = useState("");
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    loadData();
  }, [token, patientId]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [sched, msgs] = await Promise.all([
        portalApi.getTodaySchedule(token, patientId),
        portalApi.getMessages(token, patientId),
      ]);
      setSchedule(sched);
      setMessages(msgs);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStatusChange = async (
    itemType: string,
    itemId: string,
    slotName: string,
    newStatus: "TAKEN" | "MISSED" | "SKIPPED"
  ) => {
    if (!schedule) return;

    // Optimistic UI update
    const updatedSlots = schedule.slots.map((slot) => {
      if (slot.slot_name === slotName) {
        return {
          ...slot,
          items: slot.items.map((it) => (it.item_id === itemId ? { ...it, adherence_status: newStatus } : it)),
        };
      }
      return slot;
    });

    setSchedule({ ...schedule, slots: updatedSlots });

    try {
      await portalApi.logAdherence(token, {
        patient_id: patientId,
        item_type: itemType,
        item_id: itemId,
        timing_slot: slotName,
        status: newStatus,
      });
    } catch (err) {
      console.error("Adherence log error", err);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessageText.trim()) return;

    setIsSending(true);
    try {
      const sent = await portalApi.sendMessage(token, {
        patient_id: patientId,
        sender_type: "CLINICIAN",
        message_body: newMessageText.trim(),
      });
      setMessages((prev) => [...prev, sent]);
      setNewMessageText("");
    } catch (err) {
      console.error(err);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="zv-panel p-5 bg-[#121712] border border-[#24302a] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">📱</span>
            <h2 className="text-base font-serif font-semibold text-[#e3c884]">
              Patient App 2.0 — Daily Schedule & Adherence
            </h2>
            <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-[#182a1d] text-[#2ea87f] border border-[#2ea87f]/40">
              Horizon 5 Client Tier
            </span>
          </div>
          <p className="text-xs text-[#8a9490] mt-1">
            Synchronized patient view: Posology timing slots, canonical vehicles (*Anupan*), and clinical chat for{" "}
            <span className="text-[#ece8dd] font-medium">{patientName}</span>.
          </p>
        </div>

        {schedule && (
          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-[11px] text-[#8a9490] block">Rolling 7-Day Adherence</span>
              <span className="text-base font-mono font-bold text-[#2ea87f]">
                {schedule.overall_7d_adherence_pct}%
              </span>
            </div>
            <div className="w-16 h-2 bg-[#1b261e] rounded-full overflow-hidden border border-[#2ea87f]/40">
              <div
                className="h-full bg-[#2ea87f]"
                style={{ width: `${schedule.overall_7d_adherence_pct}%` }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Daily Schedule */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
              <span>⏰</span> Today’s Clinical Schedule
            </h3>
            <span className="text-xs text-[#8a9490]">
              Date: {schedule?.schedule_date || "Today"}
            </span>
          </div>

          {schedule?.slots.map((slot, idx) => (
            <div
              key={idx}
              className="zv-panel p-4 bg-[#121712] border border-[#24302a] space-y-3"
            >
              <div className="flex items-center justify-between border-b border-[#1e2922] pb-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-[#2ea87f]">
                    {slot.slot_name}
                  </span>
                  <span className="text-xs text-[#8a9490]">({slot.scheduled_time})</span>
                </div>
                <span className="text-[11px] text-[#8a9490]">
                  {slot.items.length} {slot.items.length === 1 ? "Item" : "Items"}
                </span>
              </div>

              <div className="space-y-3">
                {slot.items.map((item) => (
                  <div
                    key={item.item_id}
                    className="p-3 bg-[#0d130f] rounded border border-[#1b241d] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-[#ece8dd] text-sm">
                          {item.display_name}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#18231c] text-[#e3c884] font-mono uppercase">
                          {item.item_type}
                        </span>
                      </div>
                      <p className="text-[#8a9490]">
                        <strong>Dose & Form:</strong> {item.dosage_and_form}
                      </p>
                      <p className="text-[#2ea87f]">
                        <strong>Vehicle (Anupan):</strong> {item.anupan_vehicle}
                      </p>
                      <p className="text-[#8a9490] text-[11px] italic">
                        {item.instructions}
                      </p>
                    </div>

                    <div className="flex sm:flex-col items-center sm:items-end gap-2">
                      <span
                        className={`px-2 py-0.5 text-[10px] font-semibold rounded ${
                          item.adherence_status === "TAKEN"
                            ? "bg-[#182a1d] text-[#2ea87f]"
                            : item.adherence_status === "MISSED"
                            ? "bg-[#331c17] text-[#e06c75]"
                            : "bg-[#252422] text-[#8a9490]"
                        }`}
                      >
                        {item.adherence_status}
                      </span>

                      <div className="flex items-center gap-1">
                        <button
                          onClick={() =>
                            handleStatusChange(item.item_type, item.item_id, slot.slot_name, "TAKEN")
                          }
                          className="px-2 py-1 text-[10px] rounded bg-[#1f3326] text-[#2ea87f] hover:bg-[#284433] transition cursor-pointer"
                        >
                          Taken
                        </button>
                        <button
                          onClick={() =>
                            handleStatusChange(item.item_type, item.item_id, slot.slot_name, "SKIPPED")
                          }
                          className="px-2 py-1 text-[10px] rounded bg-[#2a2419] text-[#e3c884] hover:bg-[#382f1f] transition cursor-pointer"
                        >
                          Skip
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* Dietary Guidance */}
          {schedule?.dietary_guidelines && (
            <div className="zv-panel p-4 bg-[#141b15] border border-[#2ea87f]/30 space-y-2 text-xs">
              <span className="font-serif font-semibold text-[#e3c884] block">
                🥗 Prescribed Ilaj-bil-Ghiza (Dietary Instructions)
              </span>
              <ul className="list-disc list-inside space-y-1 text-[#ece8dd]">
                {schedule.dietary_guidelines.map((rule, idx) => (
                  <li key={idx}>{rule}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Right 1 Col: Asynchronous Patient Chat */}
        <div className="zv-panel p-5 flex flex-col h-[560px] bg-[#121712] border border-[#24302a]">
          <div className="border-b border-[#24302a] pb-3 mb-3">
            <h3 className="text-sm font-serif font-semibold text-[#e3c884] flex items-center gap-2">
              <span>💬</span> Clinician-Patient Chat
            </h3>
            <span className="text-[10px] text-[#8a9490]">Automated Triage & Emergency Redirection</span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 pr-1 text-xs">
            {messages.map((msg) => (
              <div
                key={msg.message_id}
                className={`p-3 rounded-lg border text-xs space-y-1 ${
                  msg.sender_type === "CLINICIAN"
                    ? "bg-[#18231c] border-[#2ea87f]/30 text-[#ece8dd] ml-4"
                    : "bg-[#181d19] border-[#24302a] text-[#ece8dd] mr-4"
                }`}
              >
                <div className="flex items-center justify-between text-[10px] text-[#8a9490]">
                  <span className="font-semibold text-[#e3c884]">{msg.sender_type}</span>
                  <span>{new Date(msg.timestamp_utc).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
                <p>{msg.message_body}</p>
                {msg.triage_status === "EMERGENCY_REDIRECT" && (
                  <span className="inline-block mt-1 px-1.5 py-0.5 text-[9px] font-bold rounded bg-[#451616] text-[#e06c75]">
                    EMERGENCY TRIAGE
                  </span>
                )}
              </div>
            ))}
          </div>

          <form onSubmit={handleSendMessage} className="mt-3 pt-3 border-t border-[#24302a] flex gap-2">
            <input
              type="text"
              value={newMessageText}
              onChange={(e) => setNewMessageText(e.target.value)}
              placeholder="Send instruction to patient..."
              className="zv-input text-xs flex-1"
            />
            <button
              type="submit"
              disabled={isSending || !newMessageText.trim()}
              className="zv-btn-primary px-3 py-1.5 text-xs font-semibold"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
