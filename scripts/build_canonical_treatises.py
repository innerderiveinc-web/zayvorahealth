import os
import sys
import json

output_file = "services/knowledge/app/data/canonical_treatises.py"

# We will generate CANONICAL_TREATISES dict mapping chapter_id -> treatise dict
print("Preparing 38 canonical academic treatises across 12 volumes...")

TREATISES = {}

# -----------------------------------------------------------------------------
# VOLUME I: KULLIYAT-E-TIBB & HUMAN PHYSIOLOGY (4 CHAPTERS)
# -----------------------------------------------------------------------------
TREATISES["ch-01-01"] = {
    "chapter_id": "ch-01-01",
    "volume_id": "vol-01",
    "chapter_title_en": "Arkan-e-Arba'a: The Four Elements & States of Matter",
    "chapter_title_ur": "ارکانِ اربعہ اور مادی تغیرات — طبیعیاتی حرارت اور حیاتیاتی اینٹروپی",
    "canonical_philosophy_and_doctrine": """
The doctrine of Arkan (Classical Elements) constitutes the ultimate biophysical foundation of Greco-Arab medicine, formulated across centuries by Empedocles, Hippocrates, Aristotle, Galen, and finalized by Ibn Sina in 'Al-Qanoon fit-Tibb' (Book 1, Fen 1, Treatise 1). 

Ibn Sina defines Arkan as: 'الأركان هي أجرام بسيطة، هي أجزاء أولية لبدن الإنسان وغيره، ولا يمكن انقسامها إلى أجسام مختلفة الصور' (Arkan are simple, indivisible primary bodies which form the foundational substrates of the human organism and natural entities; they cannot be further decomposed into heterogeneous substances). 

The four Arkan represent the four fundamental thermodynamic and physical states of existence:
1. **Arz (Earth / مٹی)**: Absolutely heavy and static. Its innate primary quality is Coldness and Dryness (Barid-Yabis). It confers structural integrity, anatomical density, cohesion, and permanence to tissues (bones, cartilage, dense connective matrices).
2. **Ma' (Water / پانی)**: Relatively heavy and fluid. Its innate primary quality is Coldness and Moisture (Barid-Ratab). It confers fluidity, malleability, hydration shells around macromolecules, and facilitates cellular transport and biological diffusion.
3. **Hawa (Air / ہوا)**: Relatively light and rarefied. Its innate primary quality is Hotness and Moisture (Garm-Ratab / Har-Ratab). It imparts porosity, elasticity, expansion, volatile transmission, and facilitates internal pulmonary and tissue respiration.
4. **Nar (Fire / آگ)**: Absolutely light and energetic. Its innate primary quality is Hotness and Dryness (Garm-Khushk / Har-Yabis). It represents biological heat, kinetic energy, cellular maturation (Nujd), metabolic transformation, and enzymatic breakdown.

According to Hakim Kabiruddin in 'Kulliyat-e-Qanoon', health exists when the mutual action and reaction of these four qualities achieves a harmonious equilibrium (*Itidal-e-Mizaji*). When one elemental force becomes disproportionately aggravated without material discharge, *Su-e-Mizaj Sada* occurs; when accompanied by morbid fluid retention, *Su-e-Mizaj Maddi* supervenes.
""",
    "molecular_and_cellular_pathophysiology": """
In contemporary biophysics and molecular physiology, the four Arkan map precisely to the physical phases of matter and bioenergetic thermodynamic cascades:
- **Solid Phase (Arz)**: Correlates directly with the extracellular matrix (ECM), cross-linked Type I/II collagen fibrillogenesis, hydroxyapatite crystallites in osseous tissue, and the polymerized actin-spectrin cytoskeleton that maintains cellular tensile resistance.
- **Liquid Phase (Ma')**: Represents the intracellular and extracellular aqueous compartments (60% total body water), cytosolic solvent shells, transmembrane osmotic hydrostatic pressure, and the Gibbs-Donnan equilibrium governing sodium, potassium, and chloride gradients.
- **Gas Phase (Hawa)**: Correlates with alveolar gas exchange, dissolved plasma oxygen tension (PaO2), arterial carbon dioxide tension (PaCO2), bicarbonate buffering equilibrium (CO2 + H2O <-> H2CO3 <-> HCO3- + H+), and gaseous signaling molecules including volatile Nitric Oxide (eNOS/iNOS) and Carbon Monoxide (HO-1).
- **Plasma & Energy State (Nar)**: Represents cellular bioenergetics—specifically mitochondrial adenosine triphosphate (ATP) synthesis via oxidative phosphorylation, the proton electrochemical gradient (ΔΨm) across the inner mitochondrial membrane, and non-shivering thermogenesis mediated by Uncoupling Protein 1 (UCP-1/Thermogenin) in brown adipose tissue (BAT).
""",
    "step_by_step_clinical_examination": """
1. **Thermal Equilibrium Inspection**: Palpate skin temperature bilaterally at the sternal core vs distal phalanges. Acral hypothermia with core normothermia indicates peripheral vasoconstriction (excess coldness/Barudat).
2. **Moisture & Tissue Hydration Assessment**: Inspect oral mucosa, buccal gingiva, and sublingual folds for salivary pooling vs xerostomia. Perform cutaneous skin pinch over the forearm (delayed snapback indicates systemic Yaboosat/dehydration).
3. **Tensile & Elasticity Evaluation**: Assess joint range of motion and tissue suppleness. Excessive laxity denotes hyper-moist (Ratab) state; crepitus and rigid contracture denote dry (Yabis) state.
4. **Resonant Acoustic Percussion**: Perform chest and abdominal percussion to evaluate gaseous distension (Nafakh/Hawa) vs fluid dullness (Istisqa/Ma') vs visceral organ density (Arz).
""",
    "comprehensive_pharmacopeia_and_recipes": """
**Classical Formula: Sufuf-e-Muharrik-e-Hararat (Thermal Activation Compound)**
- *Indication*: Severe Barudat (Hypometabolic hypothermia, sluggish circulation, chronic joint stiffness).
- *Ingredients*:
  1. Zanjabeel (Zingiber officinale rhizome) — 30g (Hot 3°, Dry 2°)
  2. Filfil Siyah (Piper nigrum fruit) — 15g (Hot 3°, Dry 3°)
  3. Darchini (Cinnamomum verum bark) — 20g (Hot 3°, Dry 2°)
  4. Qaranfal (Syzygium aromaticum flower buds) — 10g (Hot 3°, Dry 3°)
- *Processing & SOP*: Clean raw botanicals under ambient dry air. Pulverize to micro-mesh passing sieve #80. Store in airtight amber glass jars.
- *Dosage & Administration*: 2g twice daily after meals with lukewarm water infused with 5ml pure honey (Ma-ul-Asal).
- *Musleh (Corrective)*: Samagh-e-Arabi (Gum Acacia) 500mg if gastric pyrosis occurs.
""",
    "clinical_case_study": """
**Patient**: 44-year-old male presenting with chronic generalized Barudat (cold intolerance, basal oral temperature 35.7°C, morning stiffness, sinus bradycardia 52 bpm, severe postprandial sleepiness).
**Baseline Diagnostics**: TSH: 4.6 mIU/L (subclinical hypothyroid), Fasting Glucose: 108 mg/dL, hs-CRP: 2.8 mg/L. Pulse: *Nabz-e-Batee*, *Saghir*, *Layyin* (Slow, Small, Soft).
**Diagnostic Formulation**: *Su-e-Mizaj Barid Balghami Maddi* with diminished innate metabolic fire (Hararat-e-Ghariziyyah).
**Integrative Protocol**: 
- Days 1–14: Administration of *Sufuf-e-Muharrik-e-Hararat* 2g BID + Hab-e-Suranjan 1 tab OD after dinner + 20 minutes daily morning solar exposition (*Tashmees*).
- Dietary Modification: Elimination of dairy, cucumber, and iced water; incorporation of sheep bone broth (*Shorba*) seasoned with ginger and cumin.
**30-Day Outcome**: Oral temperature stabilized to 36.8°C; heart rate elevated to 68 bpm; postprandial lethargy abolished; hs-CRP decreased to 0.9 mg/L; subjective vitality scale improved from 3/10 to 8/10.
"""
}

TREATISES["ch-01-02"] = {
    "chapter_id": "ch-01-02",
    "volume_id": "vol-01",
    "chapter_title_en": "Akhlat-e-Arba'a: Humoral Dynamics & Fluid Compartments",
    "chapter_title_ur": "اخلاطِ اربعہ اور جسمانی مائعات — ہضمِ ثانی، جگر اور عروقی توازن",
    "canonical_philosophy_and_doctrine": """
The doctrine of Akhlat (Humors) represents the dynamic biochemical fluid continuum of human physiology. In 'Kitab al-Hawi fit-Tibb', Abu Bakr Muhammad ibn Zakariyya al-Razi (Rhazes) establishes that humors are not static fluids but living physiological juices continuously generated in the liver via Second Digestion (Hazm-e-Sani) from the nutrient chyme (Kiloos) delivered by the portal vein.

Ibn Sina elaborates in 'Al-Qanoon' that an Akhlat is defined as: 'الخلط جسم رطب سيال يستحيل إليه الغذاء أولا' (A humor is a moist, fluid body into which ingested nutrient matter is primarily converted). The four humors maintain homeostatic stoichiometry:
1. **Dam (Sanguinous Humor / خون)**: Hot and Moist (Har-Ratab). The supreme humor (*Afzal-ul-Akhlat*), characterized by rich red color, sweetish taste, and moderate density. It carries biological heat and nourishment to every cell.
2. **Balgham (Phlegmatic Humor / بلغم)**: Cold and Moist (Barid-Ratab). A raw, unripened humor serving as a metabolic emergency reserve, mucosal lubricant, joint cushioning fluid, and thermal buffer.
3. **Safra (Yellow Bile / صفراء)**: Hot and Dry (Har-Yabis). Light, fiery, and bitter. Synthesized by hepatocytes; maintains blood fluidity, stimulates intestinal peristalsis, and emulsifies lipids.
4. **Sauda (Black Bile / سوداء)**: Cold and Dry (Barid-Yabis). Heavy, astringent, and earthy. Originates from dense metabolic sediments and splenic processing; confers tissue firmness, bone mineralization, and mental appetite/tenacity.

Each humor possesses two states: **Mahmood (Normal / Physiological)** and **Ghair-Mahmood (Abnormal / Pathological)**. When an abnormal humor ferments, burns (*Ihtiraq*), or putrefies, it generates systemic humoral dyscrasia (*Ufoonat*).
""",
    "molecular_and_cellular_pathophysiology": """
The four humors correspond to distinct biological fluid compartments, rheological properties, and metabolic fractions:
- **Dam (Sanguine)**: Directly corresponds to whole blood volume, normocytic normochromic erythrocytes, plasma hemoglobin mass, and the oxygen delivery cascade (HbO2 saturation). It governs peripheral perfusion pressure and microvascular shear stress.
- **Balgham (Phlegm)**: Correlates with the interstitial fluid volume, lymphatic circulation, high-molecular-weight proteoglycans, synovial hyaluronan, and mucosal surfactant coatings. Pathological Balgham reflects elevated triglycerides, plasma transudates, and mucopolysaccharide stasis.
- **Safra (Yellow Bile)**: Correlates with bile acid salts (cholic, deoxycholic, and chenodeoxycholic acids), bilirubin glucuronides, pancreatic lipases, and systemic free fatty acid turnover. Excess Safra induces oxidative lipid peroxidation, glutathione depletion, and mitochondrial membrane permeabilization.
- **Sauda (Black Bile)**: Correlates with circulating platelet mass, splenic hemocatheresis products, polymerized ferritin/hemosiderin complexes, serum calcium-phosphate crystallization, and insoluble fibrin networks. Pathological Sauda reflects hypercoagulability, elevated D-dimer, and neuro-inflammatory microglial hyper-activation.
""",
    "step_by_step_clinical_examination": """
1. **Scleral & Mucosal Color Topography**: Inspect bulbar conjunctiva under natural daylight. Bright red suffusion indicates Damawi plethora; pale milky hue indicates Balghami serosity; yellowish-icteric tint indicates Safrawi regurgitation; dark sub-conjunctival dullness indicates Saudawi accumulation.
2. **Tongue Dorsum Stratification**: Inspect dorsal tongue coat. Thick white greasy fur indicates Balgham; thin bright yellow dry coat indicates Safra; dark brown/black dry crusting indicates burnt Sauda; clean beefy red indicates Dam.
3. **Hemodynamic & Vascular Palpation**: Palpate radial artery for fullness (Imtila) vs emptiness (Khulu). A bounding, tense, wide pulse signifies Damawi hypervolemia; a soft, wavy, undulating pulse signifies Balghami stagnation; a sharp, narrow, rapid pulse signifies Safrawi irritability.
4. **Subungual Capillary Refill**: Press distal nailbed for 5 seconds. Delayed refill (>3 seconds) indicates Saudawi microvascular constriction or Balghami hypoperfusion.
""",
    "comprehensive_pharmacopeia_and_recipes": """
**Classical Formula: Sharbat-e-Deenar (Hepatic & Humoral Decoction)**
- *Indication*: Stagnant Safra and morbid Balgham accumulating in the portal-hepatobiliary axis, presenting with visceral congestion and early hepatomegaly.
- *Ingredients*:
  1. Tukhm-e-Kasni (Cichorium intybus seeds) — 20g
  2. Tukhm-e-Kasoos (Cuscuta reflexa seeds) — 15g
  3. Gul-e-Surkh (Rosa damascena petals) — 20g
  4. Gul-e-Ghaafis (Agrimonia eupatoria flowers) — 15g
  5. Rewand Chini (Rheum emodi root) — 10g
  6. Qand Safaid (Refined sugar matrix) — 500g
- *SOP & Extraction*: Macerate botanicals in 1.5L distilled water overnight (12 hours). Boil over gentle flame until reduced to 500ml. Strain through double-layered surgical muslin. Add sugar matrix and boil to three-thread density (*Qiwam Seh Taar*).
- *Dosing*: 25ml mixed in 100ml lukewarm water, administered early morning fasting (*Naharr*).
""",
    "clinical_case_study": """
**Patient**: 39-year-old female executive with chronic Safrawi dyscrasia (epigastric burning, bitter morning taste, irritability, recurrent migrainous headache with retro-orbital throbbing, loose bilious stools).
**Investigations**: Total Bilirubin: 1.4 mg/dL, Direct Bilirubin: 0.5 mg/dL, ALT: 48 U/L, ESR: 18 mm/hr. Pulse: *Nabz-e-Azeem*, *Saree*, *Sulb* (Large, Rapid, Hard).
**Clinical Assessment**: *Su-e-Mizaj Safrawi Maddi* with early biliary dyskinesia and micro-inflammation.
**Integrative Protocol**:
- 7-Day Munzij-e-Safra regimen: *Arq Mako* (30ml) + *Arq Kasni* (30ml) with *Sharbat-e-Bazoori Motadil* (20ml) BID.
- Regimenal Therapy: Evacuative *Hijama Bila Shart* (dry cupping over right hypochondrium) followed by single session of *Hijama Ma'a Shart* (wet cupping between interscapular region, 35ml controlled sanguineous-safrawi extraction).
**Follow-up (Day 21)**: Complete resolution of epigastric burning and cephalalgia; serum ALT normalized to 24 U/L; pulse softened to *Mu'tadil* cadence; patient reported restored sleep and emotional equanimity.
"""
}

TREATISES["ch-01-03"] = {
    "chapter_id": "ch-01-03",
    "volume_id": "vol-01",
    "chapter_title_en": "Ilm-ul-Mizaj: Temperamental Science & Metabolic Typing",
    "chapter_title_ur": "علم المزاج اور انفرادی بائیو کیمسٹری — موروثی جینیات اور بائیو مارکرز",
    "canonical_philosophy_and_doctrine": """
Ilm-ul-Mizaj (The Science of Temperament) is the cornerstone of personalized precision medicine in Unani clinical philosophy. In 'Al-Qanoon', Ibn Sina establishes that every individual is born with a distinct constitutional baseline temperament (*Mizaj-e-Jibli / Asli*), perfectly balanced (*Mao'tadil*) for that specific person, even though it leans toward one of the four dominant combinations:
1. **Mizaj Damawi (Sanguine / Hot-Moist)**: Robust athletic build, rosy florid complexion, prominent venous vasculature, active digestive fire, generous sociable disposition, high physical stamina.
2. **Mizaj Balghami (Phlegmatic / Cold-Moist)**: Endomorphic build, fair/pale skin, soft flabby musculature, slow sluggish digestion, prolonged deep sleep, calm passive temperament, vulnerability to fluid retention.
3. **Mizaj Safrawi (Choleric / Hot-Dry)**: Ecto-mesomorphic build, yellowish/bronze skin, sharp penetrating gaze, rapid ferocious digestion, light restless sleep, ambitious assertive nature, low tolerance for heat.
4. **Mizaj Saudawi (Melancholic / Cold-Dry)**: Asthenic lean build, dusky dark complexion, prominent tendons and bony landmarks, variable capricious digestion, insomniac rumination, analytical serious temperament, prone to obsessive ruminations.

Furthermore, every organ in the human body has an inherent organ temperament (*Mizaj-ul-Aaza*):
- The **Heart (Qalb)** is inherently Hot-Dry (generating continuous contractile kinetic calorigenesis).
- The **Brain (Dimagh)** is inherently Cold-Moist (to allow rapid axonal rewiring and prevent metabolic burn-out).
- The **Liver (Kabid)** is inherently Hot-Moist (to sustain continuous macromolecular synthesis and metabolic transformation).
- The **Bones (Izaam)** are inherently Cold-Dry (to maintain structural rigidity and mineral crystallization).
""",
    "molecular_and_cellular_pathophysiology": """
Contemporary genomics, neuroendocrinology, and metabolic profiling directly illuminate the biochemical basis of classical Mizaj:
- **Hot Phenotypes (Damawi & Safrawi)**: Exhibit heightened sympathetic autonomic nervous system (SANS) baseline tone, elevated resting basal metabolic rates (BMR), increased thyroid hormone receptor sensitivity (elevated free T3/T4 conversion), and enhanced glucose transporter type 4 (GLUT4) translocation in skeletal muscle.
- **Cold Phenotypes (Balghami & Saudawi)**: Exhibit dominant parasympathetic tone, lower resting metabolic expenditure, reduced brown adipose tissue thermogenic density, downregulated beta-3 adrenergic receptor sensitivity, and slower hepatic cytochrome P450 phase I clearance rates.
- **Moist Phenotypes (Damawi & Balghami)**: Feature expanded circulating plasma volumes, higher extracellular fluid retention, increased endothelial nitric oxide synthase (eNOS) activity, and elevated antidiuretic hormone (ADH/Vasopressin) sensitivity.
- **Dry Phenotypes (Safrawi & Saudawi)**: Characterized by accelerated transepidermal water loss (TEWL), low synovial hyaluronic acid concentrations, heightened renin-angiotensin-aldosterone system (RAAS) reactivity, and increased baseline inflammatory cytokine expression (IL-1beta, TNF-alpha).
""",
    "step_by_step_clinical_examination": """
The 10 Canonical Determinants of Individual Mizaj (*Ajnas-e-Ashara li-Tashkhees-ul-Mizaj*):
1. **Malmas (Tactile Skin Quality)**: Palpate volar forearm. Hot/Cold denotes temperature axis; Soft/Hard denotes moisture axis.
2. **Lahm-o-Shahm (Body Composition)**: Ratio of muscle mass (*Lahm*) vs adipose tissue (*Shahm*). High muscle = Damawi; High fat = Balghami; Low fat/muscle = Saudawi.
3. **Sha'ar (Hair Topography)**: Density, color, and curling rate. Rapid growth, thick, dark curly hair = Hot-Dry (Safrawi); Slow growing, fine, straight, light hair = Cold-Moist (Balghami).
4. **Laun-ul-Badan (Skin Pigmentation & Complexion)**: Florid pink (Dam), pale alabaster (Balgham), sallow yellow (Safra), dusky leaden (Sauda).
5. **Hayat-ul-Aaza (Morphological Frame)**: Broad deep chest with prominent veins = Damawi; narrow contracted chest with hidden veins = Saudawi.
6. **Infi'al-ul-Hawaas (Sensory Reactivity)**: Immediate sharp reaction to external stimuli = Hot-Dry; delayed lethargic response = Cold-Moist.
7. **Af'aal-ul-Aaza (Functional Efficiency)**: Speed of digestive transit, cardiac output, and musculoskeletal agility.
8. **Fuzlaat-ul-Badan (Excretory Nature)**: Volume, odor, and color of perspiration, urine, and stool. Strong pungent odor with dark color = Hot-Dry.
9. **Naum-o-Yaqza (Sleep Patterns)**: Heavy profound sleep (>8h) = Cold-Moist; light interrupted sleep (<6h) = Hot-Dry or Cold-Dry.
10. **Harkat-o-Sukoon-e-Nafsani (Psychological Dispositions)**: Rapid anger followed by rapid remorse = Safra; prolonged brooding and anxiety = Sauda; cheerful optimism = Dam; placid apathy = Balgham.
""",
    "comprehensive_pharmacopeia_and_recipes": """
**Classical Temperamental Normalizer: Majun Mu'tadil-ul-Mizaj**
- *Indication*: General temperamental disequilibrium, chronic constitutional convalescence, seasonal dyscrasias.
- *Formulation Matrix*:
  1. Maghz-e-Badam Shireen (Prunus dulcis kernels) — 50g
  2. Maghz-e-Fistuq (Pistacia vera kernels) — 30g
  3. Tukhm-e-Kahu (Lactuca sativa seeds) — 20g
  4. Tukhm-e-Khashkhash (Papaver somniferum seeds) — 20g
  5. Zafran (Crocus sativus stigmas) — 2g (triturated in Arq Gulab)
  6. Asal-e-Khalis (Pure mountain honey) — 350g
- *Method*: Blanch nut kernels in warm water, remove skins, dry under shade, and micro-grind. Dissolve saffron in 10ml rose water. Incorporate powders incrementally into warmed honey matrix at 45°C. Age for 7 days in glazed ceramic vessel (*Martaban*).
- *Dosage*: 7g morning and evening with 150ml goat's milk or almond milk.
""",
    "clinical_case_study": """
**Patient**: 28-year-old male software architect of innate Safrawi temperament presenting with acute *Su-e-Mizaj Har-Yabis* (insomnia, severe aphthous stomatitis, ocular burn, pulse 94 bpm bounding, severe anxiety, elevated ALT 52 U/L, morning cortisol 24 mcg/dL).
**Etiological Trigger**: Chronic night shift work, excessive stimulant consumption (6 cups espresso daily), and diet rich in spicy fried meats.
**Integrative Protocol**:
- Dietary: Complete elimination of all stimulants and allium vegetables (garlic/onion). Prescription of cooling hydration diet: barley water (*Ma-ul-Sha'eer*), cucumber-seed cooling drink (*Tukhm-e-Khyarein*), pomegranate juice.
- Pharmacotherapy: *Sharbat-e-Nilofar* 25ml BID + *Khamira Gaozaban Ambari Jadwar Ood Saleeb Wala* 5g at bedtime.
- Regimenal: *Natool* (cranial irrigation) with decoction of Gul-e-Banafsha and Gul-e-Nilofar lukewarm for 15 minutes before sleep.
**Day 14 Outcome**: Complete resolution of stomatitis; sleep duration restored to 7.5 hours continuous; pulse normalized to 72 bpm; morning cortisol dropped to 14.2 mcg/dL; full psychological recovery.
"""
}

TREATISES["ch-01-04"] = {
    "chapter_id": "ch-01-04",
    "volume_id": "vol-01",
    "chapter_title_en": "Quwa & Afaal: Vital, Natural & Psychic Physiology",
    "chapter_title_ur": "قویٰ اور افعال — حیوانی، طبعی اور نفسیاتی نظام اور ہومیوسٹاسس",
    "canonical_philosophy_and_doctrine": """
In the physiological hierarchy of Tibb-e-Unani, Quwa (Biological Faculties) represent the functional energies and homeostatic mechanisms through which the human organism operates, while Afaal (Actions/Functions) represent the measurable physiological manifestations of those faculties.

Ali ibn Rabban al-Tabari in 'Firdaus al-Hikma' and Ibn Sina in 'Al-Qanoon' categorize Quwa into three sovereign domains anchored in the Three Master Organs (*Al-Aaza al-Ra'eesa*):
1. **Quwwat-e-Tabi'iyyah (Natural / Metabolic Faculty)**:
   - *Primary Seat*: Kabid (Liver).
   - *Subordinate Faculties*:
     - *Quwwat-e-Ghaziyyah* (Nutritive Faculty): Encompasses Jadhba (Ingestion/Attraction), Masika (Retention), Hadima (Digestion/Transformation), and Dafi'a (Expulsion).
     - *Quwwat-e-Namiyyah* (Growth/Anabolic Faculty): Governs tissue hypertrophy, cellular proliferation, and repair.
     - *Quwwat-e-Tawalludiyyah* (Reproductive/Gametic Faculty): Governs spermatogenesis, oogenesis, and embryogenesis.
2. **Quwwat-e-Hayawaniyyah (Vital / Cardiovascular Faculty)**:
   - *Primary Seat*: Qalb (Heart).
   - *Subordinate Faculties*: Governs pulsatile arterial expansion (*Inbisat*) and contraction (*Inqibad*), biological respiration, distribution of innate pneuma (*Rooh-e-Hayawani*), and maintenance of core somatic life and instinctive survival responses.
3. **Quwwat-e-Nafsaniyyah (Psychic / Neurological Faculty)**:
   - *Primary Seat*: Dimagh (Brain).
   - *Subordinate Faculties*:
     - *Quwwat-e-Mudrikah* (Cognitive / Perceptual Faculty): Internal senses (Hiss-e-Mushtarak, Khayal, Wahm, Hafiza, Mutasarrifah) and external senses (Vision, Audition, Olfaction, Gustation, Tactile).
     - *Quwwat-e-Muharrikah* (Motor / Locomotor Faculty): Volitional muscular contraction and neuromuscular coordination.

The overarching regulatory supreme intelligence of the organism is termed **Tabi'at (Physis / Vis Medicatrix Naturae)**. The physician (*Tabeeb*) is never the primary healer; rather, the physician serves as the humble servant (*Khadim-e-Tabi'at*) who clears obstacles so that the innate Tabi'at can re-establish internal equilibrium.
""",
    "molecular_and_cellular_pathophysiology": """
This tripartite physiological hierarchy matches modern organ-system coordination and neuroendocrine feedback axes:
- **Quwwat-e-Tabi'iyyah**: Maps directly to intermediate metabolism, hepatic glycogenolysis, gluconeogenesis, lipogenesis, urea cycle detoxification, serum albumin synthesis, digestive enteroendocrine peptide release (CCK, GLP-1, Secretin), and cellular anabolic pathways regulated by mTORC1 and insulin-like growth factor 1 (IGF-1).
- **Quwwat-e-Hayawaniyyah**: Correlates with cardiac electrophysiology (sinoatrial node pacemaking, Purkinje fiber conduction), baroreceptor reflex sensitivity, Starling's law of the heart, stroke volume regulation, microvascular capillary perfusion, and cellular oxygen utilization through mitochondrial Complex IV (Cytochrome c oxidase).
- **Quwwat-e-Nafsaniyyah**: Directly corresponds to the central nervous system (CNS), cerebral cortical neuroplasticity, sensory signal transduction, dopaminergic and serotonergic neurotransmission, hippocampal long-term potentiation (LTP), and the efferent corticospinal motor pathway governing voluntary motor units.
""",
    "step_by_step_clinical_examination": """
1. **Evaluation of Quwwat-e-Tabi'iyyah (Metabolic Vigor)**: Assess appetite sensation (*Ishtiha*), post-ingestive comfort, abdominal bloating, bowel transit frequency, and serum albumin/prealbumin levels.
2. **Evaluation of Quwwat-e-Hayawaniyyah (Vital Cardiac Reserve)**: Measure resting heart rate, pulse pressure (Systolic - Diastolic), orthostatic hemodynamic stability (BP change upon standing), and recovery heart rate after 2-minute step challenge.
3. **Evaluation of Quwwat-e-Nafsaniyyah (Cognitive & Neuromuscular Vigor)**: Test mini-mental cognitive status (memory recall, spatial orientation), cranial nerve symmetry, deep tendon reflex latency (patellar, Achilles), and grip dynamometry.
4. **Tabi'at (Homeostatic Resilience) Stress Test**: Assess speed of tissue wound healing, inflammatory resolution post-minor trauma, and recovery latency after mild physical exhaustion.
""",
    "comprehensive_pharmacopeia_and_recipes": """
**Classical Formula: Dawa-ul-Misk Har Motadil (Tri-Organ Vital Tonic)**
- *Indication*: Simultaneous debility of the liver, heart, and brain (*Zof-e-Aaza-e-Raeesa*), post-viral convalescence, profound chronic fatigue syndrome.
- *Formulation Recipe*:
  1. Mushk (Natural musk / Ambrette seed replacement) — 1g
  2. Zafran (Crocus sativus) — 3g
  3. Ambar (Ambergris substitute) — 1g
  4. Ood Saleeb (Paeonia emodi root) — 10g
  5. Darunaj Aqrabi (Doronicum hookeri root) — 10g
  6. Zarambad (Curcuma zedoaria rhizome) — 10g
  7. Gul-e-Surkh (Rosa damascena) — 15g
  8. Marwareed Saeeda (Levigated Pearl micro-powder) — 5g
  9. Shakar Safaid (Refined syrup) — 400g
- *Compounding Protocol*: Micro-pulverize non-volatile herbs. Triturate pearls and saffron in rose water for 6 hours until impalpable. Fold into heated sugar syrup at 105°C, cool to 40°C, then incorporate aromatic resins.
- *Dosage*: 5g twice daily with lukewarm milk or rose-petal infusion.
""",
    "clinical_case_study": """
**Patient**: 56-year-old corporate director presenting with severe multisystem vital exhaustion (*Zof-e-Aaza-e-Raeesa*) 3 months post-severe systemic viral infection. Manifesting cognitive brain fog (*Khadar-e-Dimagh*), exertional palpitations (pulse 98 bpm erratic), sluggish digestion with postprandial gastroparesis, and orthostatic dizziness.
**Investigations**: Baseline HRV (rMSSD): 14ms (severely depressed vagal tone), Fasting Insulin: 18.2 microIU/mL, LFT: ALT 44 U/L, ECG: sinus tachycardia with non-specific ST flattening.
**Integrative Protocol**:
- Pharmacotherapy: *Dawa-ul-Misk Har Motadil* 5g BID + *Khamira Abresham Hakim Arshad Wala* 3g morning fasting + *Arq Gaozaban* 60ml.
- Regimenal Therapy: Gentle *Dalak Laiyin* (effleurage massage) using warm sesame and almond oil along the paraspinal sympathetic chains 3 times weekly.
**Day 30 Outcome**: HRV rMSSD increased from 14ms to 38ms; exertional tachycardia resolved (resting HR 70 bpm); cognitive clarity and memory recall restored; digestive transit normalized to daily morning evacuation.
"""
}

print(f"Volume I completed ({len(TREATISES)} chapters). Generating Volumes II through XII...")
