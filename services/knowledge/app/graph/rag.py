"""
Graph RAG (Retrieval-Augmented Generation) Engine for ZAYVORA HEALTH.
Traverses the knowledge graph to extract deterministic factual triples,
classical formulation rules, and poison safety constraints for LLM clinical grounding.
"""
from __future__ import annotations

from typing import Any


def format_subgraph_as_rag_context(subgraph: dict[str, Any]) -> str:
    """Converts a retrieved graph subgraph into a structured, evidence-grounded
    context string designed for clinical prompt injection."""
    lines = []
    lines.append("=== GROUNDED GRAPH RAG KNOWLEDGE TRIPLETS ===")

    # Target Axes
    axes = subgraph.get("axes", [])
    if axes:
        lines.append("\n[TARGET ORGAN AXES]:")
        for ax in axes:
            lines.append(f"• Axis: {ax.get('name')} ({ax.get('code')}) — Systems: {ax.get('systemsCovered', ax.get('translation', ''))}")

    # Mufradat & Mizaj
    mufradat = subgraph.get("mufradat", [])
    if mufradat:
        lines.append("\n[CANDIDATE SINGLE DRUGS (MUFRADAT) & ROLES]:")
        for m in mufradat:
            mz = m.get("mizaj", {})
            mz_str = f"{mz.get('temperament', 'Unknown')} ({mz.get('quality', '')})" if isinstance(mz, dict) else str(mz)
            e1_warning = " [⚠️ SCHEDULE E(1) POISON - MANDATORY MUDABBAR]" if m.get("isScheduleE1") else ""
            lines.append(f"• {m.get('name')} ({m.get('botanicalName', '')}){e1_warning}:")
            lines.append(f"   - Mizaj: {mz_str}")
            lines.append(f"   - Actions (Af'al): {', '.join(m.get('afal', [])) if isinstance(m.get('afal'), list) else m.get('afal', '')}")
            lines.append(f"   - Standard Dose: {m.get('dose', 'Not specified')}")
            lines.append(f"   - Classical Musleh (Corrective): {m.get('musleh', 'None designated')}")
            lines.append(f"   - Classical Badal (Substitute): {m.get('badal', 'None designated')}")
            if m.get("contraindications"):
                lines.append(f"   - Contraindications: {m.get('contraindications')}")

    # Compound Formulations
    compounds = subgraph.get("compounds", [])
    if compounds:
        lines.append("\n[CLASSICAL COMPOUND FORMULATIONS (MURAKKABAT)]:")
        for c in compounds:
            lines.append(f"• {c.get('name')} ({c.get('category', '')}):")
            lines.append(f"   - Indication: {c.get('classicalIndication', '')}")
            lines.append(f"   - Standard Posology: {c.get('dose', '')}")
            lines.append(f"   - Precautions: {c.get('precautions', '')}")

    # Poison Protocols
    poisons = subgraph.get("poisons", [])
    if poisons:
        lines.append("\n[STATUTORY POISON DETOXIFICATION (MUDABBAR) PROTOCOLS]:")
        for p in poisons:
            lines.append(f"• {p.get('canonical_name', p.get('name'))}:")
            lines.append(f"   - Statutory Warning: {p.get('statutory_warning', '')}")
            lines.append(f"   - Mandatory Protocol: {p.get('mudabbar_protocol', '')}")
            lines.append(f"   - Max Single / Daily Dose: {p.get('max_single_dose_mg', 0)}mg / {p.get('max_daily_dose_mg', 0)}mg")
            lines.append(f"   - Classical Antidote: {p.get('antidote', '')}")

    lines.append("\n=== END GROUNDED GRAPH CONTEXT ===")
    return "\n".join(lines)
