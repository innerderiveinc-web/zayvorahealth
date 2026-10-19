import React from 'react';

export interface AppointmentItemProps {
  id: string;
  tokenNumber?: string;
  patientOrDoctorName: string;
  titleOrSpecialty?: string;
  dateTime: string;
  mode: 'In-Clinic OPD' | 'Tele-Consultation' | 'Home Visit';
  status: 'SCHEDULED' | 'WAITING' | 'IN_CONSULTATION' | 'COMPLETED' | 'CANCELLED';
  onReschedule?: () => void;
  onCancel?: () => void;
  onJoin?: () => void;
  className?: string;
}

export const AppointmentItem: React.FC<AppointmentItemProps> = ({
  id,
  tokenNumber,
  patientOrDoctorName,
  titleOrSpecialty,
  dateTime,
  mode,
  status,
  onReschedule,
  onCancel,
  onJoin,
  className = '',
}) => {
  const statusColors = {
    SCHEDULED: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    WAITING: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    IN_CONSULTATION: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    COMPLETED: 'bg-gray-500/10 text-gray-400 border-gray-500/30',
    CANCELLED: 'bg-red-500/10 text-red-400 border-red-500/30',
  }[status];

  return (
    <div
      className={`p-4 rounded-xl border border-gray-200 dark:border-slate-800 bg-white dark:bg-slate-900/60 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4 ${className}`}
    >
      <div className="flex items-start gap-3">
        {tokenNumber && (
          <span className="px-3 py-2 rounded-lg font-mono font-bold text-sm bg-brand-primary/10 text-brand-primary dark:bg-emerald-500/10 dark:text-emerald-400 border border-brand-primary/20">
            {tokenNumber}
          </span>
        )}
        <div>
          <div className="flex items-center gap-2">
            <h4 className="font-semibold text-sm text-gray-900 dark:text-gray-100">{patientOrDoctorName}</h4>
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${statusColors}`}>
              {status}
            </span>
          </div>
          {titleOrSpecialty && (
            <p className="text-xs text-gray-500 dark:text-gray-400">{titleOrSpecialty}</p>
          )}
          <p className="text-xs text-gray-600 dark:text-gray-300 mt-1 flex items-center gap-2">
            <span>📅 {dateTime}</span>
            <span>•</span>
            <span>{mode === 'Tele-Consultation' ? '📹 Video' : '🏥 OPD'}</span>
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2 self-end md:self-auto">
        {mode === 'Tele-Consultation' && onJoin && status !== 'COMPLETED' && status !== 'CANCELLED' && (
          <button
            type="button"
            onClick={onJoin}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-500 transition-colors shadow-sm"
          >
            Join Call
          </button>
        )}
        {onReschedule && status !== 'COMPLETED' && status !== 'CANCELLED' && (
          <button
            type="button"
            onClick={onReschedule}
            className="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-300 dark:border-slate-700 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-800 transition-colors"
          >
            Reschedule
          </button>
        )}
        {onCancel && status !== 'COMPLETED' && status !== 'CANCELLED' && (
          <button
            type="button"
            onClick={onCancel}
            className="px-3 py-1.5 text-xs font-medium rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
};
