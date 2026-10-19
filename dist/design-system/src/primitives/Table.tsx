import React from 'react';
import { twMerge } from 'tailwind-merge';

export interface Column<T> {
  key: string;
  header: React.ReactNode;
  render?: (item: T, index: number) => React.ReactNode;
  width?: string;
  align?: 'left' | 'center' | 'right';
  sortable?: boolean;
}

export interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T, index: number) => string | number;
  emptyMessage?: string;
  striped?: boolean;
  hoverable?: boolean;
  sortColumn?: string;
  sortDirection?: 'asc' | 'desc';
  onSort?: (columnKey: string) => void;
  className?: string;
}

export function Table<T>({
  columns,
  data,
  keyExtractor,
  emptyMessage = 'No clinical records found.',
  striped = false,
  hoverable = true,
  sortColumn,
  sortDirection,
  onSort,
  className = '',
}: TableProps<T>) {
  return (
    <div className={twMerge('w-full overflow-x-auto rounded-lg border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900', className)}>
      <table className="w-full text-left text-xs text-stone-700 dark:text-stone-300">
        <thead className="bg-stone-50 dark:bg-stone-950 border-b border-stone-200 dark:border-stone-800 text-[11px] font-semibold text-stone-600 dark:text-stone-400 uppercase tracking-wider">
          <tr>
            {columns.map((col) => {
              const alignClass = col.align === 'center' ? 'text-center' : col.align === 'right' ? 'text-right' : 'text-left';
              return (
                <th
                  key={col.key}
                  style={{ width: col.width }}
                  className={twMerge('px-4 py-3', alignClass, col.sortable ? 'cursor-pointer select-none hover:text-stone-900 dark:hover:text-stone-100' : '')}
                  onClick={() => col.sortable && onSort?.(col.key)}
                >
                  <div className={twMerge('inline-flex items-center gap-1', col.align === 'right' ? 'justify-end' : col.align === 'center' ? 'justify-center' : 'justify-start')}>
                    <span>{col.header}</span>
                    {col.sortable && (
                      <span className="text-stone-400">
                        {sortColumn === col.key ? (
                          sortDirection === 'asc' ? '▲' : '▼'
                        ) : (
                          '⇅'
                        )}
                      </span>
                    )}
                  </div>
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody className="divide-y divide-stone-200 dark:divide-stone-800">
          {data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                className="px-4 py-8 text-center text-stone-400 dark:text-stone-500 italic"
              >
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((item, index) => (
              <tr
                key={keyExtractor(item, index)}
                className={twMerge(
                  'transition-colors',
                  striped && index % 2 === 1 ? 'bg-stone-50/50 dark:bg-stone-950/20' : '',
                  hoverable ? 'hover:bg-stone-50 dark:hover:bg-stone-800/50' : ''
                )}
              >
                {columns.map((col) => {
                  const alignClass = col.align === 'center' ? 'text-center' : col.align === 'right' ? 'text-right' : 'text-left';
                  const val = (item as Record<string, unknown>)[col.key];
                  return (
                    <td key={col.key} className={twMerge('px-4 py-3', alignClass)}>
                      {col.render ? col.render(item, index) : String(val ?? '')}
                    </td>
                  );
                })}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
