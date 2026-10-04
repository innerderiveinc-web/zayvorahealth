#!/usr/bin/env python3
"""
ZAYVORA Health OS — Proprietary Clinical Branding Re-Alignment
Replaces all external clinical references (Mayo Clinic, Cleveland Clinic, ZOE, Thorne, IFM)
with ZAYVORA's own proprietary clinical trademark nomenclature across index.html and js/zayvora-core.js.
"""

import sys
import re

def rebrand_content(content):
    # Replacements map
    replacements = [
        # Headers & Badges in Modals
        ("Mayo Clinic Benchmark", "ZAYVORA Clinical Triage"),
        ("Cleveland Clinic Benchmark", "ZAYVORA Integrative Lab Desk"),
        ("ZOE / Thorne Benchmark", "ZAYVORA Precision Nutrition"),
        ("Mayo Outcomes Benchmark", "ZAYVORA Clinical Outcomes Standard"),
        ("IFM Matrix Benchmark", "ZAYVORA Metabolic Matrix Standard"),
        ("Mayo Clinic &amp; Cleveland Clinic Benchmark", "ZAYVORA Integrative Clinical Architecture"),
        ("MAYO CLINIC & CLEVELAND CLINIC BENCHMARK", "ZAYVORA INTEGRATIVE CLINICAL BENCHMARK"),
        ("Mayo Clinic • Cleveland Clinic • IFM Functional Medicine Benchmarks", "ZAYVORA Proprietary Clinical & Functional Medical Architecture"),
        ("Mayo Clinic • Cleveland Clinic • IFM Benchmarks", "ZAYVORA Integrative Clinical Intelligence"),
        ("Functional &amp; Mayo Engines", "ZAYVORA Diagnostic &amp; Clinical Engines"),
        ("Functional & Mayo Engines", "ZAYVORA Diagnostic & Clinical Engines"),
        ("Mayo / Cleveland Benchmark", "ZAYVORA Global Multi-Currency Standard"),
        
        # Tags inside Global Tools Modal
        (">MAYO CLINIC<", ">ZAYVORA TRIAGE<"),
        (">CLEVELAND CLINIC<", ">INTEGRATIVE 2ND OPINION<"),
        (">ZOE / THORNE<", ">PRECISION FOOD<"),
        (">IFM MATRIX<", ">METABOLIC MATRIX<"),
        
        # Tool card subtitles
        ("Mayo-Style Triage", "Neuro-Somatic Triage"),
        ("Cleveland 2nd Opinion", "Integrative 2nd Opinion"),
        ("ZOE Precision Food", "Constitutional Nutrition"),
        ("ZOE Precision nutrition", "Constitutional Nutrition"),
        
        # IFM specific terms
        ("IFM Matrix Assimilation &amp; Biotransformation Engine", "ZAYVORA Metabolic Assimilation &amp; Biotransformation Engine"),
        ("IFM Matrix Assimilation & Biotransformation Engine", "ZAYVORA Metabolic Assimilation & Biotransformation Engine"),
        ("The Functional Medicine Chronological Genesis (IFM Timeline Benchmark)", "ZAYVORA Chronological Genesis Timeline (Saniha-e-Maraz Standard)"),
        ("IFM Timeline Benchmark", "ZAYVORA Chronological Genesis Standard"),
        
        # Dossier & Comments
        ("Advanced Integrative Assessment Benchmark (Mayo Clinic / Cleveland Clinic Standard)", "ZAYVORA Advanced Integrative Assessment Standard (National & Global Clinical Benchmark)"),
        ("// ── 1. MAYO CLINIC BENCHMARK: INTERACTIVE BODY SYMPTOM NAVIGATOR", "// ── 1. ZAYVORA PROPRIETARY: INTERACTIVE BODY SYMPTOM NAVIGATOR"),
        ("// ── 2. CLEVELAND CLINIC BENCHMARK: LAB REPORT CORRELATOR", "// ── 2. ZAYVORA PROPRIETARY: LAB REPORT CORRELATOR"),
        ("// ── 3. ZOE / THORNE BENCHMARK: MIZAJ FOOD & KITCHEN SCANNER", "// ── 3. ZAYVORA PROPRIETARY: MIZAJ FOOD & KITCHEN SCANNER"),
        ("// ── 5. MAYO CLINICAL OUTCOMES BENCHMARK: PROMS REGISTRY DASHBOARD", "// ── 5. ZAYVORA PROPRIETARY: PROMS REGISTRY DASHBOARD"),
        ("<!-- 1. MAYO CLINIC BENCHMARK: INTERACTIVE BODY SYMPTOM NAVIGATOR MODAL", "<!-- 1. ZAYVORA PROPRIETARY: INTERACTIVE BODY SYMPTOM NAVIGATOR MODAL"),
        ("<!-- 2. CLEVELAND CLINIC BENCHMARK: LAB REPORT CORRELATOR & SECOND OPINION", "<!-- 2. ZAYVORA PROPRIETARY: LAB REPORT CORRELATOR & SECOND OPINION"),
        ("<!-- 3. ZOE / THORNE BENCHMARK: MIZAJ FOOD & KITCHEN COMPATIBILITY MATRIX", "<!-- 3. ZAYVORA PROPRIETARY: MIZAJ FOOD & KITCHEN COMPATIBILITY MATRIX"),
        ("<!-- 5. MAYO CLINICAL OUTCOMES BENCHMARK: PROMS REGISTRY DASHBOARD", "<!-- 5. ZAYVORA PROPRIETARY: PROMS REGISTRY DASHBOARD"),
        ("<!-- 6. IFM BENCHMARK: HAZM-E-ARBA'A 4-STAGE DIGESTION & DETOX ANALYZER", "<!-- 6. ZAYVORA PROPRIETARY: HAZM-E-ARBA'A 4-STAGE DIGESTION & DETOX ANALYZER"),
        ("<!-- 7. IFM BENCHMARK: FUNCTIONAL ATM ROOT-CAUSE TIMELINE BUILDER", "<!-- 7. ZAYVORA PROPRIETARY: FUNCTIONAL ATM ROOT-CAUSE TIMELINE BUILDER"),
        ("GLOBAL CLINICAL BENCHMARKS & FUNCTIONAL MEDICINE SUITE (IFM / MAYO)", "ZAYVORA GLOBAL CLINICAL & FUNCTIONAL MEDICINE SUITE")
    ]

    count = 0
    for old_str, new_str in replacements:
        if old_str in content:
            content = content.replace(old_str, new_str)
            count += 1
            print(f"  Replaced: '{old_str}' -> '{new_str}'")

    return content, count

def main():
    print("Rebranding all external clinic references to ZAYVORA proprietary nomenclature...")

    # 1. Update index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    html_updated, h_count = rebrand_content(html)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_updated)
    print(f"✓ Updated index.html ({h_count} replacements applied)")

    # 2. Update js/zayvora-core.js
    with open("js/zayvora-core.js", "r", encoding="utf-8") as f:
        js = f.read()
    js_updated, j_count = rebrand_content(js)
    with open("js/zayvora-core.js", "w", encoding="utf-8") as f:
        f.write(js_updated)
    print(f"✓ Updated js/zayvora-core.js ({j_count} replacements applied)")

if __name__ == '__main__':
    main()
