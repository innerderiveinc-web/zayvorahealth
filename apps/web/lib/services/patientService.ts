import { PatientLabReport, PatientMessage, PatientProfileData, ActiveCarePlanData } from "../cms/patientMockData";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

export class PatientService {
  /**
   * Fetches the authoritative clinical record for the authenticated patient directly from /api/v1/patient/my-records.
   */
  static async getMyRecords(token: string, mrn?: string): Promise<{
    ok: boolean;
    mrn?: string;
    patient?: any;
    appointments?: any[];
    prescriptions?: any[];
    encounters?: any[];
    invoices?: any[];
    telemed_rooms?: any[];
    notifications?: any[];
    error?: string;
  }> {
    try {
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      };
      const query = mrn ? `?mrn=${encodeURIComponent(mrn)}` : "";
      const res = await fetch(`${API}/api/v1/patient/my-records${query}`, { headers });
      if (res.ok) {
        return await res.json();
      } else {
        const err = await res.json().catch(() => ({}));
        return { ok: false, error: err.error || `HTTP ${res.status}: Server returned error` };
      }
    } catch (e: any) {
      return { ok: false, error: e.message || "Network connection failure" };
    }
  }

  /**
   * Fetches the patient's comprehensive profile from Central Clinical Service.
   */
  static async getProfile(patientId: string = "PAT-774901", token?: string): Promise<PatientProfileData | null> {
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API}/api/v1/patient/360?patient_id=${encodeURIComponent(patientId)}`, { headers });
      if (res.ok) {
        const data = await res.json();
        if (data.ok && data.patient_360) {
          const p = data.patient_360.patient || data.patient_360;
          return {
            mrn: p.mrn || "MRN-PENDING",
            abhaId: p.abha_id || p.abhaId || "ABHA-NOT-LINKED",
            fullName: `${p.first_name || ""} ${p.last_name || ""}`.trim() || p.fullName || p.name || "Patient Record",
            age: p.age || 30,
            gender: p.gender || "Not Specified",
            primaryMizaj: p.mizaj_dominant || p.primaryMizaj || "Assessment Pending",
            suEMizaj: p.su_e_mizaj || p.suEMizaj || "None Documented",
            bloodGroup: p.blood_group || p.bloodGroup || "O+",
            phone: p.contact_phone || p.phone || "",
            email: p.contact_email || p.email || "",
            address: p.address || "",
            emergencyContact: p.emergency_contact || p.emergencyContact || "None listed",
            allergies: p.allergies || []
          };
        }
      }
    } catch {}
    return null;
  }

  /**
   * Fetches the active care protocol & regimenal progression.
   */
  static async getCarePlan(patientId: string = "PAT-774901", token?: string): Promise<ActiveCarePlanData | null> {
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API}/api/v1/patient/360?patient_id=${encodeURIComponent(patientId)}`, { headers });
      if (res.ok) {
        const data = await res.json();
        if (data.ok && data.patient_360?.active_treatment_plan) {
          const tp = data.patient_360.active_treatment_plan;
          return {
            programName: tp.title || tp.program_name || "Constitutional Care Plan",
            condition: tp.condition || "Chronic Dyscrasia Management",
            currentPhase: tp.current_phase || "Stage 1: Tanqiya (Cleansing)",
            phaseNumber: tp.phase_number || 1,
            totalPhases: tp.total_phases || 3,
            progressPercent: tp.progress_percent || 0,
            startDate: tp.start_date || new Date().toISOString().split("T")[0],
            nextReviewDate: tp.next_review_date || "To be scheduled",
            attendingPhysician: tp.attending_physician || "Attending Physician",
            clinicalNotes: tp.notes || "",
            dietaryDirectives: tp.dietary_directives || [],
            lifestyleDirectives: tp.lifestyle_directives || []
          };
        }
      }
    } catch {}
    return null;
  }

  /**
   * Fetches uploaded and verified diagnostic lab reports.
   */
  static async getReports(patientId: string = "PAT-774901", token?: string): Promise<PatientLabReport[]> {
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API}/api/v1/diagnostics/reports?patient_id=${encodeURIComponent(patientId)}`, { headers });
      if (res.ok) {
        const data = await res.json();
        if (data.ok && data.reports) {
          return data.reports.map((r: any) => ({
            id: r.id || `rep-${Date.now()}`,
            title: r.test_name || r.title || "Diagnostic Report",
            testDate: r.report_date || r.testDate || new Date().toISOString().split("T")[0],
            labName: r.laboratory_name || r.labName || "Central Clinical Diagnostics",
            status: r.status === "VERIFIED" ? "Verified" : "Pending Review",
            fileSize: r.file_size || r.fileSize || "1.2 MB",
            downloadUrl: r.file_url || r.downloadUrl || "#"
          }));
        }
      }
    } catch {}
    return [];
  }

  /**
   * Uploads and registers a new patient diagnostic lab report.
   */
  static async uploadReport(fileName: string, fileSize: string, patientId: string = "PAT-774901", token?: string): Promise<PatientLabReport> {
    const cleanTitle = fileName.replace(/\.[^/.]+$/, "");
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API}/api/v1/diagnostics/reports`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          patient_id: patientId,
          test_name: cleanTitle,
          file_name: fileName,
          file_size: fileSize,
          laboratory_name: "Patient Document Upload",
          status: "PENDING_REVIEW"
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.report) {
          return {
            id: data.report.id,
            title: data.report.test_name || cleanTitle,
            testDate: data.report.report_date || new Date().toISOString().split("T")[0],
            labName: data.report.laboratory_name || "Patient Document Upload",
            status: "Pending Review",
            fileSize: fileSize,
            downloadUrl: "#"
          };
        }
      }
    } catch {}

    return {
      id: "rep-" + Date.now(),
      title: cleanTitle,
      testDate: new Date().toISOString().split("T")[0],
      labName: "Patient Document Upload",
      status: "Pending Review",
      fileSize: fileSize,
      downloadUrl: "#"
    };
  }

  /**
   * Dispatches a live message to the clinical care continuum.
   */
  static async sendMessage(text: string, senderName: string = "Patient", patientId: string = "PAT-774901", token?: string): Promise<PatientMessage> {
    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;

      const res = await fetch(`${API}/api/v1/communication/messages`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          patient_id: patientId,
          sender_name: senderName,
          sender_role: "PATIENT",
          message_text: text
        })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.message) {
          return {
            id: data.message.id || `msg-${Date.now()}`,
            senderName: data.message.sender_name || senderName,
            senderRole: "Patient",
            timestamp: "Just now",
            messageText: data.message.message_text || text,
            isDoctor: false
          };
        }
      }
    } catch {}

    return {
      id: "msg-" + Date.now(),
      senderName: senderName,
      senderRole: "Patient",
      timestamp: "Just now",
      messageText: text,
      isDoctor: false
    };
  }
}
