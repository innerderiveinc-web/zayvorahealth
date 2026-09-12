"use client";

import React, { useState, useEffect } from "react";
import { taskApi, type TaskRecord, type TaskListResponse } from "@/lib/taskApi";

interface TaskPipelineCockpitProps {
  token: string;
}

export function TaskPipelineCockpit({ token }: TaskPipelineCockpitProps) {
  const [tasksData, setTasksData] = useState<TaskListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeSubTab, setActiveSubTab] = useState<"queue" | "abdm_m3" | "fhir_batch">("queue");
  const [draining, setDraining] = useState(false);

  // ABDM M3 Form
  const [patientAbha, setPatientAbha] = useState("91-1234-5678-9012");
  const [consentId, setConsentId] = useState("CA-7788-ABDM-2035");
  const [m3Result, setM3Result] = useState<any | null>(null);

  // Batch FHIR Form
  const [rawFhirJson, setRawFhirJson] = useState(`{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Condition",
        "code": { "text": "Essential (primary) hypertension", "coding": [{ "code": "I10" }] }
      }
    },
    {
      "resource": {
        "resourceType": "MedicationRequest",
        "medicationCodeableConcept": { "text": "Hab-e-Suranjan Talkh (Schedule E1 Poison)" }
      }
    }
  ]
}`);
  const [batchResult, setBatchResult] = useState<any | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await taskApi.listTasks(token);
      setTasksData(data);
    } catch {
      // Handled by api fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [token]);

  const handleDrainQueue = async () => {
    setDraining(true);
    try {
      await taskApi.drainWorker(token, 10);
      await fetchTasks();
    } finally {
      setDraining(false);
    }
  };

  const handleTriggerABDMFlow = async () => {
    setLoading(true);
    try {
      // 1. Request Data Flow
      const reqRes = await taskApi.requestABDMDataFlow(token, consentId, patientAbha);
      // 2. Transfer Encrypted Packets
      const transferRes = await taskApi.transferABDMDataPacket(token, reqRes.transaction_id, patientAbha, [
        {
          conditions: [
            { code: "E11.9", display: "Type 2 Diabetes Mellitus" },
            { code: "M10.0", display: "Idiopathic Gout" },
          ],
          observations: [{ code: "LOINC-1558-6", display: "Fasting Blood Glucose", value: 138, unit: "mg/dL" }],
          medications: [{ name: "Hab-e-Suranjan Talkh", dosage: "1 pill post evening meal" }],
        },
      ]);
      setM3Result({ req: reqRes, transfer: transferRes });
      await fetchTasks();
    } finally {
      setLoading(false);
    }
  };

  const handleBatchImport = async () => {
    setLoading(true);
    try {
      const parsed = JSON.parse(rawFhirJson);
      const enq = await taskApi.enqueueTask(token, "fhir_batch_import", { fhir_bundle: parsed });
      setBatchResult(enq);
      await fetchTasks();
    } catch (e: any) {
      alert("Invalid JSON: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Metrics */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-2xl">⚡</span>
              <h2 className="text-xl font-bold text-white tracking-tight">
                Asynchronous Task Queue & Streaming Workers
              </h2>
              <span className="px-2 py-0.5 text-xs font-semibold rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Redis-backed background processing pipeline for ABDM Milestone 3 health packet reconciliation, bulk FHIR ingestion, and wearable streams.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleDrainQueue}
              disabled={draining}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white text-xs font-semibold rounded-lg transition-colors shadow-sm flex items-center space-x-2"
            >
              <span>{draining ? "Draining..." : "Drain Worker Queue"}</span>
            </button>
            <button
              onClick={fetchTasks}
              disabled={loading}
              className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg transition-colors border border-slate-700"
            >
              Refresh
            </button>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 uppercase tracking-wider font-medium">Queue Depth</div>
            <div className="text-2xl font-bold text-white mt-1">
              {tasksData?.queue_depth ?? 0} <span className="text-xs text-slate-400 font-normal">pending</span>
            </div>
          </div>
          <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 uppercase tracking-wider font-medium">Total Registered Tasks</div>
            <div className="text-2xl font-bold text-indigo-400 mt-1">{tasksData?.total ?? 0}</div>
          </div>
          <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 uppercase tracking-wider font-medium">Dual-Coding Invariant</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Active</div>
          </div>
          <div className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/50">
            <div className="text-xs text-slate-400 uppercase tracking-wider font-medium">Safe-To-Lock Firewall</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">
              Enforced <span className="text-xs text-slate-400 font-normal">(safe_to_lock = False)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex border-b border-slate-800 space-x-4">
        <button
          onClick={() => setActiveSubTab("queue")}
          className={`pb-3 px-1 text-sm font-medium transition-colors border-b-2 ${
            activeSubTab === "queue"
              ? "border-emerald-500 text-emerald-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Task Queue Ledger ({tasksData?.tasks?.length || 0})
        </button>
        <button
          onClick={() => setActiveSubTab("abdm_m3")}
          className={`pb-3 px-1 text-sm font-medium transition-colors border-b-2 ${
            activeSubTab === "abdm_m3"
              ? "border-emerald-500 text-emerald-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          ABDM Milestone 3 Health Data Flow
        </button>
        <button
          onClick={() => setActiveSubTab("fhir_batch")}
          className={`pb-3 px-1 text-sm font-medium transition-colors border-b-2 ${
            activeSubTab === "fhir_batch"
              ? "border-emerald-500 text-emerald-400"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          FHIR R4 Batch Ingestion & Poison Check
        </button>
      </div>

      {/* SUB-TAB 1: Task Queue Ledger */}
      {activeSubTab === "queue" && (
        <div className="space-y-4">
          {tasksData?.tasks?.map((t) => (
            <div
              key={t.task_id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center space-x-3">
                    <span className="font-mono text-xs text-indigo-400 bg-indigo-950/40 border border-indigo-800/40 px-2 py-0.5 rounded">
                      {t.task_id}
                    </span>
                    <span className="font-semibold text-white text-sm">{t.task_type}</span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded font-medium border ${
                        t.status === "COMPLETED"
                          ? "bg-emerald-950/30 text-emerald-400 border-emerald-800/40"
                          : t.status === "PROCESSING"
                          ? "bg-sky-950/30 text-sky-400 border-sky-800/40"
                          : t.status === "FAILED"
                          ? "bg-rose-950/30 text-rose-400 border-rose-800/40"
                          : "bg-amber-950/30 text-amber-400 border-amber-800/40"
                      }`}
                    >
                      {t.status}
                    </span>
                    <span className="text-xs text-slate-500 font-mono">
                      safe_to_lock: {t.safe_to_lock ? "True" : "False"}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-2 flex items-center space-x-4">
                    <span>Created: {new Date(t.created_at).toLocaleTimeString()}</span>
                    {t.completed_at && <span>Completed: {new Date(t.completed_at).toLocaleTimeString()}</span>}
                    <span>Retries: {t.retry_count} / {t.max_retries}</span>
                  </div>
                </div>
              </div>

              {/* Task Result Summary */}
              {t.result && (
                <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs">
                  <div className="text-slate-400 font-medium mb-1">Execution Outcome:</div>
                  <div className="bg-slate-950/70 p-3 rounded border border-slate-800 font-mono text-slate-300 overflow-x-auto">
                    {t.task_type === "abdm_packet_reconciliation" && t.result.reconciled_conditions && (
                      <div className="space-y-2">
                        <div className="text-emerald-400 font-semibold">
                          Reconciled {t.result.reconciled_conditions.length} Conditions with Dual Unani Coding:
                        </div>
                        {t.result.reconciled_conditions.map((c: any, idx: number) => (
                          <div key={idx} className="pl-2 border-l-2 border-slate-700">
                            <span className="text-sky-300 font-bold">{c.biomedical_code} ({c.biomedical_name})</span>
                            <span className="text-slate-400"> ➔ </span>
                            <span className="text-emerald-300 font-bold">{c.unani_amraz?.canonical_name}</span>
                            <div className="text-slate-500 text-[11px]">{c.unani_amraz?.pathology}</div>
                          </div>
                        ))}
                      </div>
                    )}

                    {t.task_type === "fhir_batch_import" && (
                      <div>
                        <div>Imported {t.result.total_entries} FHIR Resources.</div>
                        {t.result.schedule_e1_alerts?.length > 0 && (
                          <div className="text-rose-400 mt-1 font-bold">
                            ⚠️ {t.result.schedule_e1_alerts.length} Schedule E(1) Statutory Poison(s) Flagged!
                          </div>
                        )}
                      </div>
                    )}

                    {t.task_type === "wearable_stream_sync" && (
                      <div>
                        <div>Biometrics Processed: {t.result.readings_count} telemetry intervals.</div>
                        <div className="text-slate-300 mt-1">
                          Quwwat-e-Hayawaniyyah Autonomic Tone:{" "}
                          <span className="text-emerald-400 font-bold">
                            {t.result.summary_metrics?.quwwat_hayawaniyyah_score}
                          </span>{" "}
                          | Naum-o-Yaqzah Score:{" "}
                          <span className="text-sky-400 font-bold">{t.result.summary_metrics?.naum_yaqzah_score}</span>
                        </div>
                      </div>
                    )}

                    {t.task_type === "qsura_dispatch" && (
                      <div>
                        Dispatched via {t.result.channel} to {t.result.masked_recipient} (Zero-PHI Compliant:{" "}
                        {t.result.zero_phi_compliant ? "YES" : "NO"}).
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* SUB-TAB 2: ABDM Milestone 3 Data Flow Simulator */}
      {activeSubTab === "abdm_m3" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
          <div>
            <h3 className="text-base font-semibold text-white">
              ABDM Milestone 3: Encrypted Health Data Exchange (HIU & HIP)
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Demonstrates asynchronous data flow requests, ECDH curve25519 key exchange, and Unani-biomedical dual-coding reconciliation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Patient ABHA Identifier</label>
              <input
                type="text"
                value={patientAbha}
                onChange={(e) => setPatientAbha(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded px-3 py-2 text-sm text-white font-mono focus:border-indigo-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Approved Consent Artefact ID</label>
              <input
                type="text"
                value={consentId}
                onChange={(e) => setConsentId(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded px-3 py-2 text-sm text-white font-mono focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            onClick={handleTriggerABDMFlow}
            disabled={loading}
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg shadow-sm transition-colors flex items-center space-x-2"
          >
            <span>Initiate ABDM M3 Data Flow Request & Ingest Packets</span>
          </button>

          {m3Result && (
            <div className="mt-4 p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-3">
              <div className="text-emerald-400 font-bold text-sm">
                ✓ ABDM M3 Data Flow Transaction Initialized
              </div>
              <div>Transaction ID: {m3Result.req?.transaction_id}</div>
              <div>Crypto Protocol: {m3Result.req?.key_material?.crypto_algorithm} ({m3Result.req?.key_material?.curve})</div>
              <div>Nonce: {m3Result.req?.key_material?.nonce}</div>
              <div className="p-3 bg-amber-950/20 border border-amber-800/40 rounded text-amber-300">
                🔒 Invariant Guard: safe_to_lock = {m3Result.transfer?.safe_to_lock ? "True" : "False"}. 
                Transferred records are queued for clinical review and require physical physician sign-off before official finalization.
              </div>
            </div>
          )}
        </div>
      )}

      {/* SUB-TAB 3: FHIR R4 Batch Ingestion */}
      {activeSubTab === "fhir_batch" && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
          <div>
            <h3 className="text-base font-semibold text-white">Bulk FHIR R4 Bundle Import & Statutory Poison Check</h3>
            <p className="text-xs text-slate-400 mt-1">
              Parses HL7 FHIR R4 Bundles in the background, validating active prescriptions against the Schedule E(1) Statutory Poison register.
            </p>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">HL7 FHIR R4 Bundle (JSON)</label>
            <textarea
              rows={8}
              value={rawFhirJson}
              onChange={(e) => setRawFhirJson(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded p-3 text-xs text-slate-200 font-mono focus:border-indigo-500 focus:outline-none"
            />
          </div>

          <button
            onClick={handleBatchImport}
            disabled={loading}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg shadow-sm transition-colors"
          >
            Submit FHIR Bundle to Background Queue
          </button>

          {batchResult && (
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-2">
              <div className="text-indigo-400 font-bold">✓ FHIR Bundle Enqueued for Background Processing</div>
              <div>Task ID: {batchResult.task_id}</div>
              <div>Status: {batchResult.status}</div>
              <div>safe_to_lock: {batchResult.safe_to_lock ? "True" : "False"}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
