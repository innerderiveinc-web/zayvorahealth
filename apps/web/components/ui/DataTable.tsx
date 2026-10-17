/**
 * @file DataTable.tsx
 * @description Generic sortable, accessible data table component.
 * Supports column definitions with optional sort, custom cell renderers,
 * and an empty-state slot.
 */
"use client";

import React, { useState, useMemo } from "react";

export interface ColumnDef<TRow> {
  /** Unique key matching a property of TRow (or a synthetic key for custom cells) */
  key: string;
  /** Column header label */
  header: string;
  /** Whether this column is sortable */
  sortable?: boolean;
  /** Custom cell renderer – receives the row object */
  cell?: (row: TRow) => React.ReactNode;
  /** Tailwind class applied to <td> */
  className?: string;
}

interface DataTableProps<TRow extends Record<string, unknown>> {
  /** Column definitions */
  columns: ColumnDef<TRow>[];
  /** Row data */
  data: TRow[];
  /** Unique key extractor per row */
  rowKey: (row: TRow) => string;
  /** Optional node shown when data is empty */
  emptyState?: React.ReactNode;
  /** Additional wrapper class */
  className?: string;
}

type SortDir = "asc" | "desc";

/**
 * DataTable – generic sortable table with ZAYVORA dark-mode styling.
 */
export function DataTable<TRow extends Record<string, unknown>>({
  columns,
  data,
  rowKey,
  emptyState,
  className = "",
}: DataTableProps<TRow>) {
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  const sorted = useMemo(() => {
    if (!sortKey) return data;
    return [...data].sort((a, b) => {
      const av = a[sortKey];
      const bv = b[sortKey];
      const cmp =
        typeof av === "number" && typeof bv === "number"
          ? av - bv
          : String(av ?? "").localeCompare(String(bv ?? ""));
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [data, sortKey, sortDir]);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  return (
    <div className={`overflow-x-auto rounded-xl border border-[#334155] ${className}`}>
      <table className="min-w-full text-xs text-slate-300">
        {/* Header */}
        <thead className="bg-[#0f172a] border-b border-[#334155]">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                scope="col"
                className={`px-4 py-3 text-left font-semibold text-slate-400 uppercase tracking-wider whitespace-nowrap select-none ${
                  col.sortable
                    ? "cursor-pointer hover:text-white transition-colors"
                    : ""
                } ${col.className ?? ""}`}
                onClick={col.sortable ? () => handleSort(col.key) : undefined}
                aria-sort={
                  sortKey === col.key
                    ? sortDir === "asc"
                      ? "ascending"
                      : "descending"
                    : undefined
                }
              >
                <span className="flex items-center gap-1">
                  {col.header}
                  {col.sortable && (
                    <span className="text-[10px] text-slate-600">
                      {sortKey === col.key
                        ? sortDir === "asc"
                          ? "↑"
                          : "↓"
                        : "⇅"}
                    </span>
                  )}
                </span>
              </th>
            ))}
          </tr>
        </thead>

        {/* Body */}
        <tbody className="divide-y divide-[#1e293b]">
          {sorted.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length}
                className="px-4 py-8 text-center text-slate-500"
              >
                {emptyState ?? "No records found."}
              </td>
            </tr>
          ) : (
            sorted.map((row) => (
              <tr
                key={rowKey(row)}
                className="hover:bg-[#1e293b]/60 transition-colors"
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`px-4 py-3 whitespace-nowrap ${col.className ?? ""}`}
                  >
                    {col.cell
                      ? col.cell(row)
                      : String(row[col.key] ?? "—")}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
