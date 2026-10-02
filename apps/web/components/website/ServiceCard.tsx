import React from "react";
import Link from "next/link";
import { ServiceItem } from "@/lib/data/types";

interface ServiceCardProps {
  service: ServiceItem;
}

export function ServiceCard({ service }: ServiceCardProps) {
  return (
    <div className="group rounded-2xl bg-[#0D1527] border border-[#1E293B] hover:border-[#0D9488]/50 p-6 sm:p-8 flex flex-col justify-between transition-all duration-200 hover:shadow-xl hover:shadow-[#0D9488]/5">
      <div>
        <div className="flex items-center justify-between mb-4">
          <span className="text-3xl p-3 rounded-xl bg-white/5 border border-[#334155] group-hover:scale-105 transition-transform">
            {service.icon}
          </span>
          {service.badge && (
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-[#0F766E]/20 text-[#5EEAD4] border border-[#0D9488]/30">
              {service.badge}
            </span>
          )}
        </div>

        <h3 className="text-xl font-bold text-white group-hover:text-[#5EEAD4] transition">
          {service.name}
        </h3>

        <p className="mt-3 text-sm text-[#94A3B8] leading-relaxed">
          {service.shortDescription}
        </p>

        <div className="mt-5 space-y-2">
          <p className="text-xs font-bold uppercase tracking-wider text-[#64748B]">Core Capabilities</p>
          <ul className="space-y-1.5">
            {service.capabilities.slice(0, 3).map((cap, idx) => (
              <li key={idx} className="text-xs text-[#CBD5E1] flex items-start gap-2">
                <span className="text-[#10B981] font-bold">✓</span>
                <span>{cap}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-8 pt-4 border-t border-[#1E293B] flex items-center justify-between">
        <Link
          href={`/services/${service.slug}`}
          className="text-sm font-semibold text-[#5EEAD4] group-hover:text-white flex items-center gap-1 transition"
        >
          <span>Explore Service</span>
          <span className="group-hover:translate-x-1 transition-transform">→</span>
        </Link>
      </div>
    </div>
  );
}
