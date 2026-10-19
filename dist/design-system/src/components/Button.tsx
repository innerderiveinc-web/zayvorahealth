/**
 * Button — ZAYVORA Design System
 *
 * A polymorphic button component with brand variants, sizes,
 * disabled and loading states.
 *
 * @module design-system/Button
 */

import React, { ButtonHTMLAttributes, forwardRef } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ButtonSize    = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style of the button. Defaults to "primary". */
  variant?: ButtonVariant;
  /** Size preset. Defaults to "md". */
  size?: ButtonSize;
  /** Show an inline loading spinner and disable interactions. */
  loading?: boolean;
  /** Icon to render to the left of children. */
  leftIcon?: React.ReactNode;
  /** Icon to render to the right of children. */
  rightIcon?: React.ReactNode;
  /** Full-width block button. */
  fullWidth?: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const variantClasses: Record<ButtonVariant, string> = {
  primary: [
    'bg-[#2D6A4F] text-[#FAFAF7]',
    'border border-transparent',
    'hover:bg-[#255840] active:bg-[#1D4632]',
    'focus-visible:ring-2 focus-visible:ring-[#2D6A4F] focus-visible:ring-offset-2',
    'disabled:bg-[#9FCFAF] disabled:cursor-not-allowed',
  ].join(' '),

  secondary: [
    'bg-transparent text-[#2D6A4F]',
    'border border-[#2D6A4F]',
    'hover:bg-[#EAF4EE] active:bg-[#C5E2CF]',
    'focus-visible:ring-2 focus-visible:ring-[#2D6A4F] focus-visible:ring-offset-2',
    'disabled:border-[#9FCFAF] disabled:text-[#9FCFAF] disabled:cursor-not-allowed',
  ].join(' '),

  ghost: [
    'bg-transparent text-[#2D6A4F]',
    'border border-transparent',
    'hover:bg-[#EAF4EE] active:bg-[#C5E2CF]',
    'focus-visible:ring-2 focus-visible:ring-[#2D6A4F] focus-visible:ring-offset-2',
    'disabled:text-[#9FCFAF] disabled:cursor-not-allowed',
  ].join(' '),

  danger: [
    'bg-[#DC2626] text-white',
    'border border-transparent',
    'hover:bg-[#B91C1C] active:bg-[#991B1B]',
    'focus-visible:ring-2 focus-visible:ring-[#DC2626] focus-visible:ring-offset-2',
    'disabled:bg-[#FCA5A5] disabled:cursor-not-allowed',
  ].join(' '),
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm gap-1.5 rounded-md',
  md: 'px-4 py-2   text-sm gap-2   rounded-lg',
  lg: 'px-6 py-3   text-base gap-2.5 rounded-xl',
};

// ─────────────────────────────────────────────────────────────────────────────
// Loading spinner (inline SVG, brand green)
// ─────────────────────────────────────────────────────────────────────────────

const LoadingSpinner: React.FC<{ size: ButtonSize }> = ({ size }) => {
  const dim = size === 'lg' ? 18 : 16;
  return (
    <svg
      aria-hidden="true"
      width={dim}
      height={dim}
      viewBox="0 0 24 24"
      fill="none"
      className="animate-spin"
    >
      <circle
        cx="12" cy="12" r="10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeDasharray="31.416"
        strokeDashoffset="10"
        opacity="0.3"
      />
      <path
        d="M12 2a10 10 0 0 1 10 10"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Button component.
 *
 * @example
 * <Button variant="primary" size="md" onClick={handleSubmit}>
 *   Save Patient Record
 * </Button>
 *
 * @example
 * <Button variant="ghost" loading>Processing…</Button>
 */
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant   = 'primary',
      size      = 'md',
      loading   = false,
      disabled  = false,
      fullWidth = false,
      leftIcon,
      rightIcon,
      children,
      className,
      ...rest
    },
    ref,
  ) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        disabled={isDisabled}
        aria-disabled={isDisabled}
        aria-busy={loading}
        className={twMerge(
          clsx(
            // Base
            'inline-flex items-center justify-center font-medium',
            'transition-colors duration-150 outline-none select-none',
            'whitespace-nowrap leading-none',
            // Variant & size
            variantClasses[variant],
            sizeClasses[size],
            // Full width
            fullWidth && 'w-full',
            // Caller overrides
            className,
          ),
        )}
        {...rest}
      >
        {loading ? (
          <LoadingSpinner size={size} />
        ) : (
          leftIcon && <span className="shrink-0">{leftIcon}</span>
        )}

        {children && (
          <span className={clsx(loading && 'opacity-0 absolute')}>{children}</span>
        )}

        {!loading && rightIcon && (
          <span className="shrink-0">{rightIcon}</span>
        )}
      </button>
    );
  },
);

Button.displayName = 'Button';

export default Button;
