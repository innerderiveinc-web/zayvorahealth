"""
Baseline permission catalogue. This is intentionally small for Phase 0 —
only what the Clinical Core (Phase 1) will need. Each later phase should
add its own permission codes here rather than inventing ad-hoc ones in
route handlers, so the full permission surface stays in one place and
`role.manage` holders can always see the complete list.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity import Permission, Role

BASELINE_PERMISSIONS: dict[str, str] = {
    "role.manage": "Create and modify roles and their permissions",
    "user.invite": "Invite new users into the organization",
    "patient.create": "Register a new patient",
    "patient.read": "View patient records",
    "patient.update": "Edit patient records",
    "encounter.create": "Create a clinical encounter/consultation",
    "encounter.read": "View clinical encounters",
    "encounter.close": "Close/finalize a clinical encounter",
    "clinical_note.create": "Author a clinical note (SOAP or free-text)",
    "clinical_note.read": "View clinical notes",
    "clinical_note.amend": "Amend a clinical note (creates a new version; originals are never overwritten)",
    "prescription.create": "Issue a prescription",
    "prescription.read": "View prescriptions",
    "prescription.discontinue": "Discontinue an active prescription",
    "appointment.create": "Schedule an appointment",
    "appointment.read": "View appointments",
    "appointment.update": "Reschedule, complete, or cancel an appointment",
    "pharmacopoeia.read": "View Mufradat (Pharmacopoeia) monographs and their Mizaj/Organ-Axis links",
    "pharmacopoeia.write": "Create or edit Mufradat monographs, assign Mizaj, link Organ-Axis",
    "evidence.read": "View evidence records attached to Mufradat",
    "evidence.write": "Attach evidence records to Mufradat (does not auto-approve — review_status stays 'pending' until reviewed)",
    "nuskha.create": "Draft a Nuskha (runs the Safety Firewall automatically; never creates a pre-approved prescription)",
    "nuskha.read": "View Nuskha drafts",
    "nuskha.approve": "Approve or reject a Nuskha draft (blocked by a DO_NOT_RECOMMEND/REFER Safety Firewall verdict unless the approver also holds safety_firewall.override)",
    "tadbeer.create": "Create an Ilaj bil-Tadbeer plan",
    "tadbeer.read": "View Ilaj bil-Tadbeer plans",
    "ghiza.create": "Create an Ilaj bil-Ghiza dietary plan",
    "ghiza.read": "View Ilaj bil-Ghiza dietary plans",
    "care_plan.create": "Create a unified multi-horizon care plan (Dawa + Tadbeer + Ghiza + Asbab Sittah)",
    "care_plan.read": "View unified care plans",
    "care_plan.sign": "Statutory clinician signing and locking of unified care plans",
    "pharmacovigilance.report": "Submit and evaluate adverse drug reaction / botanical safety reports",
    "hakeem.consult": "Request a Hakeem Sahab AI consultation (advisory only — never auto-prescribes; every response requires clinician review)",
    "safety_firewall.override": "Override a Safety Firewall hold (logged, requires clinical justification)",
    "audit_log.read": "View the organization's audit log",
    "dispensary.manage": "Manage pharmaceutical inventory, FEFO batch allocation, and dispense medications",
    "logistics.manage": "Manage purchasing, suppliers, cold-chain tracking, and courier shipments",
    "research.manage": "Manage clinical research studies, trial cohorts, and RWE data extraction",
    "manufacturing.manage": "Manage electronic batch manufacturing records (eBMR) and QA/QC release",
    "governance.vote": "Participate in 3/3 Clinical Governance Board quorum reviews and CCO approval",
    "patient_portal.access": "Access patient personal health records, care plans, and consent management",
    "billing.manage": "Manage invoices, payments, fee schedules, subscriptions, and refunds",
}

# The role automatically granted to whoever creates a new organization.
# Broad by design (it is the tenant's first admin) — subsequent roles
# should be scoped more narrowly via POST /api/v1/roles.
OWNER_ROLE_NAME = "Owner"


def ensure_baseline_permissions(db: Session) -> dict[str, Permission]:
    existing = {p.code: p for p in db.execute(select(Permission)).scalars().all()}
    created = False
    for code, description in BASELINE_PERMISSIONS.items():
        if code not in existing:
            perm = Permission(code=code, description=description)
            db.add(perm)
            existing[code] = perm
            created = True
    if created:
        db.flush()
    return existing


def provision_owner_role(db: Session, organization_id) -> Role:
    permissions = ensure_baseline_permissions(db)
    role = Role(
        organization_id=organization_id,
        name=OWNER_ROLE_NAME,
        description="Full administrative access for this organization (auto-provisioned at signup).",
        permissions=list(permissions.values()),
    )
    db.add(role)
    db.flush()
    return role
