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
      throw new Error("Please consent to clinical record creation and HIPAA/ABDM data processing.");
    }

    // 2. Duplicate prevention
    const dedupeKey = `${cleanMobile}-${req.preferredDate}-${req.preferredTime}`;
    if (this.bookedReferences.has(dedupeKey)) {
      throw new Error("A booking request for this mobile and time slot is already being processed. Please check your messages.");
    }
    this.bookedReferences.add(dedupeKey);

    // 3. Generate Reference Code
    const randomSuffix = Math.floor(1000 + Math.random() * 9000);
    const refCode = `ZAY-APT-2026-${randomSuffix}`;
    const tokenNumber = `T-${Math.floor(100 + Math.random() * 900)}`;

    // Simulate async network processing
    await new Promise((resolve) => setTimeout(resolve, 300));

    return {
      success: true,
      referenceNumber: refCode,
      scheduledDate: req.preferredDate,
      scheduledTime: req.preferredTime,
      doctorName: req.doctorPreference || "Senior Consulting Tabeeb (Assigned by Specialization)",
      mode: req.consultationType,
      facilityLocation: req.consultationType === "In-Clinic OPD"
        ? "Jamia Hamdard AUTC - Main Hospital, OPD Wing, New Delhi"
        : "Secure Encrypted Video Teleconsultation Room (WebRTC)",
      tokenNumber: tokenNumber,
      message: `Your appointment request has been confirmed under reference ${refCode}. Our patient coordinator has dispatched booking confirmation details.`,
      notificationChannels: {
        smsDispatched: true,
        whatsAppDispatched: true,
        emailDispatched: true
      }
    };
  }
}
