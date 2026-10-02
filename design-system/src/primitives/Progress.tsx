import React from 'react';
import { twMerge } from 'tailwind-merge';

export type ProgressVariant = 'primary' | 'success' | 'warning' | 'danger';
export type ProgressSize = 'sm' | 'md' | 'lg';

export interface ProgressProps {
  value: number;
  max?: number;
  variant?: ProgressVariant;
  size?: ProgressSize;
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  max = 100,
  variant = 'primary',
  size = 'md',
  showLabel = false,
  label,
  className = '',
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const variantColors: Record<ProgressVariant, string> = {
    primary: 'bg-[#2D6A4F]',
    success: 'bg-emerald-600',
    warning: 'bg-amber-500',
    danger: 'bg-rose-600',
  };

  const heightClasses: Record<ProgressSize, string> = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4',
  };

  return (
    <div className={twMerge('w-full', className)}>
      {(showLabel || label) && (
        <div className="flex items-center justify-between text-xs font-medium text-stone-700 dark:text-stone-300 mb-1">
          <span>{label || 'Progress'}</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        className={twMerge('w-full bg-stone-200 dark:bg-stone-800 rounded-full overflow-hidden', heightClasses[size])}
      >
        <div
          className={twMerge('h-full transition-all duration-300 rounded-full', variantColors[variant])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
