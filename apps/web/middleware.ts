import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * ZAYVORA Health OS™ — Unified Auth + Security Middleware
 *
 * Routing:
 * 1. www.zayvorahealth.com → Public website (marketing, doctor discovery)
 * 2. app/os/portal/clinical subdomains → Clinical OS (protected, no-index)
 *
 * Auth Guard:
 * - All CLINICAL_OS_PATHS require a valid zayvora_token in localStorage.
 *   Since middleware runs on the server (no localStorage), we use a
 *   HttpOnly-safe cookie "zayvora_auth" set at login as the guard signal.
 *   The client-side app additionally validates the token from localStorage.
 *
 * Role-Gate:
 * - /admin → only SUPER_ADMIN or CLINIC_ADMIN
 * - /doctor → only DOCTOR or HAKEEM
 * - /pharmacy → only PHARMACIST
 * - /receptionist, /reception → only RECEPTIONIST
 * - /patient → only PATIENT (or above)
 */

// Internal clinical & admin workspace paths (require auth)
const PROTECTED_PATHS = [
  "/doctor",
  "/dashboard",
  "/pharmacy",
  "/admin",
  "/clinic",
  "/reception",
  "/receptionist",
  "/research/workspace",
  "/research/knowledge-validation",
  "/research/cohorts",
  "/research/analytics",
  "/manufacturing",
  "/patient",
  "/nurse",
  "/analytics",
  "/billing",
  "/messages",
  "/notifications",
  "/telemedicine",
  "/protocols",
  "/settings",
  "/knowledge",
  "/ai",
];

// Paths that must NOT be accessible when already authenticated
const AUTH_ONLY_PATHS = ["/login"];

// Public paths — always accessible, no auth needed
const PUBLIC_PATHS = [
  "/",
  "/about",
  "/services",
  "/products",
  "/research",
  "/team",
  "/contact",
  "/faq",
  "/careers",
  "/privacy-policy",
  "/terms-and-conditions",
  "/patient/register",
  "/patient/login",
  "/patient/forgot-password",
  "/patient/reset-password",
  "/clinician/apply",
  "/organization/apply",
];

/** Role → allowed base paths (prefix matching) */
const ROLE_ALLOWED_PATHS: Record<string, string[]> = {
  SUPER_ADMIN:  ["/admin", "/doctor", "/pharmacy", "/receptionist", "/reception", "/patient", "/dashboard", "/analytics", "/billing", "/settings", "/research", "/manufacturing", "/clinic", "/nurse", "/messages", "/notifications", "/telemedicine", "/protocols", "/knowledge", "/ai"],
  CLINIC_ADMIN: ["/admin", "/dashboard", "/analytics", "/billing", "/settings", "/patient", "/doctor", "/pharmacy", "/receptionist", "/reception", "/messages", "/notifications"],
  DOCTOR:       ["/doctor", "/patient", "/telemedicine", "/messages", "/notifications", "/knowledge", "/protocols"],
  HAKEEM:       ["/doctor", "/patient", "/telemedicine", "/messages", "/notifications", "/knowledge", "/protocols"],
  RECEPTIONIST: ["/receptionist", "/reception", "/patient", "/messages", "/notifications"],
  PHARMACIST:   ["/pharmacy", "/messages", "/notifications", "/knowledge"],
  PATIENT:           ["/patient", "/messages", "/notifications", "/telemedicine"],
  NURSE:             ["/nurse", "/doctor/queue", "/messages", "/notifications"],
  NURSE_COORDINATOR: ["/nurse", "/doctor/queue", "/messages", "/notifications"],
  RESEARCHER:         ["/research", "/messages", "/notifications", "/knowledge", "/protocols"],
  MANUFACTURING_HEAD: ["/manufacturing", "/products", "/pharmacy/inventory", "/messages", "/notifications"],
};

function isProtectedPath(pathname: string): boolean {
  return PROTECTED_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/"));
}

function isPublicPath(pathname: string): boolean {
  return PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/"));
}

export function middleware(request: NextRequest) {
  const url = request.nextUrl;
  const hostname = request.headers.get("host") || "";
  const { pathname } = url;

  // ── Subdomain detection ──────────────────────────────────────────
  const isOsSubdomain =
    hostname.startsWith("app.") ||
    hostname.startsWith("os.") ||
    hostname.startsWith("portal.") ||
    hostname.startsWith("clinical.");

  // Redirect OS subdomain root to doctor panel
  if (isOsSubdomain && (pathname === "/" || pathname === "")) {
    return NextResponse.redirect(new URL("/doctor", request.url));
  }

  // ── Auth Guard ───────────────────────────────────────────────────
  // We use a lightweight cookie "zayvora_auth" that is set by the
  // client (via document.cookie, not HttpOnly) as the middleware signal.
  // Full JWT validation happens inside each page/API route.
  const authCookie = request.cookies.get("zayvora_auth")?.value;
  const isAuthenticated = !!authCookie;

  // If trying to access a protected path without auth → redirect to login
  if (isProtectedPath(pathname) && !isAuthenticated) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // If already logged in, don't show login page — redirect to their dashboard
  if (AUTH_ONLY_PATHS.some((p) => pathname === p) && isAuthenticated) {
    // Role is encoded in cookie value: "DOCTOR|<token_prefix>"
    const role = authCookie?.split("|")[0] || "PATIENT";
    const ROLE_MAP: Record<string, string> = {
      SUPER_ADMIN:  "/admin",
      CLINIC_ADMIN: "/admin",
      DOCTOR:       "/doctor",
      HAKEEM:       "/doctor",
      RECEPTIONIST: "/receptionist",
      PHARMACIST:   "/pharmacy",
      PATIENT:           "/patient",
      NURSE:             "/nurse",
      NURSE_COORDINATOR: "/nurse",
      RESEARCHER:         "/research/workspace",
      MANUFACTURING_HEAD: "/manufacturing",
    };
    const dest = ROLE_MAP[role.toUpperCase()] || "/dashboard";
    return NextResponse.redirect(new URL(dest, request.url));
  }

  // ── Role-based path guard ────────────────────────────────────────
  // If authenticated but accessing a path not allowed for their role
  if (isAuthenticated && isProtectedPath(pathname)) {
    const role = (authCookie?.split("|")[0] || "PATIENT").toUpperCase();
    const allowedPaths = ROLE_ALLOWED_PATHS[role] || ROLE_ALLOWED_PATHS["PATIENT"];
    const isAllowed = allowedPaths.some((p) => pathname === p || pathname.startsWith(p + "/"));

    if (!isAllowed) {
      // Redirect to their correct dashboard instead of showing 403
      const ROLE_MAP: Record<string, string> = {
        SUPER_ADMIN:  "/admin",
        CLINIC_ADMIN: "/admin",
        DOCTOR:       "/doctor",
        HAKEEM:       "/doctor",
        RECEPTIONIST: "/receptionist",
        PHARMACIST:   "/pharmacy",
        PATIENT:           "/patient",
        NURSE:             "/nurse",
        NURSE_COORDINATOR: "/nurse",
        RESEARCHER:         "/research/workspace",
        MANUFACTURING_HEAD: "/manufacturing",
      };
      const dest = ROLE_MAP[role] || "/dashboard";
      return NextResponse.redirect(new URL(dest, request.url));
    }
  }

  // ── Response with security headers ──────────────────────────────
  const response = NextResponse.next();

  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "SAMEORIGIN");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=(), interest-cohort=()"
  );
  response.headers.set("X-XSS-Protection", "1; mode=block");

  // Prevent search engines from indexing clinical workspaces
  const isClinicalPath = PROTECTED_PATHS.some((p) => pathname.startsWith(p));
  if (isOsSubdomain || isClinicalPath) {
    response.headers.set("X-Robots-Tag", "noindex, nofollow, noarchive, nosnippet");
  }

  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     * - public assets (images, icons, etc.)
     */
    "/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
