import sys
sys.path.insert(0, ".")

# Import what we have so far in build_canonical_treatises.py
with open("scripts/build_canonical_treatises.py", "r") as f:
    existing_code = f.read()

# Let's verify our list of remaining chapters
from services.knowledge.app.data.grand_integrative_library_master import GRAND_INTEGRATIVE_LIBRARY

all_chapters = []
for v in GRAND_INTEGRATIVE_LIBRARY["volumes"]:
    for c in v["chapters"]:
        all_chapters.append((v["id"], c["id"], c["title_en"], c["title_ur"]))

print(f"Total canonical chapters in library: {len(all_chapters)}")
