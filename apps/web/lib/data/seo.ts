import { Metadata } from "next";
import { siteConfig } from "./siteConfig";

interface PageMetadataProps {
  title: string;
  description: string;
  path: string;
  noIndex?: boolean;
}

export function createPageMetadata({
  title,
  description,
  path,
  noIndex = false
}: PageMetadataProps): Metadata {
  const fullTitle = `${title} | ${siteConfig.name}`;
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://www.zayvorahealth.com";
  const canonicalUrl = `${baseUrl}${path.startsWith("/") ? path : `/${path}`}`;

  return {
    title: fullTitle,
    description,
    alternates: {
      canonical: canonicalUrl
    },
    openGraph: {
      title: fullTitle,
      description,
      url: canonicalUrl,
      siteName: siteConfig.name,
      images: [
        {
          url: `${baseUrl}/og-image.png`,
          width: 1200,
          height: 630,
          alt: `${siteConfig.name} — ${title}`
        }
      ],
      type: "website"
    },
    twitter: {
      card: "summary_large_image",
      title: fullTitle,
      description,
      creator: "@zayvorahealth"
    },
    robots: noIndex
      ? { index: false, follow: false }
      : { index: true, follow: true }
  };
}
