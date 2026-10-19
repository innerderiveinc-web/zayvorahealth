/**
 * Input — ZAYVORA Design System
 *
 * A fully-accessible form input with label, helper text, error state,
 * and optional leading/trailing icon slots.
 *
 * @module design-system/Input
 */

import React, {
  InputHTMLAttributes,
  forwardRef,
  useId,
} from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type InputSize = 'sm' | 'md' | 'lg';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  /** Visible label rendered above the field. */
  label?: string;
  /** Helper text shown below the field (suppressed when error is set). */
  helperText?: string;
  /** Validation error message. Puts the input in an error state. */
  error?: string;
  /** Icon / element rendered inside the leading edge of the input. */
  leadingIcon?: React.ReactNode;
  /** Icon / element rendered inside the trailing edge of the input. */
  trailingIcon?: React.ReactNode;
  /** Size preset. Defaults to "md". */
  inputSize?: InputSize;
  /** Fills the full width of the parent container. */
  fullWidth?: boolean;
  /** Visually mark the field as required. */
  required?: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const sizeClasses: Record<InputSize, { input: string; icon: string }> = {
  sm: { input: 'h-8  text-sm px-3',  icon: 'h-4 w-4' },
  md: { input: 'h-10 text-sm px-4',  icon: 'h-4 w-4' },
  lg: { input: 'h-12 text-base px-4', icon: 'h-5 w-5' },
};

const baseInput = [
  'block w-full rounded-lg border bg-white',
  'text-[#1A1A1A] placeholder:text-[#6B7280]',
  'transition-colors duration-150 outline-none',
  'disabled:bg-[#F3F3EE] disabled:text-[#6B7280] disabled:cursor-not-allowed',
].join(' ');

const normalBorder = [
  'border-gray-300',
  'hover:border-[#2D6A4F]',
  'focus:border-[#2D6A4F] focus:ring-2 focus:ring-[#2D6A4F]/20',
].join(' ');

const errorBorder = [
  'border-[#DC2626]',
  'hover:border-[#B91C1C]',
  'focus:border-[#DC2626] focus:ring-2 focus:ring-[#DC2626]/20',
].join(' ');

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Input component.
 *
 * @example
 * <Input
 *   label="Patient Name"
 *   placeholder="e.g. Ahmed Khan"
 *   helperText="Enter full name as on CNIC"
 *   leadingIcon={<UserIcon />}
 * />
 *
 * @example
 * <Input label="Email" type="email" error="Invalid email address" />
 */
export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      leadingIcon,
      trailingIcon,
      inputSize = 'md',
      fullWidth = true,
      required  = false,
      className,
      id: externalId,
      disabled,
      ...rest
    },
    ref,
  ) => {
    const generatedId = useId();
    const id          = externalId ?? generatedId;
    const helpId      = `${id}-help`;
    const errorId     = `${id}-error`;
    const hasError    = Boolean(error);
    const sizes       = sizeClasses[inputSize];

    return (
      <div className={clsx('flex flex-col gap-1.5', fullWidth && 'w-full')}>
        {/* Label */}
        {label && (
          <label
            htmlFor={id}
            className="block text-sm font-medium text-[#1A1A1A] select-none"
          >
            {label}
            {required && (
              <span aria-hidden="true" className="ml-1 text-[#DC2626]">
                *
              </span>
            )}
          </label>
        )}

        {/* Input wrapper */}
        <div className="relative flex items-center">
          {/* Leading icon */}
          {leadingIcon && (
            <span
              aria-hidden="true"
              className={clsx(
                'absolute left-3 flex items-center pointer-events-none',
                'text-[#6B7280]',
                sizes.icon,
              )}
            >
              {leadingIcon}
            </span>
          )}

          <input
            ref={ref}
            id={id}
            disabled={disabled}
            required={required}
            aria-required={required}
            aria-invalid={hasError}
            aria-describedby={
              hasError ? errorId : helperText ? helpId : undefined
            }
            className={twMerge(
              clsx(
                baseInput,
                hasError ? errorBorder : normalBorder,
                sizes.input,
                leadingIcon  && 'pl-9',
                trailingIcon && 'pr-9',
                className,
              ),
            )}
            {...rest}
          />

          {/* Trailing icon */}
          {trailingIcon && (
            <span
              aria-hidden="true"
              className={clsx(
                'absolute right-3 flex items-center pointer-events-none',
                hasError ? 'text-[#DC2626]' : 'text-[#6B7280]',
                sizes.icon,
              )}
            >
              {trailingIcon}
            </span>
          )}
        </div>

        {/* Error message */}
        {hasError && (
          <p
            id={errorId}
            role="alert"
            className="text-xs text-[#DC2626] flex items-center gap-1"
          >
            <svg
              aria-hidden="true"
              className="h-3.5 w-3.5 shrink-0"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0zm-8-5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5A.75.75 0 0 1 10 5zm0 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"
                clipRule="evenodd"
              />
            </svg>
            {error}
          </p>
        )}

        {/* Helper text (hidden when error shown) */}
        {!hasError && helperText && (
          <p id={helpId} className="text-xs text-[#6B7280]">
            {helperText}
          </p>
        )}
      </div>
    );
  },
);

Input.displayName = 'Input';

export default Input;
