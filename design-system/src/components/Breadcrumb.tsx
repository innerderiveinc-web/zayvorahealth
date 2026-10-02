import React from 'react';

export interface BreadcrumbItem {
  label: string;
  href?: string;
  isCurrent?: boolean;
}

export interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({ items, className = '' }) => {
  return (
    <nav aria-label="Breadcrumb" className={`flex items-center text-sm ${className}`}>
      <ol className="flex items-center space-x-2">
        {items.map((item, idx) => (
          <li key={idx} className="flex items-center">
            {idx > 0 && <span className="mx-2 text-gray-400 select-none">/</span>}
            {item.isCurrent || !item.href ? (
              <span className="font-semibold text-brand-primary dark:text-emerald-400" aria-current="page">
                {item.label}
              </span>
            ) : (
              <a
                href={item.href}
                className="text-gray-500 hover:text-brand-primary dark:text-gray-400 dark:hover:text-emerald-300 transition-colors"
              >
                {item.label}
              </a>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};
