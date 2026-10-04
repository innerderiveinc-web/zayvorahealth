#!/usr/bin/env python3
"""
ZAYVORA Health OS — Grand Integrative Medical Library Engine Builder
Builds the complete enriched Grand Library (12 Volumes, 250 Mufradat, 59 Murakkabat, CYP450 Interactions)
and compiles it into js/modules/05-grand-library.js and js/zayvora-core.js.
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.knowledge.app.data.grand_integrative_library_master import (
    GRAND_INTEGRATIVE_LIBRARY,
    LIBRARY_METADATA,
    MUFRADAT_LIST,
    MURAKKABAT_LIST,
    DRUG_INTERACTIONS_LIST,
    UNIVERSAL_CONTRAINDICATIONS_LIST
)

print(f"Loaded {len(GRAND_INTEGRATIVE_LIBRARY['volumes'])} volumes, {len(MUFRADAT_LIST)} mufradat, {len(MURAKKABAT_LIST)} murakkabat, {len(DRUG_INTERACTIONS_LIST)} drug interactions.")

# Build master library data dictionary
master_data = {
    "metadata": LIBRARY_METADATA,
    "volumes": GRAND_INTEGRATIVE_LIBRARY["volumes"],
    "mufradat": MUFRADAT_LIST,
    "murakkabat": MURAKKABAT_LIST,
    "drug_interactions": DRUG_INTERACTIONS_LIST,
    "universal_contraindications": UNIVERSAL_CONTRAINDICATIONS_LIST
}

library_json_str = json.dumps(master_data, ensure_ascii=False)
print(f"Serialized master data size: {len(library_json_str)/1024:.1f} KB")

