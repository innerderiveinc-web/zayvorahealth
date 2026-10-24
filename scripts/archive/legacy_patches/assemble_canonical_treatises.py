import sys
import os
sys.path.insert(0, ".")

from scripts.treatises_part1 import PART1_TREATISES
from scripts.treatises_part2 import PART2_TREATISES
from scripts.treatises_part3 import PART3_TREATISES
from scripts.treatises_part4 import PART4_TREATISES

ALL_TREATISES = {}
ALL_TREATISES.update(PART1_TREATISES)
ALL_TREATISES.update(PART2_TREATISES)
ALL_TREATISES.update(PART3_TREATISES)
ALL_TREATISES.update(PART4_TREATISES)

print(f"Total merged treatises: {len(ALL_TREATISES)}")

output_file = "services/knowledge/app/data/canonical_treatises.py"
with open(output_file, "w", encoding="utf-8") as f:
    f.write('"""\nZAYVORA Health OS — Canonical Academic Treatises (Layer 2)\n'
            'Exhaustive scholarly medical treatises covering the 12 Master Volumes and 38 Chapters.\n"""\n\n')
    f.write("CANONICAL_TREATISES = {\n")
    for ch_id, data in ALL_TREATISES.items():
        f.write(f"    {repr(ch_id)}: {{\n")
        for k, v in data.items():
            f.write(f"        {repr(k)}: {repr(v)},\n")
        f.write("    },\n")
    f.write("}\n\n")
    f.write("def get_treatise(chapter_id: str) -> dict:\n")
    f.write("    return CANONICAL_TREATISES.get(chapter_id)\n")

print(f"Successfully generated {output_file}. File size: {os.path.getsize(output_file)} bytes.")
