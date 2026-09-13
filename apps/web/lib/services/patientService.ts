import { MOCK_PATIENT_PROFILE, MOCK_CARE_PLAN, MOCK_REPORTS, MOCK_MESSAGES, PatientLabReport, PatientMessage } from "../cms/patientMockData";

export class PatientService {
  static getProfile() {
    return MOCK_PATIENT_PROFILE;
  }

  static getCarePlan() {
    return MOCK_CARE_PLAN;
  }

  static getReports(): PatientLabReport[] {
    return MOCK_REPORTS;
  }

  static uploadReport(fileName: string, fileSize: string): PatientLabReport {
    const newReport: PatientLabReport = {
      id: ,
      title: fileName.replace(/\.[^/.]+$/, ""),
      testDate: new Date().toISOString().split("T")[0],
      labName: "Patient Uploaded Document",
      status: "Pending Review",
      fileSize: fileSize,
      downloadUrl: "#"
    };
    return newReport;
  }

  static sendMessage(text: string): PatientMessage {
    return {
      id: ,
      senderName: "Hamza Farooqi",
      senderRole: "Patient",
      timestamp: "Just now",
      messageText: text,
      isDoctor: false
    };
  }
}
