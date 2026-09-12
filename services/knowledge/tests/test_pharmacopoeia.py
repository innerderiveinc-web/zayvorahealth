from __future__ import annotations

from app.core.pharmacopoeia import (
    get_compound_by_name,
    get_compound_formulations,
    get_mufrad_by_name,
    get_schedule_e1_poisons,
    get_upi_mufradat,
    match_schedule_e1_substance,
)


def test_schedule_e1_poisons_registry_integrity():
    poisons = get_schedule_e1_poisons()
    assert len(poisons) >= 10

    suranjan = poisons.get("suranjan_talkh")
    assert suranjan is not None
    assert suranjan["canonical_name"] == "Suranjan Talkh"
    assert suranjan["mandatory_mudabbar"] is True
    assert suranjan["max_single_dose_mg"] == 250.0
    assert suranjan["max_daily_dose_mg"] == 750.0
    assert any("colchicine" in a.lower() for a in suranjan["toxic_alkaloids"])

    kuchla = poisons.get("kuchla")
    assert kuchla is not None
    assert kuchla["canonical_name"] == "Kuchla"
    assert kuchla["mandatory_mudabbar"] is True
    assert kuchla["max_single_dose_mg"] == 65.0
    assert kuchla["max_daily_dose_mg"] == 125.0

    bhilawa = poisons.get("bhilawa")
    assert bhilawa is not None
    assert "brick" in bhilawa["mudabbar_protocol"].lower()

    afeem = poisons.get("afeem")
    assert afeem is not None
    assert afeem["max_single_dose_mg"] == 30.0

    bhang = poisons.get("bhang")
    assert bhang is not None
    assert bhang["mandatory_mudabbar"] is True


def test_match_schedule_e1_substance_by_synonyms():
    s1 = match_schedule_e1_substance("Colchicum")
    assert s1 is not None
    assert s1["canonical_name"] == "Suranjan Talkh"

    s2 = match_schedule_e1_substance("Nux Vomica")
    assert s2 is not None
    assert s2["canonical_name"] == "Kuchla"

    s3 = match_schedule_e1_substance("Marking Nut")
    assert s3 is not None
    assert s3["canonical_name"] == "Bhilawa"

    s4 = match_schedule_e1_substance("Opium")
    assert s4 is not None
    assert s4["canonical_name"] == "Afeem"

    s5 = match_schedule_e1_substance("Qinnab")
    assert s5 is not None
    assert s5["canonical_name"] == "Bhang"

    assert match_schedule_e1_substance("Sonf") is None


def test_upi_mufradat_registry():
    mufradat = get_upi_mufradat()
    assert len(mufradat) >= 10

    names = {m["name"] for m in mufradat}
    assert "Suranjan Talkh" in names
    assert "Kuchla" in names
    assert "Asgandh" in names
    assert "Zanjabeel" in names
    assert "Filfil Siyah" in names
    assert "Asal-us-Soos" in names
    assert "Sana Makki" in names
    assert "Ustukhuddus" in names

    # Test lookup by name
    asgandh = get_mufrad_by_name("Asgandh")
    assert asgandh is not None
    assert "Withania" in asgandh["botanical_name"]
    assert "dimagh-aasab" in asgandh["organ_axes"]

    # Test lookup by English synonym
    ginger = get_mufrad_by_name("Ginger")
    assert ginger is not None
    assert ginger["name"] == "Zanjabeel"


def test_nfum_compound_formulations_registry():
    compounds = get_compound_formulations()
    assert len(compounds) >= 8

    c_names = {c["name"] for c in compounds}
    assert "Majun Suranjan" in c_names
    assert "Habb-e-Suranjan" in c_names
    assert "Habb-e-Asab" in c_names
    assert "Itrifal Kishneezi" in c_names
    assert "Itrifal Ustukhuddus" in c_names
    assert "Sharbat Bazoori Motadil" in c_names

    majun_suranjan = get_compound_by_name("Majun Suranjan")
    assert majun_suranjan is not None
    assert majun_suranjan["schedule_e1_warning"] is True
    assert any(i["is_schedule_e1"] for i in majun_suranjan["key_ingredients"])

    habb_asab = get_compound_by_name("Habb-e-Asab")
    assert habb_asab is not None
    assert habb_asab["schedule_e1_warning"] is True
    assert "Kuchla Mudabbar" in [i["name"] for i in habb_asab["key_ingredients"]]

    itrifal = get_compound_by_name("Itrifal Kishneezi")
    assert itrifal is not None
    assert itrifal["schedule_e1_warning"] is False
