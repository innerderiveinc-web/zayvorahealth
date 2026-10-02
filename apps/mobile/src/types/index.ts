export interface User {
  id: string; email: string; name: string; role: 'patient' | 'clinician' | 'admin';
  organization_id?: string; is_active: boolean;
}

export interface Patient {
  id: string; user_id: string; mrn: string; date_of_birth: string;
  gender: string; mizaj_type?: 'Damawi' | 'Safrawi' | 'Balghami' | 'Sawdawi';
  phone?: string; blood_group?: string;
}

export interface Appointment {
  id: string; patient_id: string; clinician_id: string; scheduled_at: string;
  status: 'scheduled' | 'completed' | 'cancelled' | 'no_show';
  notes?: string; doctor_name?: string; clinic_name?: string;
}

export interface Prescription {
  id: string; patient_id: string; clinician_id: string; created_at: string;
  formulations: Array<{ name: string; dose: string; frequency: string; duration: string }>;
  notes?: string; status: 'active' | 'completed' | 'cancelled';
}

export interface LabResult {
  id: string; patient_id: string; panel_name: string; collected_at: string;
  status: 'normal' | 'abnormal' | 'pending';
  tests: Array<{ name: string; value: string; unit: string; reference_range: string; flag?: 'H' | 'L' | 'N' }>;
}

export interface Notification {
  id: string; title: string; body: string; category: string;
  read: boolean; created_at: string;
}

export type MizajType = 'Damawi' | 'Safrawi' | 'Balghami' | 'Sawdawi';
