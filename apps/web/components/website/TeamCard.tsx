import React from "react";
import { TeamMember } from "@/lib/data/types";

interface TeamCardProps {
  member: TeamMember;
}

export function TeamCard({ member }: TeamCardProps) {
  return (
    <div className="rounded-2xl bg-[#0D1527] border border-[#1E293B] hover:border-[#0D9488]/40 p-6 flex flex-col justify-between transition-all duration-200">
      <div>
        <div className="flex items-start justify-between gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-[#0D9488] to-[#2D6A4F] flex items-center justify-center text-xl font-bold text-white shadow-md">
            {member.name.split(" ").map(n => n[0]).slice(0, 2).join("")}
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-[#1E293B] text-[#94A3B8] border border-[#334155]">
            {member.division}
          </span>
        </div>

        <h3 className="mt-4 text-lg font-bold text-white">
          {member.name}
        </h3>
        
        <p className="text-xs font-semibold text-[#5EEAD4] mt-0.5">
          {member.role}
        </p>

        <p className="text-xs text-[#64748B] mt-0.5 font-medium">
          {member.degrees} • {member.experience}
        </p>

        <p className="mt-3 text-xs sm:text-sm text-[#94A3B8] leading-relaxed">
          {member.bio}
        </p>
      </div>

      <div className="mt-5 pt-4 border-t border-[#1E293B]">
        <p className="text-[11px] font-bold uppercase tracking-wider text-[#64748B] mb-2">Areas of Focus</p>
        <div className="flex flex-wrap gap-1.5">
          {member.specialization.map((spec, idx) => (
            <span
              key={idx}
              className="text-[11px] px-2 py-0.5 rounded-md bg-[#0A0F1D] text-[#CBD5E1] border border-[#1E293B]"
            >
              {spec}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
