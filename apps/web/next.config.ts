import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      // Core Public Redirects
      { source: "/website", destination: "/", permanent: true },
      { source: "/website/about", destination: "/about", permanent: true },
      { source: "/website/care", destination: "/care", permanent: true },
      { source: "/website/services", destination: "/care", permanent: true },
      { source: "/website/clinical-care", destination: "/care", permanent: true },
      { source: "/website/ai-healthcare", destination: "/ai-transparency", permanent: true },
      { source: "/website/products", destination: "/products", permanent: true },
      { source: "/website/product", destination: "/products", permanent: true },
      { source: "/website/herbals", destination: "/products", permanent: true },
      { source: "/website/programs", destination: "/programs", permanent: true },
      { source: "/website/program", destination: "/programs", permanent: true },
      { source: "/website/doctors", destination: "/doctors", permanent: true },
      { source: "/website/doctor", destination: "/doctors", permanent: true },
      { source: "/website/clinics", destination: "/clinics", permanent: true },
      { source: "/website/matab", destination: "/clinics", permanent: true },
      { source: "/website/book", destination: "/book", permanent: true },
      { source: "/website/contact", destination: "/contact", permanent: true },
      { source: "/website/faqs", destination: "/faq", permanent: true },
      { source: "/website/faq", destination: "/faq", permanent: true },
      { source: "/website/careers", destination: "/careers", permanent: true },
      { source: "/website/privacy", destination: "/privacy-policy", permanent: true },
      { source: "/website/privacy-policy", destination: "/privacy-policy", permanent: true },
      { source: "/website/terms", destination: "/terms-and-conditions", permanent: true },
      { source: "/website/terms-and-conditions", destination: "/terms-and-conditions", permanent: true },
      { source: "/website/medical-disclaimer", destination: "/medical-disclaimer", permanent: true },
      { source: "/website/accessibility", destination: "/accessibility", permanent: true },
      { source: "/website/shipping-policy", destination: "/shipping-policy", permanent: true },
      { source: "/website/refund-policy", destination: "/refund-policy", permanent: true },
      
      // Role & Workspace Canonical Aliases
      { source: "/appointments", destination: "/book", permanent: true },
      { source: "/trust-safety", destination: "/trust", permanent: true },
      { source: "/receptionist", destination: "/reception", permanent: true },
      { source: "/clinic", destination: "/reception", permanent: true },
      { source: "/materia-medica", destination: "/knowledge", permanent: true },
      { source: "/dashboard", destination: "/doctor", permanent: true },

      // Catch-all legacy /website/* fallback
      { source: "/website/:slug*", destination: "/:slug*", permanent: true },
    ];
  },
  async headers() {
    return [
      {
        source: "/(doctor|pharmacy|admin|clinic|reception|receptionist|research|manufacturing|patient)/:path*",
        headers: [
          { key: "X-Robots-Tag", value: "noindex, nofollow, noarchive, nosnippet" },
          { key: "X-Frame-Options", value: "SAMEORIGIN" },
          { key: "X-Content-Type-Options", value: "nosniff" },
        ],
      },
    ];
  },
};

export default nextConfig;
