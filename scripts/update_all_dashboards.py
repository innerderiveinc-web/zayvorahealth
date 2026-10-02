import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Original length:", len(text))

# Let's define the new renderers
new_helpers = '''
    // =========================================================================
    // GLOBAL MISSING HELPERS & CLINICAL INTERACTION ENGINE
    // =========================================================================
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

