# ZAYVORA Health OS™ — Murakkabat Schema Specification

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ZayVoraMurakkabFormulation",
  "type": "object",
  "required": ["id", "name", "category", "key_ingredients", "dose", "analytical_release_specs"],
  "properties": {
    "id": {"type": "string", "description": "Canonical NFUM identifier, e.g. nfum-majun-suranjan"},
    "name": {"type": "string"},
    "urdu_name": {"type": "string"},
    "category": {"type": "string", "enum": ["Majun", "Habb", "Kushta", "Sharbat", "Safuf", "Roghan", "Itrifal"]},
    "classical_indication": {"type": "string"},
    "key_ingredients": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "is_schedule_e1"],
        "properties": {
          "name": {"type": "string"},
          "is_schedule_e1": {"type": "boolean"},
          "ratio": {"type": "number"}
        }
      }
    },
    "dose": {"type": "string"},
    "schedule_e1_warning": {"type": "boolean"},
    "analytical_release_specs": {
      "type": "object",
      "properties": {
        "heavy_metals_ppm": {"type": "object"},
        "microbial_limits": {"type": "object"},
        "total_ash_max_pct": {"type": "number"}
      }
    }
  }
}
```
