/**
 * Modal — ZAYVORA Design System
 *
 * An accessible dialog overlay with backdrop, close button, and
 * composable Header / Body / Footer slots.
 *
 * Accessibility:
 *  - Traps focus inside the dialog while open.
 *  - Closes on Escape key or backdrop click.
 *  - Sets aria-modal, role="dialog", and aria-labelledby automatically.
 *
 * @module design-system/Modal
 */

'use client';

import React, {
  HTMLAttributes,
  KeyboardEvent,
  ReactNode,
  useCallback,
  useEffect,
  useId,
  useRef,
} from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type ModalSize = 'sm' | 'md' | 'lg' | 'xl' | 'full';

export interface ModalProps {
  /** Controls visibility. */
  open: boolean;
  /** Called when the modal requests closure (Escape / backdrop / close btn). */
  onClose: () => void;
  /** Accessible title rendered in the header bar. */
  title?: ReactNode;
  /** Size preset. Defaults to "md". */
  size?: ModalSize;
  /** Header slot (overrides built-in title/close if provided). */
  header?: ReactNode;
  /** Body content. */
  children?: ReactNode;
  /** Footer slot — typically action buttons. */
  footer?: ReactNode;
  /** Prevent closing via backdrop click. Defaults to false. */
  disableBackdropClose?: boolean;
  /** Additional class names for the dialog panel. */
  className?: string;
}

export interface ModalSectionProps extends HTMLAttributes<HTMLDivElement> {}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const sizeClasses: Record<ModalSize, string> = {
  sm:   'max-w-sm',
  md:   'max-w-lg',
  lg:   'max-w-2xl',
  xl:   'max-w-4xl',
  full: 'max-w-full mx-4',
};

// ─────────────────────────────────────────────────────────────────────────────
// Close button icon
// ─────────────────────────────────────────────────────────────────────────────

const CloseIcon: React.FC = () => (
  <svg
    aria-hidden="true"
    className="h-5 w-5"
    viewBox="0 0 20 20"
    fill="currentColor"
  >
    <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22z" />
  </svg>
);

// ─────────────────────────────────────────────────────────────────────────────
// Sub-components (exported for direct use)
// ─────────────────────────────────────────────────────────────────────────────

export const ModalBody: React.FC<ModalSectionProps> = ({
  children,
  className,
  ...rest
}) => (
  <div
    className={twMerge(clsx('px-6 py-4 overflow-y-auto flex-1'), className)}
    {...rest}
  >
    {children}
  </div>
);
ModalBody.displayName = 'Modal.Body';

export const ModalFooter: React.FC<ModalSectionProps> = ({
  children,
  className,
  ...rest
}) => (
  <div
    className={twMerge(
      clsx(
        'px-6 py-4 border-t border-gray-100',
        'bg-[#F3F3EE] rounded-b-2xl',
        'flex items-center justify-end gap-3',
      ),
      className,
    )}
    {...rest}
  >
    {children}
  </div>
);
ModalFooter.displayName = 'Modal.Footer';

// ─────────────────────────────────────────────────────────────────────────────
// Main Modal component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Modal component.
 *
 * @example
 * <Modal
 *   open={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   title="Confirm Prescription"
 *   size="md"
 *   footer={
 *     <>
 *       <Button variant="ghost" onClick={() => setIsOpen(false)}>Cancel</Button>
 *       <Button variant="primary" onClick={handleConfirm}>Confirm</Button>
 *     </>
 *   }
 * >
 *   <p>Are you sure you want to issue this prescription?</p>
 * </Modal>
 */
export const Modal: React.FC<ModalProps> = ({
  open,
  onClose,
  title,
  size                = 'md',
  header,
  children,
  footer,
  disableBackdropClose = false,
  className,
}) => {
  const titleId   = useId();
  const panelRef  = useRef<HTMLDivElement>(null);
  const closeRef  = useRef<HTMLButtonElement>(null);

  // ── Focus trap ─────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!open) return;

    // Move focus to close button on open
    const frame = requestAnimationFrame(() => closeRef.current?.focus());

    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === 'Escape') { onClose(); return; }
      if (e.key !== 'Tab') return;

      const panel = panelRef.current;
      if (!panel) return;

      const focusable = Array.from(
        panel.querySelectorAll<HTMLElement>(
          'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',
        ),
      ).filter((el) => !el.closest('[hidden]'));

      if (!focusable.length) { e.preventDefault(); return; }

      const first = focusable[0];
      const last  = focusable[focusable.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) { e.preventDefault(); last.focus(); }
      } else {
        if (document.activeElement === last)  { e.preventDefault(); first.focus(); }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [open, onClose]);

  // ── Scroll lock ────────────────────────────────────────────────────────────
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  const handleBackdrop = useCallback(() => {
    if (!disableBackdropClose) onClose();
  }, [disableBackdropClose, onClose]);

  if (!open) return null;

  return (
    /* Backdrop */
    <div
      className={clsx(
        'fixed inset-0 z-[1040] flex items-center justify-center p-4',
        'bg-black/50 backdrop-blur-sm',
        'animate-[fadeIn_150ms_ease]',
      )}
      aria-hidden="true"
      onClick={handleBackdrop}
    >
      {/* Dialog panel */}
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? titleId : undefined}
        className={twMerge(
          clsx(
            'relative z-[1050] flex flex-col w-full',
            'bg-[#FAFAF7] rounded-2xl',
            'shadow-[0_20px_48px_-8px_rgb(0_0_0/0.24),0_8px_16px_-4px_rgb(0_0_0/0.12)]',
            'max-h-[90vh]',
            'animate-[slideUp_200ms_ease]',
            sizeClasses[size],
            className,
          ),
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        {header ?? (
          <div className="flex items-center justify-between gap-4 px-6 py-4 border-b border-gray-100 shrink-0">
            {title && (
              <h2
                id={titleId}
                className="text-lg font-semibold text-[#1A1A1A] leading-snug"
              >
                {title}
              </h2>
            )}
            <button
              ref={closeRef}
              onClick={onClose}
              aria-label="Close dialog"
              className={clsx(
                'ml-auto rounded-lg p-1.5',
                'text-[#6B7280] hover:text-[#1A1A1A] hover:bg-gray-100',
                'transition-colors duration-150 outline-none',
                'focus-visible:ring-2 focus-visible:ring-[#2D6A4F] focus-visible:ring-offset-1',
              )}
            >
              <CloseIcon />
            </button>
          </div>
        )}

        {/* Body */}
        {children && (
          <ModalBody>{children}</ModalBody>
        )}

        {/* Footer */}
        {footer && <ModalFooter>{footer}</ModalFooter>}
      </div>
    </div>
  );
};

Modal.displayName = 'Modal';

export default Modal;
