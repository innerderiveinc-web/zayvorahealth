/**
 * @file LoadingSpinner.tsx
 * @description Centered loading spinner using ZAYVORA brand green.
 */
import React from "react";

interface LoadingSpinnerProps {
  /** Size in rem */
  size?: "sm" | "md" | "lg";
  /** Optional message below the spinner */
  message?: string;
  /** Whether to fill the full viewport height */
  fullScreen?: boolean;
}

const SIZE_MAP = {
  sm: "w-5 h-5 border-2",
  md: "w-8 h-8 border-2",
  lg: "w-12 h-12 border-[3px]",
};

/**
 * LoadingSpinner – centred spinner with optional label.
 */
export function LoadingSpinner({
  size = "md",
  message,
  fullScreen = false,
}: LoadingSpinnerProps) {
  return (
    <div
      role="status"
      aria-label={message ?? "Loading…"}
      className={`flex flex-col items-center justify-center gap-3 ${
        fullScreen ? "min-h-screen" : "py-16"
      }`}
    >
      <span
        className={`${SIZE_MAP[size]} rounded-full border-[#2D6A4F]/30 border-t-[#2D6A4F] animate-spin`}
        style={{ borderTopColor: "#2D6A4F" }}
      />
      {message && (
        <p className="text-xs text-slate-400 animate-pulse">{message}</p>
      )}
    </div>
  );
}
