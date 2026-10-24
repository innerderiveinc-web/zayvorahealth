import sys
from gen_patient_app import get_patient_app_code
from gen_doctor_app import get_doctor_app_code
from gen_clinic_app import get_clinic_app_code
from gen_remaining_apps import (
    get_pharmacy_app_code,
    get_research_app_code,
    get_admin_app_code,
    get_enterprise_app_code,
    get_manufacturing_app_code,
    get_herbals_app_code,
    get_mobile_app_code,
    get_hardware_app_code
)

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Original index.html length:", len(text))

# Define all blocks in top-to-bottom order
blocks = [
    ('Patient', 'function renderPatientApp(', 'function renderDoctorApp(', get_patient_app_code()),
    ('Doctor', 'function renderDoctorApp(', 'function renderSingleConsultationWorkspace(', get_doctor_app_code()),
    ('Clinic', 'function renderClinicApp(', 'function renderPharmacyApp(', get_clinic_app_code()),
    ('Pharmacy', 'function renderPharmacyApp(', 'function renderResearchApp(', get_pharmacy_app_code()),
    ('Research', 'function renderResearchApp(', 'function renderAdminApp(', get_research_app_code()),
    ('Admin', 'function renderAdminApp(', 'function renderEnterpriseApp(', get_admin_app_code()),
    ('Enterprise', 'function renderEnterpriseApp(', 'function renderManufacturingApp(', get_enterprise_app_code()),
    ('Manufacturing', 'function renderManufacturingApp(', 'function viewWebsitePage(', get_manufacturing_app_code()),
    ('Herbals', 'function renderHerbalsApp(', 'let mobileActiveScreen =', get_herbals_app_code()),
    ('Mobile', 'let mobileActiveScreen =', 'function renderHardwareApp(', get_mobile_app_code()),
    ('Hardware', 'function renderHardwareApp(', 'function toggleSearchModal(', get_hardware_app_code()),
]

# Calculate start and end indices for all blocks first
ranges = []
for name, s_str, e_str, code in blocks:
    i1 = text.find(s_str)
    i2 = text.find(e_str, i1)
    if i1 == -1 or i2 == -1 or i2 <= i1:
        print(f"Error locating {name}: {i1} to {i2}")
        sys.exit(1)
    
    # Adjust i1 to beginning of line
    ls = text.rfind('\n', 0, i1)
    if ls != -1:
        i1 = ls + 1
    
    # Adjust i2 backward across comment lines
    le = text.rfind('\n', 0, i2)
    while True:
        prev_ls = text.rfind('\n', 0, le)
        if prev_ls == -1: break
        prev_line = text[prev_ls+1:le].strip()
        if prev_line.startswith('//') or prev_line == '':
            le = prev_ls
        else:
            break
            
    ranges.append((i1, le + 1, name, code))
    print(f"Located {name:<15}: [{i1} : {le + 1}]")

# Execute replacements in REVERSE order
for i1, i2, name, code in reversed(ranges):
    text = text[:i1] + code + "\n\n    " + text[i2:]
    print(f"Applied replacement for {name}")

# Inject missing helpers right before toggleSearchModal
helpers_marker = "function toggleSearchModal("
p_h = text.find(helpers_marker)
if p_h != -1 and 'function insertAiRecommendationToPlan' not in text:
    missing_helpers_code = '''// Global clinical copilot & queue helpers
    function insertAiRecommendationToPlan() {
      const planInput = document.getElementById('consultation-plan-text');
      const rec = "Standardized Tanqiya Protocol (Day 1-7): Habb-e-Suranjan 2 tab BID + Arq Mako 25ml with warm water. Dietary: Zero cold water, avoid acidic curds.";
      if (planInput) {
        planInput.value = (planInput.value ? planInput.value + "\\n\\n" : "") + "[HAKEEM SAHAB AI RECOMMENDATION]: " + rec;
      }
      showNotification('Hakeem Sahab AI recommendation inserted into Active Encounter Care Plan.', 'success');
      toggleHakeemDrawer(false);
    }

    let currentQueueTokenIndex = 2;
    const queueTokens = [
      { token: "A-12", patient: "Rashid Minhas", room: "201", dr: "Dr. Aisha", status: "IN CONSULTATION" },
      { token: "A-13", patient: "Zubaida Begum", room: "202", dr: "Dr. Akhtar", status: "IN CONSULTATION" },
      { token: "A-14", patient: "Hamza Farooqi", room: "204", dr: "Dr. Irfan", status: "CALLED NOW" },
      { token: "A-15", patient: "Bilal Ahmad", room: "204", dr: "Dr. Irfan", status: "WAITING (NEXT)" },
      { token: "A-16", patient: "Fatima Noor", room: "201", dr: "Dr. Aisha", status: "CHECKED IN" }
    ];

    function callNextPatientQueue() {
      currentQueueTokenIndex = (currentQueueTokenIndex + 1) % queueTokens.length;
      const nextPat = queueTokens[currentQueueTokenIndex];
      showNotification(`🔔 Calling Token #${nextPat.token}: ${nextPat.patient} to Room ${nextPat.room} (${nextPat.dr})`, 'success');
      if (state.role === 'clinic' && state.tab === 'queue') {
        renderClinicApp(document.getElementById('workspace-container'));
      }
    }

    let patientChatMessages = [
      { sender: "doctor", name: "Hakim Dr. Tariq Mansoor", time: "Yesterday 04:30 PM", text: "Salam Hamza, please ensure you take Suranjan after warm milk, not cold water. Report any morning stiffness." },
      { sender: "patient", name: "Hamza Farooqi", time: "Today 09:15 AM", text: "Wa alaykumu s-salam Dr. Sahib. Stiffness has reduced by nearly 40%. Walking is much easier this morning." },
      { sender: "doctor", name: "Hakim Dr. Tariq Mansoor", time: "Today 10:00 AM", text: "Alhamdulillah. Keep following the diet strictly. We will review your knee mobility in Room 204." }
    ];

    function sendPatientChatMessage() {
      const input = document.getElementById('chat-input-field');
      if (!input || !input.value.trim()) return;
      patientChatMessages.push({
        sender: state.role === 'doctor' ? 'doctor' : 'patient',
        name: state.role === 'doctor' ? 'Hakim Dr. Irfan' : 'Hamza Farooqi',
        time: 'Just now',
        text: input.value.trim()
      });
      input.value = '';
      if (state.role === 'patient') {
        renderPatientApp(document.getElementById('workspace-container'));
      } else if (state.role === 'doctor') {
        renderDoctorApp(document.getElementById('workspace-container'));
      }
      showNotification('Clinical message dispatched securely.', 'success');
    }

    '''
    # Put before the comment line above toggleSearchModal
    ls = text.rfind('\n', 0, p_h)
    text = text[:ls+1] + missing_helpers_code + text[ls+1:]
    print("Injected missing helpers!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS! index.html & docs/index.html updated! Final length: {len(text)}")
