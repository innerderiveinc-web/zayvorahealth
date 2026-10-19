import React, { useState, useRef } from 'react';
import { twMerge } from 'tailwind-merge';

export type TooltipPlacement = 'top' | 'bottom' | 'left' | 'right';

export interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactNode;
  placement?: TooltipPlacement;
  delayMs?: number;
  className?: string;
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  children,
  placement = 'top',
  delayMs = 150,
  className = '',
}) => {
  const [visible, setVisible] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const handleMouseEnter = () => {
    timeoutRef.current = setTimeout(() => {
      setVisible(true);
    }, delayMs);
  };

  const handleMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  }[placement];

  return (
    <div
      className="relative inline-flex items-center"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleMouseEnter}
      onBlur={handleMouseLeave}
    >
      {children}
      {visible && content && (
        <div
          role="tooltip"
          className={twMerge(
            'absolute z-50 px-2.5 py-1 text-xs font-medium text-white bg-stone-900 rounded shadow-md whitespace-nowrap pointer-events-none transition-opacity duration-150',
            positionClasses,
            className
          )}
        >
          {content}
        </div>
      )}
    </div>
  );
};
