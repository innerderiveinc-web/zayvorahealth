import React from 'react';

export interface TimelineEvent {
  id: string;
  timestamp: string;
  title: string;
  description?: string;
  badge?: string;
  author?: string;
}

export interface TimelineProps {
  events: TimelineEvent[];
  className?: string;
}

export const Timeline: React.FC<TimelineProps> = ({ events, className = '' }) => {
  return (
    <div className={`relative pl-6 border-l-2 border-brand-primary/30 dark:border-emerald-500/30 space-y-6 ${className}`}>
      {events.map((evt) => (
        <div key={evt.id} className="relative group">
          <div className="absolute -left-[31px] top-1.5 w-3.5 h-3.5 rounded-full bg-brand-primary ring-4 ring-white dark:ring-slate-900" />
          <div className="flex items-center justify-between gap-2">
            <h4 className="font-semibold text-sm text-gray-900 dark:text-gray-100">{evt.title}</h4>
            <time className="text-xs text-gray-500 dark:text-gray-400">{evt.timestamp}</time>
          </div>
          {evt.description && (
            <p className="mt-1 text-xs text-gray-600 dark:text-gray-300">{evt.description}</p>
          )}
          {evt.author && (
            <p className="mt-1 text-[11px] text-gray-400">By {evt.author}</p>
          )}
        </div>
      ))}
    </div>
  );
};
