# services/knowledge/app/routers/diet.py
"""Diet router providing humoral classification for foods.

Endpoint: GET /api/v1/zkb/diet/{food_name}
Returns a JSON payload with the dietary classification (e.g., "hot", "cold", "dry", "wet").
The data is loaded from a CSV file `diet_matrix.csv` located in the same directory (or a shared resources folder).
"""

from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except ImportError:
    class APIRouter:
        def __init__(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
            super().__init__(f"{status_code}: {detail}")

import csv
from pathlib import Path

router = APIRouter(prefix="/api/v1/zkb/diet", tags=["Diet"])

# Load CSV once and cache in memory
_DATA: dict[str, dict] = {}

def _load_data() -> None:
    global _DATA
    if _DATA:
        return
    csv_path = Path(__file__).with_name("diet_matrix.csv")
    if not csv_path.is_file():
        # If the CSV is missing, raise at request time
        return
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Expect a column "food_name" as key
            key = row.get("food_name") or row.get("name")
            if key:
                _DATA[key.lower()] = row

@router.get("/{food_name}")
def get_diet_info(food_name: str):
    _load_data()
    info = _DATA.get(food_name.lower())
    if not info:
        raise HTTPException(status_code=404, detail="Food not found in diet matrix")
    # Return the whole row; callers can pick needed columns
    return info
