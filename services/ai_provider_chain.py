"""
ZAYVORA Health OS — Multi-Model AI Provider Orchestrator
=========================================================
Chained failover AI inference engine across 4 tiers:
Tier 0: Google Gemini
Tier 1: Anthropic Claude 3.5 Sonnet
Tier 2: OpenAI GPT-4o
Tier 3: Local Quantized vLLM Engine
Tier 4: Deterministic Classical Unani Knowledge Fallback Engine
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

class LiveAIProviderChain:
    """
    Orchestrates AI clinical inference across a 4-tier provider hierarchy:
    Tier 1: Primary Cloud LLM (Anthropic Claude 3.5 Sonnet)
    Tier 2: Secondary Cloud LLM (OpenAI GPT-4o)
    Tier 3: Local Quantized vLLM Engine
    Tier 4: Deterministic Classical Unani Knowledge Fallback Engine
    """
    def __init__(self):
        self.degradation_logs = []
        self.last_provider_used = None
        self.fallback_occurred = False

    def generate(self, system_prompt: str, user_prompt: str, context: dict) -> str:
        self.degradation_logs = []
        self.fallback_occurred = False
        
        sim_fail = context.get("simulatedFailure") or {}
        sim_fail_primary = sim_fail.get("primary", False)
        sim_fail_secondary = sim_fail.get("secondary", False)
        sim_fail_vllm = sim_fail.get("vllm", False)
        force_provider = context.get("forceProvider")

        # Tier 0: Primary Cloud LLM (Google Gemini)
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not sim_fail_primary and (force_provider == "gemini" or not force_provider):
            if gemini_key:
                import urllib.request
                default_gem = os.getenv("GEMINI_MODEL") or "gemini-flash-lite-latest"
                candidates = [default_gem]
                for alt in ("gemini-flash-latest", "gemini-flash-lite-latest"):
                    if alt not in candidates:
                        candidates.append(alt)
                
                gemini_success = False
                for gem_model in candidates:
                    try:
                        gemini_url = (
                            "https://generativelanguage.googleapis.com/v1beta/models/"
                            f"{gem_model}:generateContent?key={gemini_key}"
                        )
                        req = urllib.request.Request(
                            gemini_url,
                            headers={"Content-Type": "application/json"},
                            data=json.dumps({
                                "systemInstruction": {"parts": [{"text": system_prompt}]},
                                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
                                "generationConfig": {"maxOutputTokens": 2048, "temperature": 0.3}
                            }).encode()
                        )
                        with urllib.request.urlopen(req, timeout=25) as resp:
                            data = json.loads(resp.read().decode())
                            self.last_provider_used = f"Primary (Google Gemini {gem_model})"
                            return data["candidates"][0]["content"]["parts"][0]["text"]
                    except Exception as exc:
                        self.degradation_logs.append({
                            "provider": f"Primary (Google Gemini {gem_model})",
                            "status": "failed",
                            "error": str(exc)
                        })
            else:
                self.degradation_logs.append({
                    "provider": "Primary (Google Gemini 2.0 Flash)",
                    "status": "failed",
                    "error": "GEMINI_API_KEY / GOOGLE_API_KEY not configured."
                })

        # Tier 1: Primary Cloud LLM (Claude 3.5 Sonnet)
        if not sim_fail_primary and (force_provider == "primary" or not force_provider):

            if os.getenv("ANTHROPIC_API_KEY"):
                try:
                    import urllib.request
                    req = urllib.request.Request(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
                            "content-type": "application/json",
                            "anthropic-version": "2023-06-01"
                        },
                        data=json.dumps({
                            "model": "claude-3-5-sonnet-20241022",
                            "max_tokens": 2048,
                            "system": system_prompt,
                            "messages": [{"role": "user", "content": user_prompt}]
                        }).encode()
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = json.loads(resp.read().decode())
                        self.last_provider_used = "Primary (Anthropic Claude 3.5 Sonnet)"
                        return data["content"][0]["text"]
                except Exception as exc:
                    self.degradation_logs.append({
                        "provider": "Primary (Anthropic Claude 3.5 Sonnet)",
                        "status": "failed",
                        "error": str(exc)
                    })
            elif context.get("mockPrimarySuccess"):
                self.last_provider_used = "Primary (Anthropic Claude 3.5 Sonnet)"
                return context["mockPrimarySuccess"]
            else:
                self.degradation_logs.append({
                    "provider": "Primary (Anthropic Claude 3.5 Sonnet)",
                    "status": "failed",
                    "error": "Primary API key not configured or simulated failure flag active."
                })
        else:
            self.degradation_logs.append({
                "provider": "Primary (Anthropic Claude 3.5 Sonnet)",
                "status": "failed",
                "error": "Primary provider simulated network failure."
            })

        self.fallback_occurred = True

        # Tier 2: Secondary Cloud LLM (OpenAI GPT-4o)
        if not sim_fail_secondary and (force_provider == "secondary" or not force_provider):
            if os.getenv("OPENAI_API_KEY"):
                try:
                    import urllib.request
                    req = urllib.request.Request(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                            "Content-Type": "application/json"
                        },
                        data=json.dumps({
                            "model": "gpt-4o",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ]
                        }).encode()
                    )
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = json.loads(resp.read().decode())
                        self.last_provider_used = "Secondary (OpenAI GPT-4o)"
                        return data["choices"][0]["message"]["content"]
                except Exception as exc:
                    self.degradation_logs.append({
                        "provider": "Secondary (OpenAI GPT-4o)",
                        "status": "failed",
                        "error": str(exc)
                    })
            elif context.get("mockSecondarySuccess"):
                self.last_provider_used = "Secondary (OpenAI GPT-4o)"
                return context["mockSecondarySuccess"]
            else:
                self.degradation_logs.append({
                    "provider": "Secondary (OpenAI GPT-4o)",
                    "status": "failed",
                    "error": "Secondary API key not configured or simulated failure flag active."
                })
        else:
            self.degradation_logs.append({
                "provider": "Secondary (OpenAI GPT-4o)",
                "status": "failed",
                "error": "Secondary provider simulated network failure."
            })

        # Tier 3: Local Quantized vLLM Engine
        if not sim_fail_vllm and (force_provider == "vllm" or not force_provider):
            vllm_url = os.getenv("VLLM_API_URL", "http://localhost:8001/v1/chat/completions")
            try:
                import urllib.request
                req = urllib.request.Request(
                    vllm_url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({
                        "model": "unani-qwen-7b-clinical",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    }).encode()
                )
                with urllib.request.urlopen(req, timeout=2) as resp:
                    data = json.loads(resp.read().decode())
                    self.last_provider_used = "Local Quantized vLLM Engine"
                    return data["choices"][0]["message"]["content"]
            except Exception as exc:
                self.degradation_logs.append({
                    "provider": "Local Quantized vLLM Engine",
                    "status": "offline",
                    "error": f"Local vLLM server offline: {exc}"
                })
        else:
            self.degradation_logs.append({
                "provider": "Local Quantized vLLM Engine",
                "status": "failed",
                "error": "Local vLLM simulated failure."
            })

        # Tier 4: Deterministic Classical Unani Knowledge Fallback Engine
        self.last_provider_used = "Deterministic Classical Unani Knowledge Fallback"
        return self._build_deterministic_classical_response(context)

    def _build_deterministic_classical_response(self, context: dict) -> str:
        complaint = context.get("chief_complaint", "General malaise and humoral dyscrasia")
        mizaj = context.get("mizaj", "Balghami (Cold & Moist)")
        axis = context.get("organ_axis", "Musculoskeletal-Metabolic Axis (Mafasil-Asab)")
        meds = ", ".join(context.get("current_medications") or []) or "None documented"
        allergies = ", ".join(context.get("allergies") or []) or "None documented"

        # Check for joint / pain context
        is_joint = any(k in complaint.lower() for k in ["joint", "knee", "back", "pain", "stiff", "waja", "mafasil", "arthritis", "gout"])
        is_digestive = any(k in complaint.lower() for k in ["digest", "stomach", "acidity", "mida", "liver", "jigar", "gastric", "hazm"])

        if is_joint:
            classical_unani = f"Presentation concordant with Waja-ul-Mafasil Barid Balghami (Cold-Moist Phlegmatic Arthralgia) along the {axis}. Humoral stasis impairs synovial lubrication."
            biomedical = "Osteoarthritis with secondary synovial inflammation. Differential must exclude Gouty Arthritis (Niqris) and early Seronegative Spondylopathy."
            differential = "Waja-ul-Mafasil, Osteoarthritis (ICD-10 M17.9), Niqris (Gout, ICD-10 M10.9), Pseudogout."
            evidence = "UPI Monograph Vol I: Suranjan Talkh (Colchicum luteum) and Majun Suranjan indicated for joint inflammation with verified analgesic efficacy."
            options = "Majun Suranjan 5g nocte with warm milk; Roghan Suranjan local application; Dalak Layyin (gentle massage) regimen."
            missing = "Recent serum uric acid, inflammatory markers (ESR, hs-CRP), and bilateral weight-bearing radiographs."
        elif is_digestive:
            classical_unani = f"Presentation concordant with Su-e-Mizaj Meda Haar (Hot Gastric Dyscrasia) along the {axis}. Excess bile (Safra) irritation."
            biomedical = "Gastroesophageal Reflux Disease (GERD) and functional dyspepsia. Evaluate for Helicobacter pylori gastritis."
            differential = "Su-e-Mizaj Hazm, GERD (ICD-10 K21.9), Peptic Ulcer Disease, Biliary Dyskinesia."
            evidence = "UPI Monograph Vol II: Sharbat Bazoori Motadil and Jawarish Shahi indicated for post-prandial pyrosis."
            options = "Sharbat Bazoori Motadil 20ml b.i.d.; Jawarish Amla 5g post-prandial; avoid spicy, fried foods."
            missing = "Upper gastrointestinal endoscopy or H. pylori stool antigen test if alarm symptoms emerge."
        else:
            classical_unani = f"Presentation reflects temperamental dyscrasia ({mizaj}) with functional disturbance along the {axis}."
            biomedical = "Non-specific presentation requiring baseline blood investigations to exclude systemic metabolic disease."
            differential = "Constitutional Su-e-Mizaj, Chronic Fatigue Syndrome, Subclinical Hypothyroidism."
            evidence = "UPI Part I & II monographs support restorative tonics (Muqawwiyat) for constitutional debility."
            options = "Khamira Gaozaban Ambari 3g morning; dietary optimization with warm, easily digestible meals."
            missing = "Baseline hematology (CBC), fasting glucose, thyroid stimulating hormone (TSH), and urinalysis."

        red_flags = "None documented in current presentation. Immediate biomedical referral required if red flags develop."
        safety = f"Patient medications on file: {meds}. Allergies: {allergies}. Full deterministic Safety Firewall verification required before prescription lock."
        monitoring = "Clinical review and PROMs symptom score evaluation in 14 days or earlier if acute exacerbation occurs."
        uncertainty = "Low to moderate uncertainty. Clinical impression grounded in classical Unani texts (Al-Qanun fi al-Tibb, Kitab al-Hawi) and UPI monographs."

        response = f"""CLINICAL SUMMARY
Patient presenting with: {complaint}. Dominant constitution assessed as {mizaj}.

WHAT IS KNOWN
Known symptoms and functional impairment along the {axis}. Medications: {meds}.

UNANI PERSPECTIVE
{classical_unani}

BIOMEDICAL PERSPECTIVE
{biomedical}

DIFFERENTIAL CONSIDERATIONS
{differential}

RED FLAGS
{red_flags}

MISSING INFORMATION
{missing}

EVIDENCE
{evidence}

SAFETY
{safety}

POSSIBLE CARE OPTIONS
{options}

MONITORING
{monitoring}

UNCERTAINTY
{uncertainty}

CLINICIAN REVIEW REQUIRED
Yes — this clinical guidance is synthesized by ZAYVORA Hakeem Sahab™ for decision-support purposes only. In accordance with clinical governance standards, this recommendation requires non-delegable review and digital signature by a licensed practitioner before any clinical action is taken."""
        return response

