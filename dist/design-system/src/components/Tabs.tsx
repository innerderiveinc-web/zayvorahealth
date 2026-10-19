import React from "react";

export interface TabItem {
  id: string;
  label: string;
  badge?: string | number;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (id: string) => void;
  className?: string;
  variant?: "pills" | "underline";
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  activeTab,
  onChange,
  className = "",
  variant = "underline",
}) => {
  return (
    <div
      role="tablist"
      className={`flex items-center gap-2 overflow-x-auto no-scrollbar ${
        variant === "underline" ? "border-b border-slate-800" : ""
      } ${className}`}
    >
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        if (variant === "pills") {
          return (
            <button
              key={tab.id}
              role="tab"
              aria-selected={isActive}
              aria-controls={`panel-${tab.id}`}
              disabled={tab.disabled}
              onClick={() => !tab.disabled && onChange(tab.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition whitespace-nowrap ${
                isActive
                  ? "bg-[#2D6A4F] text-white shadow-sm"
                  : "bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              } ${tab.disabled ? "opacity-40 cursor-not-allowed" : ""}`}
            >
              {tab.icon && <span>{tab.icon}</span>}
              <span>{tab.label}</span>
              {tab.badge !== undefined && (
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold ${
                    isActive ? "bg-white/20 text-white" : "bg-slate-800 text-slate-300"
                  }`}
                >
                  {tab.badge}
                </span>
              )}
            </button>
          );
        }

        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            aria-controls={`panel-${tab.id}`}
            disabled={tab.disabled}
            onClick={() => !tab.disabled && onChange(tab.id)}
            className={`pb-3 px-3 text-xs font-semibold flex items-center gap-2 transition relative whitespace-nowrap ${
              isActive ? "text-[#53A96E]" : "text-slate-400 hover:text-slate-200"
            } ${tab.disabled ? "opacity-40 cursor-not-allowed" : ""}`}
          >
            {tab.icon && <span>{tab.icon}</span>}
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold">
                {tab.badge}
              </span>
            )}
            {isActive && (
              <span className="absolute bottom-0 inset-x-0 h-0.5 bg-[#2D6A4F] rounded-full" />
            )}
          </button>
        );
      })}
    </div>
  );
};
