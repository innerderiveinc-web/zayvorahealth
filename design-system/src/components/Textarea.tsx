import React, { forwardRef } from "react";

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  helperText?: string;
  error?: string;
  required?: boolean;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, helperText, error, required, disabled, className = "", id, rows = 4, ...props }, ref) => {
    const textareaId = id || (label ? `textarea-${label.toLowerCase().replace(/\s+/g, "-")}` : undefined);

    return (
      <div className="w-full flex flex-col gap-1.5">
        {label && (
          <label htmlFor={textareaId} className="text-xs font-semibold text-slate-300 flex items-center gap-1">
            <span>{label}</span>
            {required && <span className="text-red-400">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          rows={rows}
          disabled={disabled}
          aria-invalid={!!error}
          aria-describedby={error ? `${textareaId}-error` : helperText ? `${textareaId}-helper` : undefined}
          className={`w-full px-3 py-2 rounded-xl text-sm transition border bg-[#0A0F1D] text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-[#2D6A4F] ${
            error
              ? "border-red-500 focus:border-red-500 focus:ring-red-500/20"
              : "border-slate-800 focus:border-[#2D6A4F]"
          } ${disabled ? "opacity-50 cursor-not-allowed bg-slate-900" : ""} ${className}`}
          {...props}
        />
        {error && (
          <span id={`${textareaId}-error`} role="alert" className="text-xs text-red-400 font-medium">
            {error}
          </span>
        )}
        {!error && helperText && (
          <span id={`${textareaId}-helper`} className="text-xs text-slate-400">
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Textarea.displayName = "Textarea";
