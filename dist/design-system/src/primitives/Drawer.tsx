import React, { useEffect, useRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export type DrawerPlacement = 'right' | 'left' | 'bottom';
export type DrawerSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
  placement?: DrawerPlacement;
  size?: DrawerSize;
  closeOnBackdrop?: boolean;
  closeOnEsc?: boolean;
  className?: string;
  id?: string;
}

const sizeClasses: Record<DrawerPlacement, Record<DrawerSize, string>> = {
  right: {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full',
  },
  left: {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full',
  },
  bottom: {
    sm: 'max-h-64',
    md: 'max-h-96',
    lg: 'max-h-[600px]',
    xl: 'max-h-[800px]',
    full: 'max-h-full',
  },
};

export const Drawer: React.FC<DrawerProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  footer,
  placement = 'right',
  size = 'md',
  closeOnBackdrop = true,
  closeOnEsc = true,
  className = '',
  id,
}) => {
  const drawerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen || !closeOnEsc) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, closeOnEsc, onClose]);

  if (!isOpen) return null;

  const placementClass = {
    right: 'inset-y-0 right-0 h-full transform transition-transform duration-300 ease-in-out',
    left: 'inset-y-0 left-0 h-full transform transition-transform duration-300 ease-in-out',
    bottom: 'inset-x-0 bottom-0 w-full transform transition-transform duration-300 ease-in-out',
  }[placement];

  return (
    <div
      id={id}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 overflow-hidden"
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
        onClick={() => closeOnBackdrop && onClose()}
        aria-hidden="true"
      />

      <div className={twMerge('fixed z-50 flex flex-col bg-[#FAFAF7] dark:bg-stone-900 border-stone-200 dark:border-stone-800 shadow-2xl', placementClass, sizeClasses[placement][size], className)}>
        {/* Header */}
        <div className="flex items-start justify-between p-4 border-b border-stone-200 dark:border-stone-800">
          <div>
            {title && (
              <h2 className="text-base font-semibold text-stone-900 dark:text-stone-100">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="mt-0.5 text-xs text-stone-500 dark:text-stone-400">
                {subtitle}
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close drawer"
            className="p-1 rounded-lg text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800 transition"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="p-4 border-t border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};
