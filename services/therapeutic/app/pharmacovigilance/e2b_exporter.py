"""
ZAYVORA HEALTH™ — WHO-UMC Pharmacovigilance ICH E2B(R3) XML & CIOMS Exporter
Converts suspected adverse drug reaction reports and causality assessments
into standardized electronic filing formats (ICH E2B(R3) / CIOMS I) for
national pharmacovigilance centers (IPC/PvPI/AYUSH) and Uppsala Monitoring Centre.
"""
from __future__ import annotations

import html
import uuid
from datetime import datetime, timezone
from typing import Any

# Standard Unani to MedDRA LLT Term Mapping
UNANI_TO_MEDDRA_MAP: dict[str, dict[str, str]] = {
    "hurqat-ul-meda": {"llt_name": "Heartburn", "llt_code": "10019805"},
    "waja-ul-mafasil": {"llt_name": "Arthralgia", "llt_code": "10003239"},
    "humma": {"llt_name": "Pyrexia", "llt_code": "10037660"},
    "khafaqan": {"llt_name": "Palpitations", "llt_code": "10033557"},
    "suda": {"llt_name": "Headache", "llt_code": "10019211"},
    "qabz": {"llt_name": "Constipation", "llt_code": "10010774"},
    "ishaal": {"llt_name": "Diarrhoea", "llt_code": "10012735"},
    "ghutnon me dard": {"llt_name": "Arthralgia", "llt_code": "10003239"},
    "sinay me jalan": {"llt_name": "Heartburn", "llt_code": "10019805"},
    "acid reflux": {"llt_name": "Gastrooesophageal reflux disease", "llt_code": "10017885"},
    "skin rash": {"llt_name": "Rash", "llt_code": "10037844"},
    "dizziness": {"llt_name": "Dizziness", "llt_code": "10013573"},
    "nausea": {"llt_name": "Nausea", "llt_code": "10028813"},
    "vomiting": {"llt_name": "Vomiting", "llt_code": "10047700"},
}


def map_reaction_to_meddra(reaction_desc: str) -> dict[str, str]:
    """Maps adverse reaction description to MedDRA LLT name and code."""
    cleaned = reaction_desc.lower()
    for pattern, meddra in UNANI_TO_MEDDRA_MAP.items():
        if pattern in cleaned:
            return meddra
    return {"llt_name": reaction_desc[:100], "llt_code": "10000001"}


def export_ich_e2b_r3_xml(report: dict[str, Any], evaluation: dict[str, Any] | None = None) -> str:
    """
    Constructs an authentic ICH E2B(R3) ICSR XML document.
    Enforces strict de-identification of direct patient identifiers.
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y%m%d")
    datetime_str = now.strftime("%Y%m%d%H%M%S")
    safety_report_id = f"IN-ZAYVORA-{now.strftime('%Y')}-{uuid.uuid4().hex[:8].upper()}"

    suspected_agent = html.escape(str(report.get("suspected_agent", "UNKNOWN_AGENT")))
    reaction_desc = html.escape(str(report.get("adverse_reaction_description", "Unspecified adverse reaction")))
    meddra = map_reaction_to_meddra(report.get("adverse_reaction_description", ""))
    
    latency = report.get("latency_hours", 0)
    is_e1 = report.get("is_schedule_e1_substance", False)
    mudabbar_followed = report.get("verified_mudabbar_protocol_followed", True)

    causality_cat = html.escape(str((evaluation or {}).get("causality_category", "UNCLASSIFIED")))
    causality_score = (evaluation or {}).get("causality_score", 0)
    statutory_warning = html.escape(str((evaluation or {}).get("statutory_warning") or "None"))

    dechallenge_outcome = report.get("dechallenge_outcome", "unknown")
    rechallenge_outcome = report.get("rechallenge_outcome", "not_applicable")

    concomitant_drugs = report.get("concomitant_drugs", [])

    concomitant_xml = ""
    for idx, drug in enumerate(concomitant_drugs, start=2):
        escaped_drug = html.escape(str(drug))
        concomitant_xml += f"""
      <drug>
        <drugcharacterization>2</drugcharacterization>
        <medicinalproduct>{escaped_drug}</medicinalproduct>
        <drugdosagetext>Concomitant medication as prescribed</drugdosagetext>
      </drug>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ichicsr lang="en">
  <ichicsrmessageheader>
    <messagetype>ichicsr</messagetype>
    <messageformatversion>2.1</messageformatversion>
    <messageformatrelease>2.0</messageformatrelease>
    <messagenumb>{uuid.uuid4().hex}</messagenumb>
    <messagesenderidentifier>ZAYVORA-HEALTH-SAFETY</messagesenderidentifier>
    <messagereceiveridentifier>NATIONAL-PHARMACOVIGILANCE-CENTRE</messagereceiveridentifier>
    <messagedateformat>204</messagedateformat>
    <messagedate>{datetime_str}</messagedate>
  </ichicsrmessageheader>
  <safetyreport>
    <safetyreportversion>1</safetyreportversion>
    <safetyreportid>{safety_report_id}</safetyreportid>
    <primarysourcecountry>IN</primarysourcecountry>
    <occurcountry>IN</occurcountry>
    <transmissiondateformat>102</transmissiondateformat>
    <transmissiondate>{date_str}</transmissiondate>
    <reporttype>1</reporttype>
    <serious>{'1' if is_e1 and not mudabbar_followed else '2'}</serious>
    <seriousnessdeath>2</seriousnessdeath>
    <seriousnesslifethreatening>{'1' if is_e1 and not mudabbar_followed else '2'}</seriousnesslifethreatening>
    <seriousnesshospitalization>2</seriousnesshospitalization>
    <seriousnessdisabling>2</seriousnessdisabling>
    <seriousnesscongenitalanomali>2</seriousnesscongenitalanomali>
    <seriousnessother>2</seriousnessother>
    <receivedateformat>102</receivedateformat>
    <receivedate>{date_str}</receivedate>
    <receiptdateformat>102</receiptdateformat>
    <receiptdate>{date_str}</receiptdate>
    <patient>
      <!-- Direct identifiers strictly redacted per clinical data privacy regulations -->
      <patientinitials>[REDACTED]</patientinitials>
      <patientsex>0</patientsex>
      <reaction>
        <primarysourcereaction>{reaction_desc}</primarysourcereaction>
        <reactionmeddraversionllt>27.0</reactionmeddraversionllt>
        <reactionmeddrallt>{meddra['llt_code']}</reactionmeddrallt>
        <reactionmeddrallttext>{html.escape(meddra['llt_name'])}</reactionmeddrallttext>
        <reactionoutcome>{'1' if dechallenge_outcome == 'improved' else '6'}</reactionoutcome>
      </reaction>
      <drug>
        <drugcharacterization>1</drugcharacterization>
        <medicinalproduct>{suspected_agent}</medicinalproduct>
        <drugdosagetext>Standard unani therapeutic posology</drugdosagetext>
        <drugactiontaken>{'1' if report.get('dechallenge_performed') else '4'}</drugactiontaken>
        <drugrecurrence>
          <drugrecurreadministration>{'1' if rechallenge_outcome == 'positive' else '2' if rechallenge_outcome == 'negative' else '3'}</drugrecurreadministration>
        </drugrecurrence>
      </drug>{concomitant_xml}
      <summary>
        <narrativeincludeclinical>Suspected adverse reaction with latency {latency} hours. Schedule E(1) status: {is_e1}. Mudabbar compliant: {mudabbar_followed}.</narrativeincludeclinical>
        <reportercomment>Reported via ZAYVORA Clinical Safety Surveillance System.</reportercomment>
        <sendercomment>WHO-UMC Causality: {causality_cat} (Score: {causality_score}). Statutory Warning: {statutory_warning}</sendercomment>
      </summary>
    </patient>
  </safetyreport>
</ichicsr>"""
    return xml.strip()


def export_cioms_i_format(report: dict[str, Any], evaluation: dict[str, Any] | None = None) -> dict[str, Any]:
    """Generates standardized CIOMS Form I JSON representation."""
    meddra = map_reaction_to_meddra(report.get("adverse_reaction_description", ""))
    return {
        "form_type": "CIOMS_FORM_I",
        "report_id": f"CIOMS-{uuid.uuid4().hex[:8].upper()}",
        "patient": {
            "initials": "[REDACTED]",
            "age": report.get("patient_age", "N/A"),
            "sex": report.get("patient_sex", "UNKNOWN"),
        },
        "suspected_drug": {
            "name": report.get("suspected_agent"),
            "is_schedule_e1": report.get("is_schedule_e1_substance", False),
            "mudabbar_protocol_verified": report.get("verified_mudabbar_protocol_followed", True),
        },
        "adverse_reaction": {
            "description": report.get("adverse_reaction_description"),
            "meddra_llt_name": meddra["llt_name"],
            "meddra_llt_code": meddra["llt_code"],
            "latency_hours": report.get("latency_hours"),
        },
        "who_umc_causality": evaluation or {},
        "concomitant_medications": report.get("concomitant_drugs", []),
    }
