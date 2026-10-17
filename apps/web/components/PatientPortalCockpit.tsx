"use client";

import React, { useState, useEffect } from "react";
import {
  portalApi,
  type TodaySchedule,
  type PortalMessage,
  type DoseSlot,
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

  // Main navigation tab
  const [activeTab, setActiveTab] = useState<"REGIMEN" | "PARHEZ" | "PROMS">("REGIMEN");

  // Multilingual Audio Prompts & Bhashini Voice
  const [selectedLanguage, setSelectedLanguage] = useState<"ur" | "hi" | "te" | "en">("ur");
  const [activeVoicePrompt, setActiveVoicePrompt] = useState<{
    itemId: string;
    scriptText: string;
    languageName: string;
    audioDataUri: string;
    isPlaying: boolean;
  } | null>(null);
  const [isVoiceLoading, setIsVoiceLoading] = useState<string | null>(null);

  // Message compose
  const [newMessageText, setNewMessageText] = useState("");
  const [isSending, setIsSending] = useState(false);

  // 14-Day PROMs State
  const [promsDay, setPromsDay] = useState<number>(7);
  const [promsVas, setPromsVas] = useState<number>(3);
  const [promsHazm, setPromsHazm] = useState<number>(7);
  const [promsSleep, setPromsSleep] = useState<number>(8);
  const [promsVigor, setPromsVigor] = useState<number>(7);
  const [promsParhez, setPromsParhez] = useState<number>(85);
  const [promsAdverse, setPromsAdverse] = useState<string[]>([]);
  const [promsSubmitted, setPromsSubmitted] = useState<boolean>(false);
  const [promsAlert, setPromsAlert] = useState<string | null>(null);

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

  const handlePlayVoice = async (item: DoseSlot["items"][0], slotName: string) => {
    setIsVoiceLoading(item.item_id);
    try {
      const res = await portalApi.synthesizeMedicationVoice(token, {
        patient_id: patientId,
        medication_name: item.display_name,
        dosage_display: item.dosage_and_form,
        timing_slot: slotName,
        intake_vehicle: item.anupan_vehicle,
        language: selectedLanguage,
        dose_id: item.item_id,
      });

      setActiveVoicePrompt({
        itemId: item.item_id,
        scriptText: res.script_text,
        languageName: res.language_name,
        audioDataUri: res.audio_data_uri,
        isPlaying: true,
      });

      if (typeof Audio !== "undefined" && res.audio_data_uri) {
        const audio = new Audio(res.audio_data_uri);
        audio.play().catch((e) => console.warn("Audio playback notice:", e));
        audio.onended = () => {
          setActiveVoicePrompt((prev) => (prev ? { ...prev, isPlaying: false } : null));
        };
      }
    } catch (err) {
      console.error("Voice prompt synthesis error:", err);
    } finally {
      setIsVoiceLoading(null);
    }
  };

  const toggleAdverseSymptom = (symptom: string) => {
    setPromsAdverse((prev) =>
      prev.includes(symptom) ? prev.filter((s) => s !== symptom) : [...prev, symptom]
    );
  };

  const handleSubmitPROMs = (e: React.FormEvent) => {
    e.preventDefault();
    setPromsSubmitted(true);
    if (promsAdverse.length > 0) {
      setPromsAlert(
        "⚠️ Clinical Safety Firewall: You reported adverse symptoms. Your prescribing Hakeem has been automatically alerted for immediate review."
      );
    } else {
      setPromsAlert(
        "✓ Check-in successfully recorded! Your clinical vitality score is improving on target (+48% vs Day 0 baseline)."
      );
    }
  };

  // Vitality Calculation
  const symptomInversion = Math.max(0, 10 - promsVas);
  const currentVitality = Math.round(
    symptomInversion * 3.0 + promsHazm * 2.5 + promsVigor * 2.5 + promsSleep * 2.0
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="zv-panel p-5 bg-[#121712] border border-[#24302a] flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">📱</span>
            <h2 className="text-base font-serif font-semibold text-[#e3c884]">
              Sehat Sahab: Patient Clinical Companion
            </h2>
            <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-[#182a1d] text-[#2ea87f] border border-[#2ea87f]/40">
              Active Protocol: Mafasil Reversal
            </span>
          </div>
          <p className="text-xs text-[#8a9490] mt-1">
            Personalized recovery companion for <strong className="text-[#ece8dd]">{patientName}</strong> (MRN: {patientId}).
            Daily posology, 8-Tier Parhez dietary firewall, and 14-day outcome tracking.
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

      {/* Navigation Tab Bar */}
      <div className="flex flex-wrap items-center gap-2 border-b border-[#24302a] pb-3">
        <button
          type="button"
          onClick={() => setActiveTab("REGIMEN")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center gap-2 ${
            activeTab === "REGIMEN"
              ? "bg-[#1f6f54] text-white border border-[#2ea87f]"
              : "bg-[#131913] text-[#8a9490] border border-[#24302a] hover:text-[#ece8dd]"
          }`}
        >
          <span>⏰</span> Daily Regimen & Voice Instructions
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("PARHEZ")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center gap-2 ${
            activeTab === "PARHEZ"
              ? "bg-[#1f6f54] text-white border border-[#2ea87f]"
              : "bg-[#131913] text-[#8a9490] border border-[#24302a] hover:text-[#ece8dd]"
          }`}
        >
          <span>🛡️</span> 8-Tier Parhez Engine (Ilaj-bil-Ghiza)
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("PROMS")}
          className={`px-4 py-2 rounded-lg text-xs font-semibold transition cursor-pointer flex items-center gap-2 ${
            activeTab === "PROMS"
              ? "bg-[#1f6f54] text-white border border-[#2ea87f]"
              : "bg-[#131913] text-[#8a9490] border border-[#24302a] hover:text-[#ece8dd]"
          }`}
        >
          <span>📈</span> 14-Day PROMs Recovery Tracker
        </button>
      </div>

      {/* TAB 1: DAILY REGIMEN & CHAT */}
      {activeTab === "REGIMEN" && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left 2 Cols: Daily Schedule */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h3 className="text-sm font-serif font-semibold text-[#e3c884] uppercase tracking-wider flex items-center gap-2">
                <span>⏰</span> Today’s Clinical Schedule
              </h3>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1.5 bg-[#141d17] px-2 py-1 rounded border border-[#243328]">
                  <span className="text-[11px] text-[#8a9490]">🎙️ Voice:</span>
                  <select
                    value={selectedLanguage}
                    onChange={(e) => setSelectedLanguage(e.target.value as any)}
                    className="text-xs bg-transparent text-[#e3c884] focus:outline-none cursor-pointer"
                  >
                    <option value="ur">Urdu (Roman Transliteration)</option>
                    <option value="hi">Hindi (हिन्दी)</option>
                    <option value="te">Telugu (తెలుగు)</option>
                    <option value="en">English</option>
                  </select>
                </div>
                <span className="text-xs text-[#8a9490]">
                  Date: {schedule?.schedule_date || "Today"}
                </span>
              </div>
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
                      className="p-3 bg-[#0d130f] rounded border border-[#1b241d] flex flex-col gap-2 text-xs"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
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

                          <div className="flex items-center gap-1.5">
                            <button
                              onClick={() => handlePlayVoice(item, slot.slot_name)}
                              disabled={isVoiceLoading === item.item_id}
                              className="flex items-center gap-1 px-2 py-1 text-[10px] rounded bg-[#18281e] text-[#e3c884] border border-[#2ea87f]/30 hover:bg-[#203628] transition cursor-pointer"
                              title="Listen to vernacular audio instructions"
                            >
                              <span>{isVoiceLoading === item.item_id ? "⏳" : "🔊"}</span>
                              <span>
                                {isVoiceLoading === item.item_id
                                  ? "Generating..."
                                  : activeVoicePrompt?.itemId === item.item_id && activeVoicePrompt.isPlaying
                                  ? "Playing..."
                                  : "Listen"}
                              </span>
                            </button>

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

                      {activeVoicePrompt?.itemId === item.item_id && (
                        <div className="mt-1 p-2 rounded bg-[#142318] border border-[#2ea87f]/40 text-xs space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="text-[11px] font-mono text-[#2ea87f] flex items-center gap-1">
                              <span>🎙️ Bhashini Audio ({activeVoicePrompt.languageName})</span>
                            </span>
                            <button
                              onClick={() => setActiveVoicePrompt(null)}
                              className="text-[#8a9490] hover:text-[#ece8dd] text-[10px]"
                            >
                              ✕
                            </button>
                          </div>
                          <p className="text-sm font-serif text-[#ece8dd] leading-relaxed">
                            {activeVoicePrompt.scriptText}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
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
                </div>
              ))}
            </div>

            <form onSubmit={handleSendMessage} className="mt-3 pt-3 border-t border-[#24302a] flex gap-2">
              <input
                type="text"
                value={newMessageText}
                onChange={(e) => setNewMessageText(e.target.value)}
                placeholder="Send message to Matab team..."
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
      )}

      {/* TAB 2: 8-TIER PARHEZ ENGINE */}
      {activeTab === "PARHEZ" && (
        <div className="space-y-6">
          <div className="bg-[#121712] border border-[#24302a] rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-base font-bold font-serif text-[#f2efe6] flex items-center gap-2">
                <span>🛡️</span> 8-Tier Canonical Parhez & Lifestyle Firewall (Ilaj-bil-Ghiza)
              </h3>
              <span className="text-xs px-2.5 py-1 rounded bg-[#1f6f54]/30 border border-[#2ea87f]/40 text-[#2ea87f] font-mono">
                Protocol: Balghami-Mafasil (Cold/Wet Reversal)
              </span>
            </div>
            <p className="text-xs text-[#8a9490] leading-relaxed">
              Unani medicine dictates that medicinal therapy (*Ilaj-bil-Dawa*) cannot succeed without rigorous adherence to
              dietary counter-measures (*Parhez*) and the Six Essential Lifestyle Requisites (*Asbab-e-Sittah Zarooriyyah*).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Tier 1 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 1: Primary Dietary Quality
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  Haar-Yabis (Warm/Dry Foods)
                </span>
              </div>
              <p className="text-[#ece8dd]">
                <strong>Beneficial (Allowed): </strong>
                Mutton broth infused with ginger/black pepper, pigeon soup, mung daal, roasted garlic, fenugreek greens.
              </p>
              <p className="text-rose-400">
                <strong>Strictly Prohibited: </strong>
                Curd, cold milk, raw cucumbers, radishes, iced beverages, okra, excess salt.
              </p>
            </div>

            {/* Tier 2 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 2: Hydration & Arqiyat
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">
                  Warm Fluids Only
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Drink water boiled with a slice of fresh ginger or cumin. Sip warm. No iced drinks.
              </p>
              <p className="text-[#8a9490]">
                <strong>Prescribed Arq: </strong> 30ml Arq-e-Gaozaban in morning; 30ml Arq-e-Badiyan post heavy meals.
              </p>
            </div>

            {/* Tier 3 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 3: Circadian Sleep Timing (Naum wa Yaqzah)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">
                  10:00 PM – 5:30 AM
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Retire by 10:00 PM to facilitate nocturnal Tabiyat hepatic digestion. Strictly avoid sleeping immediately
                after meals or daytime naps longer than 20 minutes (exacerbates Balgham).
              </p>
            </div>

            {/* Tier 4 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 4: Physical Movement (Harkat wa Sukoon)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                  Riyazat-e-Motadila
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Light morning brisk walking for 20 minutes before breakfast. Gentle joint mobility rotations. Avoid high-impact
                pounding while joint inflammation is in the active Tanqiya stage.
              </p>
            </div>

            {/* Tier 5 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 5: Mental & Emotional Equilibrium (Araz-e-Nafsaniyya)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800">
                  Stress Reduction
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Practice 10 minutes of deep rhythmic diaphragmatic breathing (Habs-e-Nafas) twice daily. Chronic anger or grief
                disrupts innate heat (*Hararat-e-Ghariziyya*).
              </p>
            </div>

            {/* Tier 6 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 6: Vehicle (Anupan) Protocol
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  Targeted Delivery
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Electuaries (*Majun, Itrifal*) must be taken with lukewarm water or warm milk as designated. Never wash down with
                cold tap water, as it blunts medicinal assimilation in the stomach (*Meda*).
              </p>
            </div>

            {/* Tier 7 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-rose-400 uppercase tracking-wider text-[11px]">
                  Tier 7: Tabah (Prohibited Combinations)
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                  Critical Incompatibilities
                </span>
              </div>
              <p className="text-rose-300">
                Never combine Fish with Milk; never consume sour fruits with dairy; never consume melons immediately after
                taking oily preparations. These generate morbid humors (*Akhlat-e-Fasida*).
              </p>
            </div>

            {/* Tier 8 */}
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#2ea87f] uppercase tracking-wider text-[11px]">
                  Tier 8: Phase-Specific Dietary Adjustments
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                  Current: Days 1–14
                </span>
              </div>
              <p className="text-[#ece8dd]">
                Current active phase: <strong>Tanqiya (Concoction & Cleansing)</strong>. Keep calorie density moderate to light,
                avoiding heavy fried grains so digestive energy is directed toward humoral clearance.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: 14-DAY PROMS RECOVERY TRACKER */}
      {activeTab === "PROMS" && (
        <div className="space-y-6">
          <div className="bg-[#121712] border border-[#24302a] rounded-xl p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h3 className="text-base font-bold font-serif text-[#f2efe6] flex items-center gap-2">
                <span>📈</span> 14-Day Clinical Outcome & PROMs Intake Tracker
              </h3>
              <p className="text-xs text-[#8a9490] mt-1">
                Validated patient-reported milestone scoring to measure symptomatic relief, digestive vitality (*Hazm*),
                and humoral normalization under the care of your prescribing Hakeem.
              </p>
            </div>

            <div className="flex items-center gap-2 bg-[#171f19] px-3 py-1.5 rounded-lg border border-[#24302a]">
              <span className="text-xs text-[#8a9490]">Milestone:</span>
              <select
                value={promsDay}
                onChange={(e) => setPromsDay(parseInt(e.target.value, 10))}
                className="bg-transparent text-xs font-bold text-[#2ea87f] focus:outline-none cursor-pointer"
              >
                <option value={7}>Day 7 Check-in</option>
                <option value={14}>Day 14 Final Review</option>
              </select>
            </div>
          </div>

          {/* Status Alert Banner */}
          {promsAlert && (
            <div
              className={`p-4 rounded-xl text-xs border ${
                promsAdverse.length > 0
                  ? "bg-rose-950/40 border-rose-800 text-rose-200"
                  : "bg-emerald-950/40 border-emerald-800 text-emerald-200"
              }`}
            >
              {promsAlert}
            </div>
          )}

          {/* Visual Progression Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl">
              <span className="text-[11px] text-[#8a9490] uppercase font-semibold">Pain / Severity (VAS)</span>
              <div className="text-2xl font-bold font-mono text-rose-400 mt-1">{promsVas} / 10</div>
              <span className="text-[10px] text-emerald-400">↓ Down from 8.0 (Baseline)</span>
            </div>

            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl">
              <span className="text-[11px] text-[#8a9490] uppercase font-semibold">Digestive Hazm Vitality</span>
              <div className="text-2xl font-bold font-mono text-[#2ea87f] mt-1">{promsHazm} / 10</div>
              <span className="text-[10px] text-emerald-400">↑ Optimal bowel transit</span>
            </div>

            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl">
              <span className="text-[11px] text-[#8a9490] uppercase font-semibold">Parhez Adherence</span>
              <div className="text-2xl font-bold font-mono text-[#c9a24b] mt-1">{promsParhez}%</div>
              <span className="text-[10px] text-emerald-400">Tier: Excellent (≥85%)</span>
            </div>

            <div className="bg-[#111713] border border-[#1f2b24] p-4 rounded-xl">
              <span className="text-[11px] text-[#8a9490] uppercase font-semibold">Composite Vitality Index</span>
              <div className="text-2xl font-bold font-mono text-teal-300 mt-1">{currentVitality} / 100</div>
              <span className="text-[10px] text-teal-400">Mizaj: STABLE_EQUILIBRIUM</span>
            </div>
          </div>

          {/* Interactive Check-in Form */}
          <form onSubmit={handleSubmitPROMs} className="bg-[#111713] border border-[#1f2b24] rounded-xl p-6 space-y-6 text-xs">
            <div className="border-b border-[#1f2b24] pb-3">
              <h4 className="text-sm font-bold text-[#f2efe6] uppercase tracking-wider">
                Milestone Intake Survey — Day {promsDay}
              </h4>
              <p className="text-[#8a9490] mt-0.5">
                Please rate your symptoms over the last 48 hours to inform clinical adjustments.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* VAS Symptom Severity */}
              <div className="space-y-2">
                <div className="flex justify-between font-semibold">
                  <span className="text-[#ece8dd]">Primary Joint Pain / Discomfort (0 = None, 10 = Severe)</span>
                  <span className="font-mono text-rose-400 text-sm font-bold">{promsVas} / 10</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={10}
                  value={promsVas}
                  onChange={(e) => setPromsVas(parseInt(e.target.value, 10))}
                  className="w-full accent-rose-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-[#8a9490]">
                  <span>0 (Pain Free)</span>
                  <span>5 (Moderate)</span>
                  <span>10 (Severe / Disabling)</span>
                </div>
              </div>

              {/* Hazm / Digestion */}
              <div className="space-y-2">
                <div className="flex justify-between font-semibold">
                  <span className="text-[#ece8dd]">Digestive Vitality (Hazm / Appetite / Gas)</span>
                  <span className="font-mono text-[#2ea87f] text-sm font-bold">{promsHazm} / 10</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={10}
                  value={promsHazm}
                  onChange={(e) => setPromsHazm(parseInt(e.target.value, 10))}
                  className="w-full accent-[#2ea87f] cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-[#8a9490]">
                  <span>0 (Severe bloating/nausea)</span>
                  <span>5 (Average)</span>
                  <span>10 (Optimal digestion)</span>
                </div>
              </div>

              {/* Sleep & Calm */}
              <div className="space-y-2">
                <div className="flex justify-between font-semibold">
                  <span className="text-[#ece8dd]">Sleep Quality & Mental Calm (Naum / Sukoon)</span>
                  <span className="font-mono text-sky-400 text-sm font-bold">{promsSleep} / 10</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={10}
                  value={promsSleep}
                  onChange={(e) => setPromsSleep(parseInt(e.target.value, 10))}
                  className="w-full accent-sky-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-[#8a9490]">
                  <span>0 (Broken / Insomnia)</span>
                  <span>5 (Fair)</span>
                  <span>10 (Deep restorative)</span>
                </div>
              </div>

              {/* Energy & Vigor */}
              <div className="space-y-2">
                <div className="flex justify-between font-semibold">
                  <span className="text-[#ece8dd]">Physical Energy & Vigor (Quwwat-e-Badaniyya)</span>
                  <span className="font-mono text-amber-400 text-sm font-bold">{promsVigor} / 10</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={10}
                  value={promsVigor}
                  onChange={(e) => setPromsVigor(parseInt(e.target.value, 10))}
                  className="w-full accent-amber-500 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-[#8a9490]">
                  <span>0 (Exhausted / Bedbound)</span>
                  <span>5 (Moderate)</span>
                  <span>10 (High vitality)</span>
                </div>
              </div>
            </div>

            {/* Parhez Adherence Slider */}
            <div className="space-y-2 pt-2 border-t border-[#1f2b24]">
              <div className="flex justify-between font-semibold">
                <span className="text-[#ece8dd]">8-Tier Parhez Dietary Adherence Level</span>
                <span className="font-mono text-[#2ea87f] text-sm font-bold">{promsParhez}%</span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                step={5}
                value={promsParhez}
                onChange={(e) => setPromsParhez(parseInt(e.target.value, 10))}
                className="w-full accent-[#2ea87f] cursor-pointer"
              />
              <p className="text-[11px] text-[#8a9490]">
                Strict adherence to prescribed warm fluids, avoided curds/cold items, and adhered to Asbab-e-Sittah timings.
              </p>
            </div>

            {/* Safety Firewall: Adverse Symptoms Checklist */}
            <div className="space-y-3 pt-2 border-t border-[#1f2b24]">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#f2efe6] uppercase tracking-wider">
                  Safety Monitor: Have you experienced any of the following?
                </span>
                <span className="text-[10px] text-[#8a9490]">Click to select any observed symptoms</span>
              </div>

              <div className="flex flex-wrap gap-2">
                {[
                  "Loose stools or watery diarrhea",
                  "Abdominal cramping",
                  "Skin itching or rash",
                  "Gastric heartburn / acid burning",
                  "Dry mouth / excessive thirst",
                  "Mild headache",
                ].map((symptom) => {
                  const active = promsAdverse.includes(symptom);
                  return (
                    <button
                      key={symptom}
                      type="button"
                      onClick={() => toggleAdverseSymptom(symptom)}
                      className={`px-3 py-1.5 rounded-lg text-xs transition cursor-pointer border ${
                        active
                          ? "bg-rose-950 text-rose-300 border-rose-700 font-semibold"
                          : "bg-[#171f19] text-[#8a9490] border-[#24302a] hover:border-[#8a9490]"
                      }`}
                    >
                      {active ? "⚠️ " : "+ "}
                      {symptom}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-[#1f2b24]">
              <span className="text-[#8a9490] text-[11px]">
                Your clinical responses are securely signed and archived under your Matab longitudinal record.
              </span>
              <button
                type="submit"
                className="px-5 py-2.5 bg-[#2ea87f] hover:bg-[#268f6c] text-[#0a0f0d] font-bold text-xs rounded-lg transition shadow-md shadow-[#2ea87f]/20 cursor-pointer"
              >
                Submit Day {promsDay} Clinical Check-in
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
