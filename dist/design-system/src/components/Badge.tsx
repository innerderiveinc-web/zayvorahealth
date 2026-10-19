/**
 * Badge — ZAYVORA Design System
 *
 * Compact status labels for conveying state at a glance.
 * Supports success, warning, error, info, and neutral variants.
 *
 * @module design-system/Badge
 */

import React, { HTMLAttributes } from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type BadgeVariant = 'success' | 'warning' | 'error' | 'info' | 'neutral';
export type BadgeSize    = 'sm' | 'md';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  /** Semantic colour variant. Defaults to "neutral". */
  variant?: BadgeVariant;
  /** Size preset. Defaults to "md". */
  size?: BadgeSize;
  /** Optional dot indicator shown before the label. */
  dot?: boolean;
  /** Pill (fully-rounded) shape. Defaults to true. */
  pill?: boolean;
}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const variantClasses: Record<BadgeVariant, { badge: string; dot: string }> = {
  success: {
    badge: 'bg-[#EAF4EE] text-[#1D4632] ring-1 ring-inset ring-[#2D6A4F]/20',
    dot:   'bg-[#2D6A4F]',
  },
  warning: {
    badge: 'bg-[#FEF3C7] text-[#92400E] ring-1 ring-inset ring-[#D97706]/20',
    dot:   'bg-[#D97706]',
  },
  error: {
    badge: 'bg-[#FEE2E2] text-[#991B1B] ring-1 ring-inset ring-[#DC2626]/20',
    dot:   'bg-[#DC2626]',
  },
  info: {
    badge: 'bg-[#DBEAFE] text-[#1E3A8A] ring-1 ring-inset ring-[#2563EB]/20',
    dot:   'bg-[#2563EB]',
  },
  neutral: {
    badge: 'bg-[#F3F4F6] text-[#374151] ring-1 ring-inset ring-[#6B7280]/20',
    dot:   'bg-[#6B7280]',
  },
};

const sizeClasses: Record<BadgeSize, string> = {
  sm: 'px-1.5 py-0.5 text-xs gap-1',
  md: 'px-2.5 py-1   text-xs gap-1.5',
};

const dotSizeClasses: Record<BadgeSize, string> = {
  sm: 'h-1.5 w-1.5',
  md: 'h-2   w-2',
};

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Badge component.
 *
 * @example
 * <Badge variant="success" dot>Active</Badge>
 * <Badge variant="error">Critical</Badge>
 * <Badge variant="warning" size="sm">Pending</Badge>
 */
export const Badge: React.FC<BadgeProps> = ({
  variant = 'neutral',
  size    = 'md',
  dot     = false,
  pill    = true,
  children,
  className,
  ...rest
}) => {
  const styles = variantClasses[variant];

  return (
    <span
      className={twMerge(
        clsx(
          'inline-flex items-center font-medium leading-none',
          pill ? 'rounded-full' : 'rounded-md',
          styles.badge,
          sizeClasses[size],
          className,
        ),
      )}
      {...rest}
    >
      {dot && (
        <span
          aria-hidden="true"
          className={clsx(
            'shrink-0 rounded-full',
            dotSizeClasses[size],
            styles.dot,
          )}
        />
      )}
      {children}
    </span>
  );
};

Badge.displayName = 'Badge';

export default Badge;
