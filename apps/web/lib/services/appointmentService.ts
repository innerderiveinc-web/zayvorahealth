export interface AppointmentBookingRequest {
  fullName: string;
  mobile: string;
  email: string;
  age: number;
  gender: string;
  healthConcern: string;
  consultationType: "Online Video Consultation" | "In-Clinic OPD";
  preferredDate: string;
  preferredTime: string;
  doctorPreference: string;
  additionalMessage?: string;
  hasPreviousReports?: boolean;
  consentAccepted: boolean;
}

export interface AppointmentBookingResult {
  success: boolean;
  referenceNumber: string;
  scheduledDate: string;
  scheduledTime: string;
  doctorName: string;
  mode: string;
  facilityLocation: string;
  tokenNumber: string;
  message: string;
  notificationChannels: {
    smsDispatched: boolean;
    whatsAppDispatched: boolean;
    emailDispatched: boolean;
  };
}

export class AppointmentService {
  private static bookedReferences: Set<string> = new Set();

  static getAvailableSlots(dateStr: string): string[] {
    // Standard OPD clinical slots
    return [
      "09:30 AM – 10:00 AM",
      "10:00 AM – 10:30 AM",
      "10:30 AM – 11:00 AM",
      "11:30 AM – 12:00 PM",
      "12:00 PM – 12:30 PM",
      "02:30 PM – 03:00 PM",
      "03:30 PM – 04:00 PM",
      "04:30 PM – 05:00 PM"
    ];
  }

  static async bookAppointment(req: AppointmentBookingRequest): Promise<AppointmentBookingResult> {
    // 1. Validation checks
    if (!req.fullName || req.fullName.trim().length < 3) {
      throw new Error("Please enter your full legal name (at least 3 characters).");
    }

    const cleanMobile = req.mobile.replace(/\D/g, "");
    if (cleanMobile.length < 10) {
      throw new Error("Please enter a valid 10-digit mobile number.");
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(req.email)) {
      throw new Error("Please enter a valid email address.");
    }

    if (!req.preferredDate) {
      throw new Error("Please select your preferred consultation date.");
    }

    if (!req.preferredTime) {
      throw new Error("Please select an available time slot.");
    }

    if (!req.consentAccepted) {
      throw new Error("Please consent to clinical record creation and DPDP Act 2023 / ABDM data processing.");
    }

    // 2. Duplicate prevention
    const dedupeKey = `${cleanMobile}-${req.preferredDate}-${req.preferredTime}`;
    if (this.bookedReferences.has(dedupeKey)) {
      throw new Error("A booking request for this mobile and time slot is already being processed. Please check your messages.");
    }
    this.bookedReferences.add(dedupeKey);

    // 3. Submit to Live REST API and Central Database
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
    let bookingData: any = null;

    try {
      const res = await fetch(`${API_URL}/api/v1/appointments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patientName: req.fullName,
          date: req.preferredDate,
          timeSlot: req.preferredTime,
          doctorName: req.doctorPreference || "Prof. (Dr.) Mansoor Alam",
          chiefComplaint: req.healthConcern || "General Health Assessment",
          fee: 800.0,
          mobile: cleanMobile,
          email: req.email,
          consultationType: req.consultationType
        })
      });

      if (!res.ok) {
        const errorPayload = await res.json().catch(() => ({}));
        throw new Error(errorPayload.detail || `Clinical appointment scheduling failed (HTTP ${res.status}). Please contact clinic reception.`);
      }

      const body = await res.json();
      if (!body.ok && !body.appointment) {
        throw new Error(body.detail || "Clinical server rejected appointment scheduling. Please verify availability.");
      }
      bookingData = body.appointment || body;
    } catch (err: any) {
      this.bookedReferences.delete(dedupeKey);
      throw new Error(
        err.message || 
        "Unable to reach the clinical appointment service. Please verify your connection or contact ZAYVORA Matab reception at +91 11 4928 0000."
      );
    }

    const refCode = bookingData.id || bookingData.referenceNumber || `ZAY-APT-2026-${Math.floor(1000 + Math.random() * 9000)}`;
    const tokenNumber = bookingData.tokenNumber || bookingData.token_number || "T-101";

    return {
      success: true,
      referenceNumber: refCode,
      scheduledDate: req.preferredDate,
      scheduledTime: req.preferredTime,
      doctorName: req.doctorPreference || "Senior Consulting Tabeeb (Assigned by Specialization)",
      mode: req.consultationType,
      facilityLocation: req.consultationType === "In-Clinic OPD"
        ? "ZAYVORA Matab™ — Central Care Centre, OPD Wing, New Delhi"
        : "Secure Encrypted Video Teleconsultation Room (WebRTC)",
      tokenNumber: tokenNumber,
      message: `Your appointment request has been scheduled on the Central Clinical Server under reference ${refCode}.`,
      notificationChannels: {
        smsDispatched: Boolean(bookingData.smsDispatched ?? bookingData.sms_dispatched ?? false),
        whatsAppDispatched: Boolean(bookingData.whatsAppDispatched ?? bookingData.whatsapp_dispatched ?? false),
        emailDispatched: Boolean(bookingData.emailDispatched ?? bookingData.email_dispatched ?? false)
      }
    };
  }
}
