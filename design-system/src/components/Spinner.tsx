/**
 * Spinner — ZAYVORA Design System
 *
 * Accessible loading indicator in brand colours.
 * Renders an SVG spinner with an aria-label for screen readers.
 *
 * @module design-system/Spinner
 */

import React, { SVGAttributes } from 'react';
import { clsx } from 'clsx';

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

export type SpinnerSize    = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type SpinnerVariant = 'primary' | 'secondary' | 'accent' | 'white' | 'current';

export interface SpinnerProps extends SVGAttributes<SVGSVGElement> {
  /** Size preset. Defaults to "md". */
  size?: SpinnerSize;
  /** Colour variant. Defaults to "primary". */
  variant?: SpinnerVariant;
  /** Accessible label for screen readers. Defaults to "Loading…". */
  label?: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// Style maps
// ─────────────────────────────────────────────────────────────────────────────

const sizeMap: Record<SpinnerSize, number> = {
  xs: 14,
  sm: 18,
  md: 24,
  lg: 36,
  xl: 48,
};

const strokeMap: Record<SpinnerSize, number> = {
  xs: 2.5,
  sm: 2.5,
  md: 3,
  lg: 3,
  xl: 3.5,
};

const colourMap: Record<SpinnerVariant, string> = {
  primary:   'text-[#2D6A4F]',
  secondary: 'text-[#1B4332]',
  accent:    'text-[#F4A261]',
  white:     'text-white',
  current:   'text-current',
};

// ─────────────────────────────────────────────────────────────────────────────
// Component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Spinner component.
 *
 * @example
 * <Spinner />
 * <Spinner size="lg" variant="accent" label="Saving record…" />
 */
export const Spinner: React.FC<SpinnerProps> = ({
  size    = 'md',
  variant = 'primary',
  label   = 'Loading…',
  className,
  ...rest
}) => {
  const dim    = sizeMap[size];
  const stroke = strokeMap[size];
  const r      = (dim - stroke * 2) / 2;
  const cx     = dim / 2;
  const circ   = 2 * Math.PI * r;

  return (
    <svg
      role="status"
      aria-label={label}
      width={dim}
      height={dim}
      viewBox={`0 0 ${dim} ${dim}`}
      fill="none"
      className={clsx('animate-spin', colourMap[variant], className)}
      {...rest}
    >
      {/* Track */}
      <circle
        cx={cx}
        cy={cx}
        r={r}
        stroke="currentColor"
        strokeWidth={stroke}
        strokeOpacity={0.2}
      />
      {/* Arc */}
      <circle
        cx={cx}
        cy={cx}
        r={r}
        stroke="currentColor"
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={circ}
        strokeDashoffset={circ * 0.75}
        transform={`rotate(-90 ${cx} ${cx})`}
      />
    </svg>
  );
};

Spinner.displayName = 'Spinner';

export default Spinner;
