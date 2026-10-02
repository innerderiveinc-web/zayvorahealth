"""
ZAYVORA Health OS™ - Canonical Substance Identity Service.

Authoritative Single Source of Truth for:
- Mufradat (Single Botanical / Mineral / Animal Drugs)
- Murakkabat (Classical Compound Formulations)
- Schedule E(1) Statutory Poisons (Drugs & Cosmetics Rules 1945)
- Multilingual Synonym Reconciliation (Latin, Unani/Tibbi, Urdu, Arabic, Hindi, English)
- Confusable Species Safety Registry & Adulteration Firewall

Guarantees 100% deterministic resolution across all clinical, therapeutic, and knowledge engines.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SubstanceIdentity:
    canonical_id: str
    canonical_name: str
    canonical_unani_name: str
    botanical_name: str
    family: str
    english_name: str
    urdu_name: str
    arabic_name: Optional[str] = None
    hindi_name: Optional[str] = None
    synonyms: List[str] = field(default_factory=list)
    is_schedule_e1: bool = False
    e1_id: Optional[str] = None
    toxic_alkaloids: List[str] = field(default_factory=list)
    mandatory_mudabbar: bool = False
    mudabbar_protocol: Optional[str] = None
    confusable_with: List[str] = field(default_factory=list)
    confusable_notes: Optional[str] = None
    musleh: Optional[str] = None
    badal: Optional[str] = None
    upi_monograph_ref: Optional[str] = None
    nfum_code: Optional[str] = None
    primary_organ_axis: Optional[str] = None
    default_adult_dose_mg: Optional[float] = None
    max_daily_dose_mg: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "matched": True,
            "canonical_id": self.canonical_id,
            "canonical_name": self.canonical_name,
            "canonical_unani_name": self.canonical_unani_name,
            "botanical_name": self.botanical_name,
            "family": self.family,
            "english_name": self.english_name,
            "urdu_name": self.urdu_name,
            "arabic_name": self.arabic_name,
            "hindi_name": self.hindi_name,
            "synonyms": self.synonyms,
            "is_schedule_e1": self.is_schedule_e1,
            "e1_id": self.e1_id,
            "toxic_alkaloids": self.toxic_alkaloids,
            "mandatory_mudabbar": self.mandatory_mudabbar,
            "mudabbar_protocol": self.mudabbar_protocol,
            "confusable_with": self.confusable_with,
            "confusable_notes": self.confusable_notes,
            "musleh": self.musleh,
            "badal": self.badal,
            "upi_monograph_ref": self.upi_monograph_ref,
            "nfum_code": self.nfum_code,
            "primary_organ_axis": self.primary_organ_axis,
            "default_adult_dose_mg": self.default_adult_dose_mg,
            "max_daily_dose_mg": self.max_daily_dose_mg,
            "status": "RECONCILED",
            "message": f"Canonical identity verified: {self.canonical_id} ({self.canonical_name})"
        }


# Master Catalog of Canonical Single Drugs & Compounds
CANONICAL_CATALOG: Dict[str, SubstanceIdentity] = {
    # ------------------ MUFRADAT (SINGLE DRUGS) ------------------
    "ZMF-001": SubstanceIdentity(
        canonical_id="ZMF-001",
        canonical_name="Ustukhuddus",
        canonical_unani_name="Ustukhuddus",
        botanical_name="Lavandula stoechas L.",
        family="Lamiaceae",
        english_name="Arabian Lavender / French Lavender",
        urdu_name="اسطخودوس",
        arabic_name="اسطوخودوس",
        hindi_name="Dharu / Ustukhuddus",
        synonyms=["ustukhuddus", "lavandula stoechas", "arabian lavender", "french lavender", "ustukhudus", "ustukhudoos", "jarob-e-dimagh"],
        is_schedule_e1=False,
        musleh="Kateera, Lemon Juice, Sharbat-e-Banafsha",
        badal="Aftimoon (Cuscuta reflexa), Banafsha",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 78",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=5000.0,
        max_daily_dose_mg=7000.0,
    ),
    "ZMF-002": SubstanceIdentity(
        canonical_id="ZMF-002",
        canonical_name="Suranjan Talkh",
        canonical_unani_name="Suranjan Talkh",
        botanical_name="Colchicum luteum Baker / Colchicum autumnale L.",
        family="Colchicaceae",
        english_name="Bitter Meadow Saffron / Bitter Colchicum",
        urdu_name="سورنجان تلخ",
        arabic_name="سورنجان مر",
        hindi_name="Kadva Suranjan / Hirantutiya",
        synonyms=["suranjan talkh", "colchicum luteum", "colchicum autumnale", "colchicum", "bitter meadow saffron", "suranjan-e-talkh", "kadva suranjan", "hirantutiya"],
        is_schedule_e1=True,
        e1_id="se1-suranjan-talkh",
        toxic_alkaloids=["Colchicine", "Demecolcine"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Boiled in cow milk for 3 hours, skin peeled, embryonic shoot excised, fried lightly in Almond Oil (Roghan-e-Badam).",
        confusable_with=["ZMF-003"],
        confusable_notes="Do not confuse with ZMF-003 Suranjan Shireen (Sweet Colchicum), which is non-poisonous and lacks colchicine toxicity.",
        musleh="Roghan-e-Badam (Almond Oil), Kateera, Zafran",
        badal="Suranjan Shireen, Bozidana",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 71",
        primary_organ_axis="mafasil",
        default_adult_dose_mg=250.0,
        max_daily_dose_mg=750.0,
    ),
    "ZMF-003": SubstanceIdentity(
        canonical_id="ZMF-003",
        canonical_name="Suranjan Shireen",
        canonical_unani_name="Suranjan Shireen",
        botanical_name="Merendera persica Boiss. / Colchicum autumnale (Sweet var.)",
        family="Colchicaceae",
        english_name="Sweet Colchicum / Sweet Meadow Saffron",
        urdu_name="سورنجان شیریں",
        arabic_name="سورنجان حلو",
        hindi_name="Meetha Suranjan",
        synonyms=["suranjan shireen", "merendera persica", "sweet colchicum", "meetha suranjan", "suranjan shirin"],
        is_schedule_e1=False,
        confusable_with=["ZMF-002"],
        confusable_notes="Must be distinguished from ZMF-002 Suranjan Talkh (Bitter Colchicum), a Schedule E1 poison.",
        musleh="Kateera, Zafran",
        badal="Bozidana, Asgandh",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 72",
        primary_organ_axis="mafasil",
        default_adult_dose_mg=2000.0,
        max_daily_dose_mg=4000.0,
    ),
    "ZMF-004": SubstanceIdentity(
        canonical_id="ZMF-004",
        canonical_name="Qaranfal",
        canonical_unani_name="Qaranfal",
        botanical_name="Syzygium aromaticum (L.) Merr. & L.M.Perry",
        family="Myrtaceae",
        english_name="Clove",
        urdu_name="قرنفل / لونگ",
        arabic_name="قرنفل",
        hindi_name="Laung",
        synonyms=["qaranfal", "clove", "laung", "syzygium aromaticum", "eugenia caryophyllata", "lavang"],
        is_schedule_e1=False,
        musleh="Gond Babool, Sharbat-e-Banafsha",
        badal="Darchini, Kababchini",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 62",
        primary_organ_axis="qalb-urooq",
        default_adult_dose_mg=500.0,
        max_daily_dose_mg=1500.0,
    ),
    "ZMF-005": SubstanceIdentity(
        canonical_id="ZMF-005",
        canonical_name="Asgandh",
        canonical_unani_name="Asgandh",
        botanical_name="Withania somnifera (L.) Dunal",
        family="Solanaceae",
        english_name="Indian Ginseng / Winter Cherry / Ashwagandha",
        urdu_name="اسگندھ",
        arabic_name="عکبر / سم الفراخ",
        hindi_name="Ashwagandha / Asgandh Nagori",
        synonyms=[
            "ashwagandha", "asgandh", "asgand", "withania somnifera", "indian ginseng",
            "winter cherry", "asgand nagori", "punir", "ashvagandha"
        ],
        is_schedule_e1=False,
        musleh="Gond Kateera, Shakkar (Raw Sugar), Cow Ghee",
        badal="Bahman Surkh, Salab Misri, Shatavari",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 05",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=3000.0,
        max_daily_dose_mg=6000.0,
    ),
    "ZMF-006": SubstanceIdentity(
        canonical_id="ZMF-006",
        canonical_name="Filfil Siyah",
        canonical_unani_name="Filfil Siyah",
        botanical_name="Piper nigrum L.",
        family="Piperaceae",
        english_name="Black Pepper",
        urdu_name="فلفل سیاہ / کالی مرچ",
        arabic_name="فلفل اسود",
        hindi_name="Kali Mirch",
        synonyms=["filfil siah", "filfil siyah", "black pepper", "piper nigrum", "kali mirch", "maricha"],
        is_schedule_e1=False,
        musleh="Roghan-e-Zaitoon (Olive Oil), Fresh Milk, Honey",
        badal="Zanjabeel, Peepal (Piper longum)",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 23",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=500.0,
        max_daily_dose_mg=1500.0,
    ),
    "ZMF-007": SubstanceIdentity(
        canonical_id="ZMF-007",
        canonical_name="Zanjabeel",
        canonical_unani_name="Zanjabeel",
        botanical_name="Zingiber officinale Roscoe",
        family="Zingiberaceae",
        english_name="Ginger / Dried Ginger (Sonth)",
        urdu_name="زنجبیل / سونٹھ",
        arabic_name="زنجبيل",
        hindi_name="Adrak / Sonth",
        synonyms=["zanjabeel", "ginger", "sonth", "zingiber officinale", "adrak", "shunthi", "sunth"],
        is_schedule_e1=False,
        musleh="Roghan-e-Badam, Honey",
        badal="Darfulful, Peepal, Filfil Safed",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 79",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=1500.0,
        max_daily_dose_mg=3000.0,
    ),
    "ZMF-013": SubstanceIdentity(
        canonical_id="ZMF-013",
        canonical_name="Zafran",
        canonical_unani_name="Zafran",
        botanical_name="Crocus sativus L.",
        family="Iridaceae",
        english_name="Saffron",
        urdu_name="زعفران / کیسر",
        arabic_name="زعفران",
        hindi_name="Kesar / Kumkum",
        synonyms=["zafran", "kesar", "saffron", "crocus sativus", "kumkum", "zaafraan"],
        is_schedule_e1=False,
        musleh="Aanisoon, Sekanjabeen",
        badal="Qust Shireen, Asaroon",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 76",
        primary_organ_axis="qalb-urooq",
        default_adult_dose_mg=250.0,
        max_daily_dose_mg=1000.0,
    ),
    "ZMF-014": SubstanceIdentity(
        canonical_id="ZMF-014",
        canonical_name="Asaroon",
        canonical_unani_name="Asaroon",
        botanical_name="Asarum europaeum L.",
        family="Aristolochiaceae",
        english_name="Asarabacca / Wild Nard / Hazelwort",
        urdu_name="اسارون",
        arabic_name="اسارون",
        hindi_name="Tagar Ganth / Asaroon",
        synonyms=["asaroon", "asaron", "asarum europaeum", "wild nard", "asarabacca", "hazelwort"],
        is_schedule_e1=False,
        confusable_with=["ZMF-015"],
        confusable_notes="CRITICAL SAFETY ADVISORY: Frequently confused or illicitly substituted in commercial markets with Tagar (Valeriana wallichii / ZMF-015). True Asaroon belongs to Aristolochiaceae and requires screening for aristolochic acid nephrotoxicity.",
        musleh="Gul-e-Surkh (Rose petals), Sharbat-e-Banafsha",
        badal="Zafran, Qaranfal, Tagar (under clinical control)",
        upi_monograph_ref="UPI Part I, Vol. II, Entry 08",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=1000.0,
        max_daily_dose_mg=3000.0,
    ),
    "ZMF-015": SubstanceIdentity(
        canonical_id="ZMF-015",
        canonical_name="Tagar",
        canonical_unani_name="Tagar",
        botanical_name="Valeriana wallichii DC. / Valeriana jatamansi Jones",
        family="Caprifoliaceae",
        english_name="Indian Valerian",
        urdu_name="تگر / مشک بالا",
        arabic_name="سنبل بری / تگر",
        hindi_name="Tagar / Sugandhabala",
        synonyms=["tagar", "valeriana wallichii", "valeriana jatamansi", "indian valerian", "mushk bala", "sugandhabala"],
        is_schedule_e1=False,
        confusable_with=["ZMF-014"],
        confusable_notes="Tagar (Valeriana wallichii) contains sedative valepotriates and is non-nephrotoxic. Must not be blindly conflated with Asaroon (Asarum europaeum / ZMF-014).",
        musleh="Amla, Sekanjabeen",
        badal="Ustukhuddus, Sumbul-ut-Teeb",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 74",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=1500.0,
        max_daily_dose_mg=3000.0,
    ),
    "ZMF-016": SubstanceIdentity(
        canonical_id="ZMF-016",
        canonical_name="Halela Siyah",
        canonical_unani_name="Halela Siyah",
        botanical_name="Terminalia chebula Retz. (immature fruit)",
        family="Combretaceae",
        english_name="Black Myrobalan / Chebulic Myrobalan",
        urdu_name="ہلیلہ سیاہ / ہرڑ",
        arabic_name="اهليلج اسود",
        hindi_name="Harad / Kali Harad",
        synonyms=["halela siah", "halela siyah", "terminalia chebula", "black myrobalan", "kali harad", "harad", "chebulic myrobalan", "haritaki"],
        is_schedule_e1=False,
        musleh="Roghan-e-Badam, Cow Ghee",
        badal="Amla, Balela",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 31",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=3000.0,
        max_daily_dose_mg=5000.0,
    ),
    "ZMF-090": SubstanceIdentity(
        canonical_id="ZMF-090",
        canonical_name="Kuchla",
        canonical_unani_name="Azaraqi / Kuchla",
        botanical_name="Strychnos nux-vomica L.",
        family="Loganiaceae",
        english_name="Poison Nut / Nux Vomica",
        urdu_name="کچلہ / اذراقی",
        arabic_name="جوز القیء / اذراقی",
        hindi_name="Kuchla / Vishamusti",
        synonyms=["kuchla", "azaraqi", "azaragi", "strychnos nux-vomica", "nux vomica", "poison nut", "vishatinduka", "vishamusti"],
        is_schedule_e1=True,
        e1_id="se1-kuchla",
        toxic_alkaloids=["Strychnine", "Brucine"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Soaked in fresh cow milk or Triphala decoction for 7 days with daily liquid change; outer testa scraped, embryonic shoot excised, fried in Cow Ghee until yellowish-brown.",
        confusable_with=["ZMF-091"],
        confusable_notes="Schedule E1 spinal convulsant poison. Toxic dose produces hyperreflexia and tetanic spasms. Must never be prescribed without certified Tadbir.",
        musleh="Roghan-e-Zard (Cow Ghee), Sheer-e-Taza (Milk), Anisoon",
        badal="Jadwar Khatai, Asgandh",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 42",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=50.0,
        max_daily_dose_mg=125.0,
    ),
    "ZMF-096": SubstanceIdentity(
        canonical_id="ZMF-096",
        canonical_name="Asl-us-Soos",
        canonical_unani_name="Asl-us-Soos",
        botanical_name="Glycyrrhiza glabra L.",
        family="Fabaceae",
        english_name="Liquorice / Licorice / Sweet Root",
        urdu_name="اصل السوس / ملٹھی",
        arabic_name="عرق السوس",
        hindi_name="Mulethi / Yashtimadhu",
        synonyms=[
            "mulethi", "mulathi", "liquorice", "licorice", "asl-us-soos", "asl-ul-soos",
            "glycyrrhiza glabra", "sweet root", "yashtimadhu", "jethimadh", "asal-us-soos"
        ],
        is_schedule_e1=False,
        musleh="Gul-e-Surkh (Rose petals), Kateera",
        badal="Kateera, Samagh-e-Arabi",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 10",
        primary_organ_axis="riya-sadr",
        default_adult_dose_mg=3000.0,
        max_daily_dose_mg=5000.0,
    ),
    "ZMF-101": SubstanceIdentity(
        canonical_id="ZMF-101",
        canonical_name="Bhilawa",
        canonical_unani_name="Bhilawa / Baladur",
        botanical_name="Semecarpus anacardium L.f.",
        family="Anacardiaceae",
        english_name="Marking Nut",
        urdu_name="بھلاواں / بلاذر",
        arabic_name="حب الفہم / بلاذر",
        hindi_name="Bhilawa / Bhallataka",
        synonyms=["bhilawa", "baladur", "semecarpus anacardium", "marking nut", "bhallataka"],
        is_schedule_e1=True,
        e1_id="se1-bhilawa",
        toxic_alkaloids=["Bhilawanol", "Anacardic Acid", "Carbophenol"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Receptacle excised, pericarp cut, boiled in Brick Dust (Khisht-e-Pukhta) / Cow Urine for 6 hours, washed in warm water, dried.",
        musleh="Gond Babool, Roghan-e-Kunjad (Sesame Oil), Fresh Butter",
        badal="Balela, Kundur",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 14",
        primary_organ_axis="mafasil",
        default_adult_dose_mg=125.0,
        max_daily_dose_mg=250.0,
    ),
    "ZMF-102": SubstanceIdentity(
        canonical_id="ZMF-102",
        canonical_name="Afeem",
        canonical_unani_name="Afeem / Afyoon",
        botanical_name="Papaver somniferum L.",
        family="Papaveraceae",
        english_name="Opium Poppy Latex",
        urdu_name="افیون",
        arabic_name="افیون",
        hindi_name="Afeem / Ahiphena",
        synonyms=["afeem", "afyoon", "opium", "papaver somniferum", "ahiphena"],
        is_schedule_e1=True,
        e1_id="se1-afeem",
        toxic_alkaloids=["Morphine", "Codeine", "Thebaine", "Noscapine"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Dissolved in fresh goat milk, strained through fine cloth 7 times, slowly evaporated to mass.",
        musleh="Jund-e-Bedastar, Zafran, Filfil Siyah",
        badal="Bazrulbanj, Post-e-Khashkhash",
        upi_monograph_ref="UPI Part I, Vol. II, Entry 02",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=30.0,
        max_daily_dose_mg=65.0,
    ),
    "ZMF-103": SubstanceIdentity(
        canonical_id="ZMF-103",
        canonical_name="Bhang",
        canonical_unani_name="Bhang / Qinnab",
        botanical_name="Cannabis sativa L.",
        family="Cannabaceae",
        english_name="Indian Hemp / Cannabis",
        urdu_name="بھنگ / ورق الخیال",
        arabic_name="قنب / ورق الخیال",
        hindi_name="Bhang / Vijaya",
        synonyms=["bhang", "qinnab", "cannabis sativa", "hemp", "vijaya", "ganja"],
        is_schedule_e1=True,
        e1_id="se1-bhang",
        toxic_alkaloids=["Delta-9-THC", "Cannabinol"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Boiled in cow milk for 3 hours with Babool leaves, washed in warm water, dried and fried in Cow Ghee.",
        musleh="Roghan-e-Zard, Roghan-e-Pista, Honey",
        badal="Post-e-Khashkhash, Kishneez Khushk",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 16",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=250.0,
        max_daily_dose_mg=500.0,
    ),
    "ZMF-104": SubstanceIdentity(
        canonical_id="ZMF-104",
        canonical_name="Dhatura",
        canonical_unani_name="Jouz-masil / Dhatura",
        botanical_name="Datura metel L. / Datura stramonium L.",
        family="Solanaceae",
        english_name="Thorn Apple / Datura",
        urdu_name="دھتورہ / جوز ماثل",
        arabic_name="جوز ماثل",
        hindi_name="Dhatura",
        synonyms=["dhatura", "jouz masil", "datura metel", "datura stramonium", "thorn apple"],
        is_schedule_e1=True,
        e1_id="se1-dhatura",
        toxic_alkaloids=["Scopolamine (Hyoscine)", "Hyoscyamine", "Atropine"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Seeds soaked in cow milk, boiled until milk evaporates, washed in warm water and peeled.",
        musleh="Roghan-e-Badam, Sheer-e-Taza, Honey",
        badal="Bazrulbanj, Afyoon",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 20",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=30.0,
        max_daily_dose_mg=60.0,
    ),
    "ZMF-105": SubstanceIdentity(
        canonical_id="ZMF-105",
        canonical_name="Jamalgota",
        canonical_unani_name="Habb-us-Salateen / Jamalgota",
        botanical_name="Croton tiglium L.",
        family="Euphorbiaceae",
        english_name="Purging Croton",
        urdu_name="جمال گوٹہ / حب السلاطین",
        arabic_name="حب السلاطین",
        hindi_name="Jamalgota / Jayapala",
        synonyms=["jamalgota", "habb-us-salateen", "croton tiglium", "purging croton", "jayapala"],
        is_schedule_e1=True,
        e1_id="se1-jamalgota",
        toxic_alkaloids=["Crotonoside", "Phorbol Esters", "Crotin (Toxalbumin)"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Outer shell peeled, cotyledonary embryo completely excised, boiled in Cow Milk wrapped in Dol yantra, fried lightly in Cow Ghee.",
        musleh="Kishneez Khushk, Buttermilk, Roghan-e-Badam",
        badal="Turbud, Saqmooniya",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 26",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=30.0,
        max_daily_dose_mg=60.0,
    ),
    "ZMF-106": SubstanceIdentity(
        canonical_id="ZMF-106",
        canonical_name="Bish",
        canonical_unani_name="Bish / Meetha Zehar",
        botanical_name="Aconitum chasmanthum Stapf ex Holmes / Aconitum ferox",
        family="Ranunculaceae",
        english_name="Indian Aconite / Monkshood",
        urdu_name="بیش / میٹھا زہر",
        arabic_name="بیش / خانق الذئب",
        hindi_name="Vatsanabha / Bachnag",
        synonyms=["bish", "meetha zehar", "aconitum chasmanthum", "aconitum ferox", "monkshood", "vatsanabha", "bachnag"],
        is_schedule_e1=True,
        e1_id="se1-bish",
        toxic_alkaloids=["Aconitine", "Mesoaconitine", "Hypaconitine"],
        mandatory_mudabbar=True,
        mudabbar_protocol="Steeped in Cow Urine (Gomutra) for 7 days under direct sunlight, boiled in Cow Milk for 3 hours, outer cortex scraped off.",
        musleh="Roghan-e-Badam, Roghan-e-Zard, Sheer-e-Taza, Jadwar Khatai",
        badal="Jadwar, Asgandh",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 15",
        primary_organ_axis="dimagh-aasab",
        default_adult_dose_mg=15.0,
        max_daily_dose_mg=30.0,
    ),
    "ZMF-107": SubstanceIdentity(
        canonical_id="ZMF-107",
        canonical_name="Chiraita",
        canonical_unani_name="Chiraita Shireen",
        botanical_name="Swertia chirata Buch.-Ham. ex C.B.Clarke",
        family="Gentianaceae",
        english_name="Chiretta / Indian Bitter",
        urdu_name="چرائتہ شیریں",
        arabic_name="قصب الذريرة",
        hindi_name="Chirayata",
        synonyms=["chiraita", "chirayata", "swertia chirata", "chiretta", "kiratatikta"],
        is_schedule_e1=False,
        confusable_with=["ZMF-108"],
        confusable_notes="Frequently substituted by Kalmegh (Andrographis paniculata / ZMF-108). While both are potent bitter tonics, Swertia chirata belongs to Gentianaceae (Amarogentin) whereas Andrographis belongs to Acanthaceae (Andrographolide).",
        musleh="Anisoon, Sharbat-e-Banafsha",
        badal="Kalmegh (under authorized substitution), Afsanteen",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 18",
        primary_organ_axis="jigar-tihal",
        default_adult_dose_mg=3000.0,
        max_daily_dose_mg=6000.0,
    ),
    "ZMF-108": SubstanceIdentity(
        canonical_id="ZMF-108",
        canonical_name="Kalmegh",
        canonical_unani_name="Kalmegh",
        botanical_name="Andrographis paniculata (Burm.f.) Nees",
        family="Acanthaceae",
        english_name="Green Chiretta / King of Bitters",
        urdu_name="کالمیکھ",
        arabic_name="قصب الزعفران",
        hindi_name="Kalmegh / Bhunimba",
        synonyms=["kalmegh", "andrographis paniculata", "green chiretta", "king of bitters", "bhunimba"],
        is_schedule_e1=False,
        confusable_with=["ZMF-107"],
        confusable_notes="Often traded as substitute for Chiraita (ZMF-107). Distinct botanical chemistry (Andrographolide).",
        musleh="Roghan-e-Badam, Honey",
        badal="Chiraita",
        upi_monograph_ref="UPI Part I, Vol. II, Entry 15",
        primary_organ_axis="jigar-tihal",
        default_adult_dose_mg=2000.0,
        max_daily_dose_mg=4000.0,
    ),
    "ZMF-109": SubstanceIdentity(
        canonical_id="ZMF-109",
        canonical_name="Sana Makki",
        canonical_unani_name="Sana Makki",
        botanical_name="Cassia angustifolia Vahl / Senna alexandrina Mill.",
        family="Fabaceae",
        english_name="Alexandrian Senna / Tinnevelly Senna",
        urdu_name="سنا مکی",
        arabic_name="سنا مكي",
        hindi_name="Sanay",
        synonyms=["sana makki", "senna", "cassia angustifolia", "senna alexandrina", "sanay", "swarnapatri"],
        is_schedule_e1=False,
        musleh="Anisoon, Gulqand, Roghan-e-Badam",
        badal="Turbud Safed, Halela Zard",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 68",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=4000.0,
        max_daily_dose_mg=8000.0,
    ),
    "ZMF-110": SubstanceIdentity(
        canonical_id="ZMF-110",
        canonical_name="Kalonji",
        canonical_unani_name="Kalonji / Habba Sauda",
        botanical_name="Nigella sativa L.",
        family="Ranunculaceae",
        english_name="Black Cumin / Black Seed / Nigella",
        urdu_name="کلونجی / حبة السوداء",
        arabic_name="حبة السوداء / شونیز",
        hindi_name="Kalonji",
        synonyms=["kalonji", "habba sauda", "nigella sativa", "black seed", "black cumin", "shuneez", "upakunchika"],
        is_schedule_e1=False,
        musleh="Sirka (Vinegar), Roghan-e-Kunjad, Kateera",
        badal="Zeera Siyah",
        upi_monograph_ref="UPI Part I, Vol. I, Entry 43",
        primary_organ_axis="meda-amaa",
        default_adult_dose_mg=2000.0,
        max_daily_dose_mg=4000.0,
    ),
}

# Auto-enrich catalog from 350 Gold Benchmark monographs
try:
    from services.knowledge.app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
except ImportError:
    try:
        from app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
    except ImportError:
        GOLD_BENCHMARK_25_MONOGRAPHS = {}

for zid, mono in GOLD_BENCHMARK_25_MONOGRAPHS.items():
    if zid in CANONICAL_CATALOG:
        continue
    c_ident = mono.get("canonical_identity", {})
    c_prof = mono.get("classical_profile", {})
    s_fire = mono.get("safety_firewall", {})
    m_evid = mono.get("modern_evidence", {})
    p_cross = mono.get("pharmacopoeial_crosswalk", {})

    can_name = c_ident.get("canonical_unani_name") or zid
    is_e1 = s_fire.get("is_schedule_e1", False)
    tadbeer = c_prof.get("tadbeer", "")
    mand_mudabbar = is_e1 or bool(tadbeer and "purification" in tadbeer.lower())

    musleh_raw = c_prof.get("musleh", "")
    musleh_s = ", ".join(musleh_raw) if isinstance(musleh_raw, list) else str(musleh_raw or "")
    badal_raw = c_prof.get("badal", "")
    badal_s = ", ".join(badal_raw) if isinstance(badal_raw, list) else str(badal_raw or "")

    aff_list = mono.get("organ_axis_affinity", [])
    primary_axis = aff_list[0].lower().replace(" ", "-") if aff_list else "tabiyat"

    syn_list = list(c_ident.get("synonyms", []))
    if c_ident.get("hindi_regional_names"):
        syn_list.extend(c_ident.get("hindi_regional_names"))

    CANONICAL_CATALOG[zid] = SubstanceIdentity(
        canonical_id=zid,
        canonical_name=can_name,
        canonical_unani_name=can_name,
        botanical_name=c_ident.get("botanical_name", ""),
        family=c_ident.get("family", ""),
        english_name=c_ident.get("canonical_english_name", can_name),
        urdu_name=c_ident.get("urdu_name", can_name),
        arabic_name=c_ident.get("arabic_name"),
        hindi_name=c_ident.get("hindi_name"),
        synonyms=syn_list,
        is_schedule_e1=is_e1,
        e1_id=f"se1-{zid.lower()}" if is_e1 else None,
        mandatory_mudabbar=mand_mudabbar,
        mudabbar_protocol=tadbeer if mand_mudabbar else None,
        musleh=musleh_s,
        badal=badal_s,
        upi_monograph_ref=p_cross.get("upi_monograph_citation"),
        nfum_code=p_cross.get("nfum_reference"),
        primary_organ_axis=primary_axis,
        default_adult_dose_mg=3000.0,
        max_daily_dose_mg=s_fire.get("maximum_daily_ceiling_mg", 6000.0)
    )


# Pre-indexed normalized lookups with priority reservation for core authoritative monographs
NORMALIZED_SYNONYM_LOOKUP: Dict[str, str] = {}

CORE_AUTHORITATIVE_IDS = {
    "ZMF-001", "ZMF-002", "ZMF-003", "ZMF-004", "ZMF-005", "ZMF-006", "ZMF-007",
    "ZMF-013", "ZMF-014", "ZMF-015", "ZMF-016", "ZMF-090", "ZMF-096", "ZMF-101",
    "ZMF-102", "ZMF-103", "ZMF-104", "ZMF-105", "ZMF-106", "ZMF-107", "ZMF-108",
    "ZMF-109", "ZMF-110"
}

def _index_substance_entry(cid: str, sub: SubstanceIdentity, is_priority: bool):
    keys = [
        cid.lower(),
        sub.canonical_name.lower(),
        sub.canonical_unani_name.lower(),
        sub.botanical_name.lower(),
        sub.english_name.lower()
    ]
    if sub.hindi_name:
        keys.append(sub.hindi_name.lower())
    for syn in sub.synonyms:
        if syn and syn.strip():
            keys.append(syn.strip().lower())

    for k in keys:
        if is_priority or k not in NORMALIZED_SYNONYM_LOOKUP:
            NORMALIZED_SYNONYM_LOOKUP[k] = cid

# First index core authoritative entries
for cid in CORE_AUTHORITATIVE_IDS:
    if cid in CANONICAL_CATALOG:
        _index_substance_entry(cid, CANONICAL_CATALOG[cid], is_priority=True)

# Next index the remaining entries without overwriting core synonyms
for cid, sub in CANONICAL_CATALOG.items():
    if cid not in CORE_AUTHORITATIVE_IDS:
        _index_substance_entry(cid, sub, is_priority=False)



class CanonicalSubstanceIdentityService:
    """Authoritative reconciliation and validation service for Unani substances."""

    @classmethod
    def normalize_query(cls, text: str) -> str:
        """Strip punctuation and extraneous whitespace for deterministic comparison."""
        cleaned = re.sub(r"[^\w\s-]", " ", text)
        return " ".join(cleaned.lower().split())

    @classmethod
    def resolve_substance(cls, query: str) -> Dict[str, Any]:
        """
        Reconciles any input name (botanical, Latin, Urdu, Arabic, Hindi, English, or catalog ID)
        to the authoritative Canonical Substance Identity.
        """
        if not query or not query.strip():
            return {
                "matched": False,
                "query": query,
                "status": "INVALID_INPUT",
                "message": "Substance query cannot be empty."
            }

        norm = cls.normalize_query(query)

        # 1. Exact match in normalized synonym lookup
        if norm in NORMALIZED_SYNONYM_LOOKUP:
            canonical_id = NORMALIZED_SYNONYM_LOOKUP[norm]
            return CANONICAL_CATALOG[canonical_id].to_dict()

        # 2. Check if raw query directly matches (e.g. catalog ID ZMF-005)
        raw_upper = query.strip().upper()
        if raw_upper in CANONICAL_CATALOG:
            return CANONICAL_CATALOG[raw_upper].to_dict()

        # 3. Substring matching across indexed synonyms
        for syn, cid in NORMALIZED_SYNONYM_LOOKUP.items():
            # If the normalized query is contained in synonym or vice versa (for multi-word match)
            if len(norm) >= 4 and (norm == syn or norm in syn or syn in norm):
                return CANONICAL_CATALOG[cid].to_dict()

        # 4. Fallback: Check botanical / binomial matches (e.g. "Withania" or "somnifera")
        for cid, sub in CANONICAL_CATALOG.items():
            botanical_parts = sub.botanical_name.lower().split()
            for part in botanical_parts:
                if len(part) >= 5 and part in norm:
                    return sub.to_dict()

        return {
            "matched": False,
            "query": query,
            "canonical_id": None,
            "status": "RECONCILIATION_REQUIRED",
            "message": f"No canonical substance identity verified for '{query}'. Pending taxonomy board review."
        }

    @classmethod
    def is_confusable(cls, substance_a: str, substance_b: str) -> Tuple[bool, str]:
        """
        Evaluates whether two substances have known commercial confusion or adulteration risk.
        Returns (is_confusable, advisory_rationale).
        """
        res_a = cls.resolve_substance(substance_a)
        res_b = cls.resolve_substance(substance_b)

        if not res_a.get("matched") or not res_b.get("matched"):
            return False, "One or both substances could not be resolved to canonical catalog."

        id_a = res_a["canonical_id"]
        id_b = res_b["canonical_id"]

        sub_a = CANONICAL_CATALOG[id_a]
        if id_b in sub_a.confusable_with:
            notes = sub_a.confusable_notes or f"Confusion risk between {sub_a.canonical_name} and {id_b}."
            return True, notes

        sub_b = CANONICAL_CATALOG[id_b]
        if id_a in sub_b.confusable_with:
            notes = sub_b.confusable_notes or f"Confusion risk between {sub_b.canonical_name} and {id_a}."
            return True, notes

        return False, "No known classical or regulatory confusion registered between these substances."

    @classmethod
    def get_canonical_metadata(cls, canonical_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves structured metadata by canonical ID."""
        cid = canonical_id.strip().upper()
        if cid in CANONICAL_CATALOG:
            return CANONICAL_CATALOG[cid].to_dict()
        return None

    @classmethod
    def list_all_canonical_substances(cls) -> List[Dict[str, Any]]:
        """Returns all registered canonical substances."""
        return [sub.to_dict() for sub in CANONICAL_CATALOG.values()]
