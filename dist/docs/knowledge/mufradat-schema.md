# ZAYVORA Health OS™ — Mufradat Schema Specification

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ZayVoraMufradMonograph",
  "type": "object",
  "required": ["id", "name", "botanical_name", "mizaj", "dose", "is_schedule_e1"],
  "properties": {
    "id": {"type": "string", "description": "Canonical UPI identifier, e.g. upi-suranjan-talkh"},
    "name": {"type": "string", "description": "Canonical Unani name"},
    "botanical_name": {"type": "string", "description": "Accepted binomial nomenclature"},
    "part_used": {"type": "string"},
    "synonyms": {"type": "array", "items": {"type": "string"}},
    "afal": {"type": "array", "items": {"type": "string"}, "description": "Classical actions"},
    "mizaj": {
      "type": "object",
      "required": ["temperament", "quality", "hc_degree", "wd_degree"],
      "properties": {
        "temperament": {"type": "string", "enum": ["Damwi", "Safrawi", "Balghami", "Saudawi", "Motadil"]},
        "quality": {"type": "string"},
        "hc_degree": {"type": "integer", "minimum": 1, "maximum": 4},
        "wd_degree": {"type": "integer", "minimum": 1, "maximum": 4}
      }
    },
    "organ_axes": {"type": "array", "items": {"type": "string"}},
    "musleh": {"type": "string", "description": "Classical corrective"},
    "badal": {"type": "string", "description": "Classical substitute"},
    "dose": {"type": "string", "description": "Statutory therapeutic dose range"},
    "is_schedule_e1": {"type": "boolean"},
    "mandatory_mudabbar": {"type": "boolean"},
    "mudabbar_protocol": {"type": "string"},
    "wfo_id": {"type": "string", "description": "World Flora Online identifier"},
    "powo_id": {"type": "string", "description": "Plants of the World Online LSID"}
  }
}
```
