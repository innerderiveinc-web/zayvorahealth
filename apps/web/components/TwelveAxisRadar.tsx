"use client";

import React from "react";

export interface AxisDefinition {
  id: string;
  name: string;
  shortName: string;
  system: string;
}

export const TWELVE_AXES: AxisDefinition[] = [
  { id: "jigar-banas", name: "Jigar–Banas", shortName: "Hepatic", system: "Hepato-Metabolic" },
  { id: "dimagh-aasab", name: "Dimagh–Aasab", shortName: "Neuro", system: "Neuro-Psychological" },
  { id: "qalb-uroq", name: "Qalb–Urooq", shortName: "Cardio", system: "Cardio-Vascular" },
  { id: "riya-sadr", name: "Riya–Sadr", shortName: "Pulmonary", system: "Broncho-Pulmonary" },
  { id: "meda-amaa", name: "Meda–Amaa", shortName: "GI / Mida", system: "Gastro-Intestinal" },
  { id: "ghudad-hazm", name: "Kulyatain", shortName: "Renal", system: "Nephro-Urological" },
  { id: "khusyatain", name: "Khusyatain", shortName: "Male Repro", system: "Male Reproductive" },
  { id: "reham-mabaysim", name: "Rahim", shortName: "Female Repro", system: "Female Reproductive" },
  { id: "mafasil", name: "Mafasil", shortName: "Joints", system: "Musculo-Skeletal" },
  { id: "shaar-jigar", name: "Jild", shortName: "Skin / Barrier", system: "Dermato-Immunological" },
  { id: "ghudda-mithana", name: "Tihal", shortName: "Splenic", system: "Spleno-Cerebral" },
  { id: "tabiyat", name: "Hifz-e-Sehat", shortName: "Tabiyat", system: "Vital Resilience" },
];

interface TwelveAxisRadarProps {
  activeAxes?: string[];
  axisScores?: Record<string, number>; // 0 to 5
  onAxisClick?: (axisId: string) => void;
  size?: number;
  className?: string;
}

export function TwelveAxisRadar({
  activeAxes = [],
  axisScores = {},
  onAxisClick,
  size = 320,
  className = "",
}: TwelveAxisRadarProps) {
  const center = size / 2;
  const radius = center * 0.72;
  const totalAxes = TWELVE_AXES.length;
  const angleStep = (Math.PI * 2) / totalAxes;

  // Compute coordinates at a given distance ratio (0.0 to 1.0)
  const getCoordinates = (index: number, ratio: number) => {
    const angle = index * angleStep - Math.PI / 2;
    return {
      x: center + radius * ratio * Math.cos(angle),
      y: center + radius * ratio * Math.sin(angle),
    };
  };

  // Concentric grid polygons (5 levels: 0.2, 0.4, 0.6, 0.8, 1.0)
  const gridLevels = [0.2, 0.4, 0.6, 0.8, 1.0];
  const gridPolygons = gridLevels.map((lvl) => {
    return TWELVE_AXES.map((_, i) => {
      const { x, y } = getCoordinates(i, lvl);
      return `${x},${y}`;
    }).join(" ");
  });

  // Calculate polygon for active axes / scores
  const scorePolygon = TWELVE_AXES.map((axis, i) => {
    const isExplicitlyActive = activeAxes.includes(axis.id);
    const score = axisScores[axis.id] ?? (isExplicitlyActive ? 4.5 : 1.0);
    const ratio = Math.max(0.15, Math.min(1.0, score / 5.0));
    const { x, y } = getCoordinates(i, ratio);
    return `${x},${y}`;
  }).join(" ");

  return (
    <div className={`flex flex-col items-center select-none ${className}`}>
      <div className="relative">
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="overflow-visible"
        >
          {/* Background Concentric Grid Polygons */}
          {gridPolygons.map((points, idx) => (
            <polygon
              key={`grid-${idx}`}
              points={points}
              fill="none"
              stroke="#24302a"
              strokeWidth={idx === gridPolygons.length - 1 ? 1.5 : 0.75}
              strokeDasharray={idx === gridPolygons.length - 1 ? "none" : "3,3"}
              className="opacity-70"
            />
          ))}

          {/* Radial Spokes from Center */}
          {TWELVE_AXES.map((axis, i) => {
            const { x, y } = getCoordinates(i, 1.0);
            const isActive = activeAxes.includes(axis.id);
            return (
              <line
                key={`spoke-${axis.id}`}
                x1={center}
                y1={center}
                x2={x}
                y2={y}
                stroke={isActive ? "#2ea87f" : "#24302a"}
                strokeWidth={isActive ? 1.5 : 0.8}
                className="transition-colors duration-300"
              />
            );
          })}

          {/* Active Value Area Polygon */}
          <polygon
            points={scorePolygon}
            fill="rgba(46, 168, 127, 0.25)"
            stroke="#2ea87f"
            strokeWidth={2}
            className="transition-all duration-500 ease-out"
          />

          {/* Data Points on the Polygon */}
          {TWELVE_AXES.map((axis, i) => {
            const isExplicitlyActive = activeAxes.includes(axis.id);
            const score = axisScores[axis.id] ?? (isExplicitlyActive ? 4.5 : 1.0);
            const ratio = Math.max(0.15, Math.min(1.0, score / 5.0));
            const { x, y } = getCoordinates(i, ratio);
            return (
              <circle
                key={`pt-${axis.id}`}
                cx={x}
                cy={y}
                r={isExplicitlyActive ? 4.5 : 2.5}
                fill={isExplicitlyActive ? "#c9a24b" : "#2ea87f"}
                stroke="#121712"
                strokeWidth={1.5}
                className="transition-all duration-300"
              />
            );
          })}

          {/* Perimeter Labels */}
          {TWELVE_AXES.map((axis, i) => {
            const { x, y } = getCoordinates(i, 1.18);
            const isActive = activeAxes.includes(axis.id);
            return (
              <g
                key={`lbl-${axis.id}`}
                className="cursor-pointer group"
                onClick={() => onAxisClick?.(axis.id)}
              >
                <text
                  x={x}
                  y={y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  className={`text-[9px] font-mono transition-colors duration-200 ${
                    isActive
                      ? "fill-[#c9a24b] font-bold"
                      : "fill-[#8a9490] hover:fill-[#ece8dd]"
                  }`}
                >
                  {axis.shortName}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Mini Legend */}
      <div className="flex items-center gap-4 mt-2 text-[10px] text-[#8a9490]">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-[#c9a24b]" />
          Targeted Axis ({activeAxes.length})
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-0.5 bg-[#2ea87f]" />
          12-Axis Humoral Equilibrium
        </span>
      </div>
    </div>
  );
}
