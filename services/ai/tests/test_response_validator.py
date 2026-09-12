from app.engines.response_validator import REQUIRED_SECTIONS, parse_sections, validate_response_structure
from app.providers.fake_provider import DEFAULT_WELL_FORMED_RESPONSE


def test_well_formed_response_has_no_missing_sections():
    missing = validate_response_structure(DEFAULT_WELL_FORMED_RESPONSE)
    assert missing == []


def test_missing_safety_section_is_detected():
    truncated = DEFAULT_WELL_FORMED_RESPONSE.split("SAFETY\n")[0]
    missing = validate_response_structure(truncated)
    assert "SAFETY" in missing
    assert "POSSIBLE CARE OPTIONS" in missing  # everything after the cut is also missing


def test_missing_clinician_review_required_is_detected():
    truncated = DEFAULT_WELL_FORMED_RESPONSE.replace("\nCLINICIAN REVIEW REQUIRED\n", "\n")
    missing = validate_response_structure(truncated)
    assert "CLINICIAN REVIEW REQUIRED" in missing


def test_empty_response_is_missing_everything():
    missing = validate_response_structure("")
    assert set(missing) == set(REQUIRED_SECTIONS)


def test_parse_sections_extracts_content_under_each_header():
    sections = parse_sections(DEFAULT_WELL_FORMED_RESPONSE)
    assert "chronic fatigue" in sections["CLINICAL SUMMARY"].lower()
    assert "yes" in sections["CLINICIAN REVIEW REQUIRED"].lower()


def test_parse_sections_returns_all_thirteen_when_well_formed():
    sections = parse_sections(DEFAULT_WELL_FORMED_RESPONSE)
    assert set(sections.keys()) == set(REQUIRED_SECTIONS)
