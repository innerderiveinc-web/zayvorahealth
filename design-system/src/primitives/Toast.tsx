import React, { useEffect } from 'react';
import { twMerge } from 'tailwind-merge';

export type ToastVariant = 'success' | 'warning' | 'error' | 'info';

export interface ToastProps {
  id?: string;
  variant?: ToastVariant;
  title?: string;
  message: string;
  durationMs?: number;
  onDismiss?: (id?: string) => void;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

export const Toast: React.FC<ToastProps> = ({
  id,
  variant = 'info',
  title,
  message,
  durationMs = 4000,
  onDismiss,
  action,
  className = '',
}) => {
  useEffect(() => {
    if (durationMs <= 0 || !onDismiss) return;
    const timer = setTimeout(() => {
      onDismiss(id);
    }, durationMs);
    return () => clearTimeout(timer);
  }, [durationMs, onDismiss, id]);

  const variantConfig = {
    success: {
      bg: 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-500/30 text-emerald-900 dark:text-emerald-200',
      icon: (
        <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      ),
    },
    warning: {
      bg: 'bg-amber-50 dark:bg-amber-950/40 border-amber-500/30 text-amber-900 dark:text-amber-200',
      icon: (
        <svg className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
    },
    error: {
      bg: 'bg-rose-50 dark:bg-rose-950/40 border-rose-500/30 text-rose-900 dark:text-rose-200',
      icon: (
        <svg className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      ),
    },
    info: {
      bg: 'bg-teal-50 dark:bg-teal-950/40 border-teal-500/30 text-teal-900 dark:text-teal-200',
      icon: (
        <svg className="w-5 h-5 text-teal-600 dark:text-teal-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  }[variant];

  return (
    <div
      role="status"
      className={twMerge(
        'flex items-start gap-3 p-3.5 rounded-lg border shadow-lg max-w-sm w-full transition-all duration-200',
        variantConfig.bg,
        className
      )}
    >
      {variantConfig.icon}
      <div className="flex-1 text-xs">
        {title && <div className="font-semibold mb-0.5">{title}</div>}
        <div className="leading-relaxed">{message}</div>
        {action && (
          <button
            type="button"
            onClick={action.onClick}
            className="mt-2 text-xs font-semibold underline underline-offset-2 hover:opacity-80 transition"
          >
            {action.label}
          </button>
        )}
      </div>
      {onDismiss && (
        <button
          type="button"
          onClick={() => onDismiss(id)}
          aria-label="Dismiss toast"
          className="text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 p-0.5"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
};

export interface ToastContainerProps {
  toasts: ToastProps[];
  onDismiss: (id?: string) => void;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
}

export const ToastContainer: React.FC<ToastContainerProps> = ({
  toasts,
  onDismiss,
  position = 'top-right',
}) => {
  const positionClasses = {
    'top-right': 'top-4 right-4 items-end',
    'top-left': 'top-4 left-4 items-start',
    'bottom-right': 'bottom-4 right-4 items-end',
    'bottom-left': 'bottom-4 left-4 items-start',
  }[position];

  if (!toasts.length) return null;

  return (
    <div className={`fixed z-50 flex flex-col gap-2 pointer-events-none ${positionClasses}`}>
      {toasts.map((toast) => (
        <div key={toast.id || toast.message} className="pointer-events-auto">
          <Toast {...toast} onDismiss={onDismiss} />
        </div>
      ))}
    </div>
  );
};
