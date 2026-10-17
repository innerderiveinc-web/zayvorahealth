"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { INSTITUTIONAL_HEADER_NAVIGATION, NavSubItem } from "@/lib/cms/website/navigationData";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { AuthService } from "@/lib/services/authService";
import { saveSession } from "@/lib/session";

export function PublicHeader() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchModalOpen, setSearchModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const dropdownTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Staff & Clinician Modal States
  const [staffModalOpen, setStaffModalOpen] = useState(false);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 15);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchModalOpen(true);
      }
      if (e.key === "Escape") {
        setSearchModalOpen(false);
        setMobileMenuOpen(false);
        setActiveDropdown(null);
        setStaffModalOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  useEffect(() => {
    setMobileMenuOpen(false);
    setActiveDropdown(null);
  }, [pathname]);

  // Clean public visitor search index — only public health, care, and discovery resources
  const searchIndex = [
    { title: "Clinical Care & Matab Consultation", sub: "Individualized Unani Care Plans", href: "/services/clinical-care" },
    { title: "Care Programs", sub: "Metabolic, Digestive, and Joint Programs", href: "/programs" },
    { title: "Health Conditions Directory", sub: "Clinical Overviews & Guidance", href: "/conditions" },
    { title: "Virtual Consultation", sub: "Teleconsultation with Verified Physicians", href: "/teleconsultation" },
    { title: "Specialists & Clinicians", sub: "NCISM-Registered Practitioners", href: "/doctors" },
    { title: "Health Library", sub: "Clinician-Reviewed Health Guidance", href: "/health-library" },
    { title: "Classical Unani Formulations", sub: "Standardized NFUM Formulations", href: "/products/unani-care" },
    { title: "Product Quality & Safety", sub: "Schedule E(1) & GMP Standards", href: "/products/safety" },
    { title: "Clinical Governance & Ethics", sub: "Physician Oversight Principles", href: "/clinical-governance" },
    { title: "Patient Portal (My ZAYVORA™)", sub: "Appointments, Records & Care Plan", href: "/patient" },
    { title: "Book Consultation", sub: "Schedule Outpatient or Virtual Visit", href: "/book" },
  ];

  const filteredResults = searchQuery.trim() === ""
    ? searchIndex.slice(0, 6)
    : searchIndex.filter(i =>
        i.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        i.sub.toLowerCase().includes(searchQuery.toLowerCase())
      );

  const handleMouseEnter = (label: string) => {
    if (dropdownTimeoutRef.current) clearTimeout(dropdownTimeoutRef.current);
    setActiveDropdown(label);
  };

  const handleMouseLeave = () => {
    dropdownTimeoutRef.current = setTimeout(() => {
      setActiveDropdown(null);
    }, 150);
  };

  const handleStaffFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!loginEmail.trim() || !loginPassword) {
      setLoginError("Please provide both email and password.");
      return;
    }
    setLoginLoading(true);
    setLoginError(null);

    try {
      const session = await AuthService.loginAsync(loginEmail.trim(), loginPassword);
      saveSession({
        access_token: session.token,
        token_type: "bearer",
        expires_in: 7200,
        role: session.user.role.toLowerCase(),
        organization_id: session.user.facilityId
      });
      setStaffModalOpen(false);
      const targetPath = session.user.role === "SUPER_ADMIN" ? "/admin" 
        : session.user.role === "PHARMACIST" ? "/pharmacy" 
        : session.user.role === "PATIENT" ? "/patient"
        : "/doctor";
      router.push(targetPath);
    } catch (err: any) {
      setLoginError(err?.message || "Invalid clinician or staff credentials. Please check your email and password.");
    } finally {
      setLoginLoading(false);
    }
  };

  return (
    <>
      <header
        className={`sticky top-0 z-40 transition-all duration-200 ${
          isScrolled
            ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-[#E2E8F0]"
            : "bg-[#FAFAF7] border-b border-[#E2E8F0]"
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
          
          {/* Institutional Brand Identity */}
          <Link href="/" className="flex items-center gap-3 shrink-0 group">
            <div className="w-10 h-10 rounded-2xl bg-[#1B4332] flex items-center justify-center p-2 shadow-sm group-hover:bg-[#2D6A4F] transition-colors">
              <HealthcareIcon name="shield-check" className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-extrabold text-[#1B4332] text-lg tracking-tight block leading-tight">
                ZAYVORA <span className="text-[#2D6A4F] font-semibold text-base">Health™</span>
              </span>
              <span className="text-[10px] text-[#64748B] font-semibold tracking-wider block uppercase">
                Integrative Unani Healthcare OS
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links with Dropdowns (5 Pillars) */}
          <nav className="hidden xl:flex items-center gap-6 text-xs font-semibold text-[#475569]">
            {INSTITUTIONAL_HEADER_NAVIGATION.map((item) => {
              const hasDropdown = Boolean(item.dropdown && item.dropdown.length > 0);
              const isActive = pathname === item.href || (item.dropdown && item.dropdown.some(sub => pathname === sub.href));
              const isOpen = activeDropdown === item.label;

              if (hasDropdown) {
                return (
                  <div
                    key={item.label}
                    className="relative"
                    onMouseEnter={() => handleMouseEnter(item.label)}
                    onMouseLeave={handleMouseLeave}
                  >
                    <Link
                      href={item.href}
                      className={`inline-flex items-center gap-1.5 py-2 transition hover:text-[#1B4332] ${
                        isActive ? "text-[#1B4332] font-bold" : ""
                      }`}
                    >
                      <span>{item.label}</span>
                      <HealthcareIcon
                        name="chevron-down"
                        className={`w-3.5 h-3.5 transition-transform duration-150 ${isOpen ? "rotate-180 text-[#1B4332]" : "text-[#94A3B8]"}`}
                      />
                    </Link>

                    {/* Dropdown Menu Panel */}
                    {isOpen && (
                      <div className="absolute top-full left-0 w-80 pt-2 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                        <div className="rounded-2xl bg-white border border-[#E2E8F0] p-2.5 shadow-xl space-y-1">
                          {item.dropdown?.map((sub) => {
                            const isSubActive = pathname === sub.href;
                            return (
                              <Link
                                key={sub.href}
                                href={sub.href}
                                className={`flex items-start gap-3 p-2.5 rounded-xl transition ${
                                  isSubActive
                                    ? "bg-[#E8F5E9] text-[#1B4332] font-medium"
                                    : "hover:bg-[#F8FAFC] text-[#334155] hover:text-[#0F172A]"
                                }`}
                              >
                                <div className="p-2 rounded-lg bg-[#F1F5F9] text-[#1B4332] shrink-0 mt-0.5">
                                  <HealthcareIcon name={sub.iconKey} className="w-4 h-4" />
                                </div>
                                <div>
                                  <div className="flex items-center gap-1.5">
                                    <span className="text-xs font-bold text-[#0F172A]">{sub.title}</span>
                                    {sub.badge && (
                                      <span className="text-[9px] font-bold px-1.5 py-0.2 rounded bg-[#E8F5E9] text-[#1B4332]">
                                        {sub.badge}
                                      </span>
                                    )}
                                  </div>
                                  <p className="text-[11px] text-[#64748B] line-clamp-1 mt-0.5 leading-snug">
                                    {sub.description}
                                  </p>
                                </div>
                              </Link>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                );
              }

              return (
                <Link
                  key={item.label}
                  href={item.href}
                  className={`py-2 transition hover:text-[#1B4332] ${
                    isActive ? "text-[#1B4332] font-bold" : ""
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          {/* Action CTAs: Search, Staff Portals, Patient Portal, Clinician Sign In, Book Consultation */}
          <div className="flex items-center gap-2 sm:gap-2.5">
            {/* Quick ⌘K Search Trigger */}
            <button
              onClick={() => setSearchModalOpen(true)}
              className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#F8FAFC] border border-[#E2E8F0] hover:border-[#CBD5E1] text-[#64748B] text-xs transition"
              title="Search care and clinical knowledge (⌘K)"
            >
              <HealthcareIcon name="search" className="w-3.5 h-3.5 text-[#94A3B8]" />
              <span>Search...</span>
              <kbd className="text-[10px] font-mono bg-white px-1.5 py-0.5 rounded border border-[#E2E8F0] text-[#64748B]">
                ⌘K
              </kbd>
            </button>

            {/* Patient Portal Link */}
            <Link
              href="/patient"
              className="hidden sm:flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-[#1B4332] hover:bg-[#E8F5E9] transition border border-[#D8F3DC] shadow-xs"
              title="Mareez ke login ke liye (Personal Health Record & Lab Reports)"
            >
              <HealthcareIcon name="user" className="w-3.5 h-3.5 text-[#2D6A4F]" />
              <span>Patient Portal</span>
            </Link>

            {/* Clinician / Staff Sign-in Modal Trigger */}
            <button
              onClick={() => setStaffModalOpen(true)}
              className="hidden sm:flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-slate-800 hover:text-slate-900 hover:bg-slate-100 transition border border-slate-300 shadow-xs"
              title="Doctor, Dispensary & Hospital Staff Gateway"
            >
              <HealthcareIcon name="lock" className="w-3.5 h-3.5 text-emerald-700" />
              <span>Staff / Clinician Gateway</span>
            </button>

            {/* Primary Consultation Booking CTA */}
            <Link
              href="/book"
              className="px-4 py-2 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-semibold shadow-sm hover:shadow transition duration-150 flex items-center gap-1.5 shrink-0"
            >
              <HealthcareIcon name="calendar" className="w-3.5 h-3.5 text-[#A7F3D0]" />
              <span>Book Consultation</span>
            </Link>

            {/* Mobile Menu Toggle Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="xl:hidden p-2 rounded-xl text-[#334155] hover:bg-[#F1F5F9] transition"
              aria-label="Toggle navigation menu"
            >
              <HealthcareIcon name={mobileMenuOpen ? "x" : "menu"} className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="xl:hidden fixed inset-0 top-[80px] z-50 bg-white border-t border-[#E2E8F0] overflow-y-auto p-4 space-y-4 shadow-xl">
          <div className="space-y-1">
            {INSTITUTIONAL_HEADER_NAVIGATION.map((item) => (
              <div key={item.label} className="border-b border-[#F1F5F9] pb-2">
                <Link
                  href={item.href}
                  className="block py-2 text-sm font-bold text-[#0F172A]"
                >
                  {item.label}
                </Link>
                {item.dropdown && (
                  <div className="pl-3 space-y-1.5 pt-1">
                    {item.dropdown.map((sub) => (
                      <Link
                        key={sub.href}
                        href={sub.href}
                        className="flex items-center gap-2 py-1.5 text-xs text-[#475569] hover:text-[#1B4332]"
                      >
                        <HealthcareIcon name={sub.iconKey} className="w-3.5 h-3.5 text-[#2D6A4F]" />
                        <span>{sub.title}</span>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="pt-2 space-y-2 border-t border-[#E2E8F0]">
            <button
              onClick={() => { setMobileMenuOpen(false); setStaffModalOpen(true); }}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl border border-slate-300 bg-slate-100 text-slate-800 text-xs font-bold"
            >
              <HealthcareIcon name="lock" className="w-4 h-4 text-emerald-700" />
              <span>Staff / Clinician Gateway</span>
            </button>
            <Link
              href="/patient"
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl border border-[#D8F3DC] bg-[#E8F5E9] text-[#1B4332] text-xs font-bold"
            >
              <HealthcareIcon name="user" className="w-4 h-4 text-[#2D6A4F]" />
              <span>Patient Portal (My ZAYVORA™)</span>
            </Link>
            <Link
              href="/appointments"
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-[#1B4332] text-white text-xs font-bold"
            >
              <HealthcareIcon name="calendar" className="w-4 h-4" />
              <span>Book a Clinical Consultation</span>
            </Link>
          </div>
        </div>
      )}

      {/* Global ⌘K Quick Search Modal */}
      {searchModalOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="w-full max-w-xl bg-white rounded-2xl border border-[#CBD5E1] shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
            <div className="p-4 border-b border-[#E2E8F0] flex items-center gap-3">
              <HealthcareIcon name="search" className="w-5 h-5 text-[#94A3B8]" />
              <input
                type="text"
                placeholder="Search care programs, clinicians, health topics, or medicines..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="w-full text-sm text-[#0F172A] placeholder-[#94A3B8] focus:outline-none"
              />
              <button
                onClick={() => setSearchModalOpen(false)}
                className="text-xs font-semibold text-[#64748B] hover:text-[#0F172A]"
              >
                ESC
              </button>
            </div>

            <div className="p-2 max-h-80 overflow-y-auto space-y-1">
              {filteredResults.map((res, idx) => (
                <Link
                  key={idx}
                  href={res.href}
                  onClick={() => setSearchModalOpen(false)}
                  className="flex items-center justify-between p-3 rounded-xl hover:bg-[#F8FAFC] transition group"
                >
                  <div>
                    <p className="text-xs font-bold text-[#0F172A] group-hover:text-[#1B4332]">{res.title}</p>
                    <p className="text-[11px] text-[#64748B]">{res.sub}</p>
                  </div>
                  <HealthcareIcon name="arrow-right" className="w-4 h-4 text-[#CBD5E1] group-hover:text-[#1B4332]" />
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* CLINICIAN & STAFF LOGIN / 1-CLICK WORKSPACE MODAL */}
      {staffModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
          <div className="w-full max-w-2xl bg-white rounded-3xl border border-slate-200 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
            
            {/* Modal Header */}
            <div className="p-6 bg-gradient-to-r from-[#1B4332] to-[#2D6A4F] text-white flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center">
                  <HealthcareIcon name="shield-check" className="w-5 h-5 text-emerald-300" />
                </div>
                <div>
                  <h3 className="text-base font-bold tracking-tight text-white">ZAYVORA Health OS™ — Staff Gateway</h3>
                  <p className="text-xs text-emerald-100/80">Authorized Access for Clinicians, Pharmacists, and Administrators</p>
                </div>
              </div>
              <button
                onClick={() => setStaffModalOpen(false)}
                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition"
              >
                <HealthcareIcon name="x" className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 space-y-6">
            <div className="p-6 space-y-5">
              <div className="border-b border-slate-200 pb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-800 block">Clinician &amp; Operational Authentication</span>
                <p className="text-xs text-slate-500 mt-0.5">Please sign in with your institutional hospital or matab credentials.</p>
              </div>

              <form onSubmit={handleStaffFormSubmit} className="space-y-4">
                <div className="space-y-3">
                  <div>
                    <label className="text-[11px] font-semibold text-slate-600 block mb-1">Clinician / Staff Email</label>
                    <input
                      type="email"
                      placeholder="doctor@hospital.org"
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 focus:outline-none focus:border-emerald-600 font-mono"
                      required
                      autoFocus
                    />
                  </div>
                  <div>
                    <label className="text-[11px] font-semibold text-slate-600 block mb-1">Password</label>
                    <input
                      type="password"
                      placeholder="••••••••••••"
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 focus:outline-none focus:border-emerald-600 font-mono"
                      required
                    />
                  </div>
                </div>

                {loginError && (
                  <p className="text-xs text-rose-600 bg-rose-50 p-2.5 rounded-xl border border-rose-200">
                    {loginError}
                  </p>
                )}

                <div className="flex items-center justify-between pt-2">
                  <Link
                    href="/patient/forgot-password"
                    className="text-[11px] text-slate-500 hover:text-emerald-700 hover:underline"
                  >
                    Forgot Password?
                  </Link>
                  <button
                    type="submit"
                    disabled={loginLoading}
                    className="px-6 py-2.5 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white text-xs font-bold shadow-sm transition flex items-center gap-2"
                  >
                    {loginLoading ? (
                      <>
                        <HealthcareIcon name="refresh" className="w-3.5 h-3.5 animate-spin" />
                        <span>Authenticating...</span>
                      </>
                    ) : (
                      <>
                        <HealthcareIcon name="lock" className="w-3.5 h-3.5" />
                        <span>Sign In to Health OS</span>
                      </>
                    )}
                  </button>
                </div>
              </form>

              {/* Statutory Note */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-500 flex items-center justify-between">
                <span>Governed under <strong>NCISM Act 2020</strong> &amp; statutory electronic record and signature regulations.</span>
                <span className="font-mono text-[10px] text-slate-400">v5.0 Enterprise</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
