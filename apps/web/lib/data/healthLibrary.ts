/**
 * ZAYVORA Health OS™ — Health Library & Editorial Knowledge System (NHS & NCISM Aligned)
 *
 * Implements strict clinical editorial standards:
 * - Author & Senior Clinical Reviewer
 * - Authoritative Unani & Modern Scientific Sources
 * - Verified Last Reviewed Date & Next Scheduled Review Date
 * - Version Control & Target Audience Classification
 * - Prominent Medical Disclaimer & Emergency Callout
 */

export interface HealthLibraryArticle {
  slug: string;
  title: string;
  category: "Conditions" | "Symptoms" | "Tests" | "Treatments" | "Lifestyle" | "Unani Concepts" | "Patient Guides";
  summary: string;
  author: {
    name: string;
    qualification: string;
    role: string;
  };
  clinicalReviewer: {
    name: string;
    qualification: string;
    ncismRegNumber: string;
    reviewDate: string;
    nextReviewDate: string;
  };
  version: string;
  readingTimeMinutes: number;
  sources: string[];
  contentSections: {
    heading: string;
    body: string;
    unaniPerspective?: string;
  }[];
  redFlagEmergencySigns: string[];
  faqs: { question: string; answer: string }[];
}

export const HEALTH_LIBRARY_ARTICLES: HealthLibraryArticle[] = [
  {
    slug: "understanding-waja-ul-mafasil-joint-health",
    title: "Understanding Waja-ul-Mafasil: Joint Care, Mizaj & Cartilage Restitution",
    category: "Conditions",
    summary: "A comprehensive guide to joint stiffness, cold-wet humoral dystemperament (Su-e-Mizaj Barid Balghami), and classical 3-phase Unani recovery protocols.",
    author: {
      name: "Hakeem Dr. Irfan Ashraf",
      qualification: "BUMS (AKTC AMU Aligarh, Batch 2002-2007)",
      role: "Founder, Chairman & Chief Architect"
    },
    clinicalReviewer: {
      name: "Prof. (Dr.) Mansoor Alam",
      qualification: "BUMS, MD (Unani) Moalejat",
      ncismRegNumber: "UP-UNANI-2012-08819",
      reviewDate: "2026-09-01",
      nextReviewDate: "2027-09-01"
    },
    version: "2026.2",
    readingTimeMinutes: 6,
    sources: [
      "Ibn Sina, Al-Qanun fi al-Tibb (The Canon of Medicine), Book III (Special Pathology)",
      "Unani Pharmacopoeia of India (UPI), Part-I, Vol-I, Ministry of AYUSH, Govt. of India",
      "CCRUM Guidelines for Clinical Research in Unani Medicine, New Delhi",
      "EULAR Recommendations for the Management of Rheumatoid and Osteo-Arthritis"
    ],
    contentSections: [
      {
        heading: "1. What is Waja-ul-Mafasil?",
        body: "Waja-ul-Mafasil (Joint Arthralgia) literally translates to 'pain of the joints'. In classical Unani clinical medicine, it encompasses disorders involving synovial articulation, including osteoarthritis, gouty arthritis (Niqris), and inflammatory arthropathy. Rather than treating the joint in isolation, Unani medicine identifies the systemic humoral imbalance allowing morbid matter (Mawad-e-Fasida) to settle in vulnerable articulating cartilage.",
        unaniPerspective: "Classified by the dominant humor: Balghami (Phlegmatic/Cold-Moist), Damawi (Sanguinous/Warm-Moist), or Safrawi (Bilious/Hot-Dry)."
      },
      {
        heading: "2. The Three-Phase Restitution Protocol",
        body: "Standard treatment follows the classical therapeutic sequence: (1) Tanqia-e-Mawad: Coction and expulsion of accumulated cold phlegmatic matter through gentle carminative and laxative formulations. (2) Tadeel-e-Mizaj: Restoring natural equilibrium using warm-dry single herbs such as Suranjan (Colchicum), Asgand (Withania), and Zanjabeel (Ginger). (3) Taqwiyat-e-Aaza: Strengthening local peri-articular ligaments and muscles through regimenal therapy (Ilaj-bit-Tadbeer)."
      },
      {
        heading: "3. Nutrition & 8-Tier Parhez Guidelines",
        body: "Dietary therapy is the cornerstone of joint care. Patients are advised to strictly eliminate cold and moist food items (ice water, excessive yoghurt, raw cucumbers, heavy viscous red meats) that exacerbate phlegm production. Warm broths cooked with carminative spices (cinnamon, cumin, clove, garlic) actively support digestion and metabolic heat."
      }
    ],
    redFlagEmergencySigns: [
      "Rapid joint swelling accompanied by high fever and severe redness (suspected septic arthritis)",
      "Sudden inability to bear any weight with severe excruciating pain",
      "Loss of sensation or progressive weakness in the limb below the joint"
    ],
    faqs: [
      {
        question: "Can Unani treatment be taken alongside my regular blood pressure medicines?",
        answer: "Yes, under certified clinician supervision. ZAYVORA's Permanent Safety Rail screens every prescribed herb against Cytochrome P450 interactions to ensure total safety."
      },
      {
        question: "How soon do patients experience relief from morning stiffness?",
        answer: "Most patients report measurable reduction in morning stiffness within 14 to 21 days as digestive coction (Nujz) and synovial circulation improve."
      }
    ]
  },
  {
    slug: "metabolic-health-and-asbab-sitta-essentials",
    title: "Metabolic Health & Asbab Sitta: The Six Non-Negotiable Pillars of Wellness",
    category: "Lifestyle",
    summary: "How ancient Unani preventive medicine governs insulin sensitivity, cellular energy, and circadian rhythms through environmental and metabolic equilibrium.",
    author: {
      name: "Dr. Aisha Siddiqui",
      qualification: "BUMS, MD (Tahaffuzi wa Samaji Tibb)",
      role: "Consultant Preventive Medicine"
    },
    clinicalReviewer: {
      name: "Hakeem Dr. Irfan Ashraf",
      qualification: "BUMS (AKTC AMU Aligarh, Batch 2002-2007)",
      ncismRegNumber: "Reg. No: (Updating / Verification in Progress)",
      reviewDate: "2026-09-05",
      nextReviewDate: "2027-09-05"
    },
    version: "2026.1",
    readingTimeMinutes: 5,
    sources: [
      "Al-Razi (Rhazes), Kitab al-Hawi fi al-Tibb (Continens Liber)",
      "NCISM Model Curriculum for Tahaffuzi wa Samaji Tibb (Preventive Healthcare)",
      "Lancet Diabetes & Endocrinology: Circadian Disruption and Metabolic Syndrome"
    ],
    contentSections: [
      {
        heading: "1. The Concept of Asbab-e-Sitta Zarooriya",
        body: "In Unani physiological philosophy, health is sustained by six essential external influences (Asbab-e-Sittah Zarooriyyah): (1) Ambient Air & Environment (Hawa), (2) Food & Drink (Makool wa Mashroob), (3) Physical Movement & Rest (Harkat wa Sukoon-e-Badani), (4) Sleep & Wakefulness (Naum wa Yaqza), (5) Retention & Evacuation (Ehtebas wa Istifragh), and (6) Emotional & Psychological Balance (Harkat wa Sukoon-e-Nafsani).",
        unaniPerspective: "A disturbance in any single pillar leads to altered Tabiyat (the innate self-healing intelligence of the human body)."
      },
      {
        heading: "2. Resetting Insulin Sensitivity",
        body: "Modern sedentary habits and late-night meals directly violate the sleep and movement pillars, producing chronic Su-e-Hazm (impaired digestion) and accumulation of crude chyme (Kham Balgham). By aligning meal timing with diurnal solar cycles and engaging in moderate daily ambulation (Riyazat-e-Motadila), cellular receptivity is restored naturally."
      }
    ],
    redFlagEmergencySigns: [
      "Fasting blood glucose > 250 mg/dL accompanied by nausea or confusion",
      "Sudden shortness of breath or crushing chest pressure during physical exertion"
    ],
    faqs: [
      {
        question: "What is the best time for breakfast according to Unani principles?",
        answer: "Breakfast should be consumed when the natural morning metabolic heat (Hararat-e-Ghariziya) is stimulated, typically within 1 to 2 hours of sunrise after light movement."
      }
    ]
  }
];
