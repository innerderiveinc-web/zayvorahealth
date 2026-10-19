import React from 'react';

export interface StepItem {
  id: string;
  title: string;
  description?: string;
}

export interface StepperProps {
  steps: StepItem[];
  currentStepIndex: number;
  className?: string;
  onStepClick?: (index: number) => void;
}

export const Stepper: React.FC<StepperProps> = ({
  steps,
  currentStepIndex,
  className = '',
  onStepClick,
}) => {
  return (
    <div className={`w-full ${className}`}>
      <ol className="flex items-center w-full">
        {steps.map((step, idx) => {
          const isCompleted = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <li
              key={step.id}
              className={`flex items-center ${idx < steps.length - 1 ? 'w-full' : ''}`}
            >
              <button
                type="button"
                disabled={!onStepClick}
                onClick={() => onStepClick && onStepClick(idx)}
                className={`flex items-center text-left ${onStepClick ? 'cursor-pointer' : 'cursor-default'}`}
              >
                <span
                  className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs transition-colors ${
                    isCompleted
                      ? 'bg-brand-primary text-white dark:bg-emerald-600'
                      : isCurrent
                      ? 'bg-brand-accent text-gray-900 ring-2 ring-brand-primary'
                      : 'bg-gray-200 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                  }`}
                >
                  {isCompleted ? '✓' : idx + 1}
                </span>
                <div className="ml-3 hidden sm:block">
                  <p
                    className={`text-xs font-semibold ${
                      isCurrent ? 'text-brand-primary dark:text-emerald-400' : 'text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    {step.title}
                  </p>
                  {step.description && (
                    <p className="text-[10px] text-gray-400">{step.description}</p>
                  )}
                </div>
              </button>

              {idx < steps.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-4 ${
                    isCompleted ? 'bg-brand-primary dark:bg-emerald-600' : 'bg-gray-200 dark:bg-gray-800'
                  }`}
                />
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
};
