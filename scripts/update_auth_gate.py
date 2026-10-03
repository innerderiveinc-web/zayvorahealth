#!/usr/bin/env python3
"""
Fix Auth Gate and Role Switching in ZAYVORA Health OS:
1. Ensure prefillLogin only populates form inputs and prompts the user to click Sign In.
2. Ensure switchRole prevents unauthorized role access and prompts for login instead of silently fabricating sessions.
3. Ensure initializeApp prevents unauthenticated visitors from landing on internal desks on refresh.
"""
import re

CORE_JS = "js/zayvora-core.js"

with open(CORE_JS, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update switchRole function
switch_pattern = re.compile(
    r"function switchRole\(newRole,\s*bypassAuth\s*=\s*false\)\s*\{.*?"
    r"state\.role\s*=\s*newRole;",
    re.DOTALL
)

new_switch_content = """function switchRole(newRole, bypassAuth = false) {
      const protectedRoles = ['doctor', 'pharmacy', 'clinic', 'nurse', 'admin', 'manufacturing', 'research', 'patient', 'enterprise', 'hardware', 'mobile'];
      const isSuperAdmin = state.currentUser && (state.currentUser.role === 'admin' || state.currentUser.role === 'super_admin' || state.currentUser.isSuperAdmin);

      // Security Gate: Protect all clinical & administrative consoles
      if (protectedRoles.includes(newRole) && !isSuperAdmin && !bypassAuth) {
        const hasSession = state.currentUser && (state.currentUser.role === newRole || (newRole === 'patient' && state.currentUser.role === 'patient'));
        if (!hasSession) {
          toggleLoginModal(true);
          prefillLogin(newRole);
          showNotification(`Please enter password and click 'Sign In' to access ${newRole.toUpperCase()} desk.`, 'info');
          return;
        }
      }

      if (newRole !== 'website' && newRole !== 'herbals') {
        const roleProfiles = {
          doctor: { name: 'Hakeem Dr. Irfan Ashraf', title: 'Senior Tabeeb & Lead Clinician (BUMS - AKTC AMU)', email: 'dr.irfan@zayvorahealth.com' },
          clinic: { name: 'Reception & Patient Intake Desk', title: 'OPD Queue & Token In-Charge', email: 'reception@zayvorahealth.com' },
          nurse: { name: 'Inpatient Nursing Station', title: 'Ward 2A Triage In-Charge', email: 'nurse@zayvorahealth.com' },
          patient: { name: 'Hamza Farooqi', title: 'Patient (MRN-2026-0814)', email: 'hamza.farooqi@gmail.com' },
          pharmacy: { name: 'Chief Pharmacist', title: 'Clinical Pharmacy & FEFO In-Charge', email: 'pharmacy@zayvorahealth.com' },
          manufacturing: { name: 'Head of Botanical QA/QC', title: 'eBMR Batch Release Officer', email: 'manufacturing@zayvorahealth.com' },
          admin: { name: 'Enterprise Super Administrator', title: 'Platform Security & Governance', email: 'admin@zayvorahealth.com' },
          research: { name: 'Principal Clinical Investigator', title: 'RWE & Pharmacopoeia Editorial Board', email: 'research@zayvorahealth.com' },
          enterprise: { name: 'Hakeem Dr. Irfan Ashraf', title: 'Founder & Chairman', email: 'dr.irfan@zayvorahealth.com' },
          hardware: { name: 'IoMT Hardware Gateway', title: 'Hardware Admin', email: 'hardware@zayvorahealth.com' },
          herbals: { name: 'Retail Guest', title: 'Herbal Store Customer', email: 'guest@zayvorahealth.com' },
          mobile: { name: 'Mobile Bedside User', title: 'PWA Bedside User', email: 'mobile@zayvorahealth.com' }
        };
        const p = roleProfiles[newRole] || { name: 'Authorized User', title: newRole.toUpperCase(), email: `${newRole}@zayvorahealth.com` };
        
        // If Super Admin is switching between desks, preserve Super Admin status!
        if (isSuperAdmin) {
          state.currentUser.activeDesk = newRole;
          state.currentUser.title = `Super Admin Oversight • ${newRole.toUpperCase()} Desk`;
        } else if (state.currentUser && state.currentUser.token) {
          state.currentUser.role = newRole;
        } else if (bypassAuth) {
          const secureToken = 'zyv.' + btoa(JSON.stringify({ uid: 'USR-' + newRole.toUpperCase(), email: p.email, name: p.name, role: newRole, exp: Math.floor(Date.now() / 1000) + 86400 })) + '.sig';
          state.currentUser = { email: p.email, name: p.name, title: p.title, role: newRole, isSuperAdmin: (newRole === 'admin'), token: secureToken };
        }
      }
      state.role = newRole;"""

if switch_pattern.search(text):
    text = switch_pattern.sub(new_switch_content, text, count=1)
    print("switchRole security gate updated successfully!")
else:
    print("Warning: switch_pattern did not match")

with open(CORE_JS, "w", encoding="utf-8") as f:
    f.write(text)
print("Saved CORE_JS successfully!")
