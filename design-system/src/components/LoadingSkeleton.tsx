import React from "react";

export interface LoadingSkeletonProps {
  className?: string;
  count?: number;
  height?: string;
  circle?: boolean;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  className = "",
  count = 1,
  height = "h-4",
  circle = false,
}) => {
  const items = Array.from({ length: count });

  return (
    <div className="space-y-2.5 w-full">
      {items.map((_, i) => (
        <div
          key={i}
          className={`animate-pulse bg-slate-800/60 ${
            circle ? "rounded-full aspect-square" : "rounded-lg"
          } ${height} ${className}`}
        />
      ))}
    </div>
  );
};
