import React, { forwardRef } from 'react';
import { twMerge } from 'tailwind-merge';

export interface SearchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  shortcut?: string;
  onClear?: () => void;
  className?: string;
}

export const Search = forwardRef<HTMLInputElement, SearchProps>(({
  size = 'md',
  loading = false,
  shortcut,
  onClear,
  value,
  onChange,
  disabled,
  placeholder = 'Search clinical records, substances, or actions...',
  className = '',
  ...props
}, ref) => {
  const sizeClass = {
    sm: 'py-1.5 pl-8 pr-8 text-xs',
    md: 'py-2 pl-9 pr-9 text-sm',
    lg: 'py-2.5 pl-11 pr-11 text-base',
  }[size];

  const iconSizeClass = {
    sm: 'w-3.5 h-3.5 left-2.5',
    md: 'w-4 h-4 left-3',
    lg: 'w-5 h-5 left-3.5',
  }[size];

  const hasValue = value !== undefined && value !== null && String(value).length > 0;

  return (
    <div className={twMerge('relative flex items-center w-full', className)}>
      <span className={twMerge('absolute pointer-events-none text-stone-400 dark:text-stone-500', iconSizeClass)}>
        {loading ? (
          <svg className="animate-spin" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
        ) : (
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        )}
      </span>

      <input
        ref={ref}
        type="search"
        value={value}
        onChange={onChange}
        disabled={disabled}
        placeholder={placeholder}
        className={twMerge(
          'w-full bg-white dark:bg-stone-900 text-stone-900 dark:text-stone-100 placeholder-stone-400 dark:placeholder-stone-500',
          'border border-stone-300 dark:border-stone-700 rounded-lg transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-[#2D6A4F] focus:border-[#2D6A4F]',
          'disabled:bg-stone-100 dark:disabled:bg-stone-800 disabled:cursor-not-allowed',
          sizeClass
        )}
        {...props}
      />

      <div className="absolute right-2.5 flex items-center gap-1">
        {hasValue && onClear && !disabled && (
          <button
            type="button"
            onClick={onClear}
            aria-label="Clear search"
            className="p-0.5 text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 rounded"
          >
            <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
        {shortcut && !hasValue && (
          <kbd className="hidden sm:inline-flex items-center px-1.5 py-0.5 text-[10px] font-mono font-medium text-stone-400 bg-stone-100 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 rounded">
            {shortcut}
          </kbd>
        )}
      </div>
    </div>
  );
});

Search.displayName = 'Search';
