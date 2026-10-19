import React, { forwardRef } from "react";

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  helperText?: string;
  error?: string;
  required?: boolean;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, options, helperText, error, required, disabled, className = "", id, ...props }, ref) => {
    const selectId = id || (label ? `select-${label.toLowerCase().replace(/\s+/g, "-")}` : undefined);

    return (
      <div className="w-full flex flex-col gap-1.5">
        {label && (
          <label htmlFor={selectId} className="text-xs font-semibold text-slate-300 flex items-center gap-1">
            <span>{label}</span>
            {required && <span className="text-red-400">*</span>}
          </label>
        )}
        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            disabled={disabled}
            aria-invalid={!!error}
            aria-describedby={error ? `${selectId}-error` : helperText ? `${selectId}-helper` : undefined}
            className={`w-full appearance-none px-3 py-2.5 rounded-xl text-sm transition border bg-[#0A0F1D] text-white focus:outline-none focus:ring-2 focus:ring-[#2D6A4F] ${
              error
                ? "border-red-500 focus:border-red-500 focus:ring-red-500/20"
                : "border-slate-800 focus:border-[#2D6A4F]"
            } ${disabled ? "opacity-50 cursor-not-allowed bg-slate-900" : ""} ${className}`}
            {...props}
          >
            {options.map((opt) => (
              <option key={opt.value} value={opt.value} disabled={opt.disabled} className="bg-[#0A0F1D] text-white">
                {opt.label}
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
        {error && (
          <span id={`${selectId}-error`} role="alert" className="text-xs text-red-400 font-medium">
            {error}
          </span>
        )}
        {!error && helperText && (
          <span id={`${selectId}-helper`} className="text-xs text-slate-400">
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Select.displayName = "Select";
