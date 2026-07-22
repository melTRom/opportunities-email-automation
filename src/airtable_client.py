"""
Stage 2 support + Stage 5 write-back: Airtable record access.

Expected Airtable table fields (adjust names here if your base differs):
Title, Date, Description, Location, Link, Source

This is currently a LOCAL FILE-BACKED MOCK, not the real Airtable REST API.
We don't have a Personal Access Token yet, so records live in a JSON file
under data/ instead of an actual Airtable base. The function signatures
match what a pyairtable-based implementation would expose, so swapping in
the real client later is a one-file change -- nothing that calls these
functions has to change.

MVP scope: read all existing records once per run for dedupe; write new,
non-duplicate records only after explicit user confirmation in review.py.
"""
import json
from pathlib import Path
from uuid import uuid4

from src.models import OpportunityItem

# Runtime store this module owns (gitignored -- each dev gets their own).
_RUNTIME_PATH = Path("data/mock_airtable.json")
# Read-only starter data a teammate maintains separately; safe if missing.
_SEED_PATH = Path("data/mock_airtable_seed.json")


def _load_records() -> list[dict]:
    """Load records from the runtime file, seeding it from _SEED_PATH on
    first run so the app has starter data without anyone seeding it by hand.
    """
    if not _RUNTIME_PATH.exists():
        seed: list[dict] = []
        if _SEED_PATH.exists():
            seed = json.loads(_SEED_PATH.read_text())
        _save_records(seed)
        return seed
    return json.loads(_RUNTIME_PATH.read_text())


def _save_records(records: list[dict]) -> None:
    _RUNTIME_PATH.write_text(json.dumps(records, indent=2))


def fetch_existing_records(base_id: str, table_name: str, pat: str) -> list[dict]:
    """
    Return all existing records as raw dicts (including a record 'id'),
    used as the comparison set for dedupe.py.

    base_id/table_name/pat are unused by the mock -- accepted anyway so this
    drops in for the real Airtable client later without touching main.py
    or config.py call sites.
    """
    return _load_records()


def write_new_records(
    items: list[OpportunityItem], base_id: str, table_name: str, pat: str
) -> list[str]:
    """
    Write non-duplicate items to the mock store. Only called after review.py
    has gotten explicit confirmation. Returns the list of newly created
    record IDs, in the same order as `items`.

    base_id/table_name/pat are unused by the mock -- see fetch_existing_records.
    """
    records = _load_records()
    new_ids = []
    for item in items:
        # "mock_" prefix makes it obvious in logs/output that this id isn't
        # a real Airtable record id.
        record_id = f"mock_{uuid4().hex[:8]}"
        new_ids.append(record_id)
        records.append(
            {
                "id": record_id,
                "fields": {
                    "Title": item.title,
                    "Date": item.date.isoformat() if item.date else None,
                    "Description": item.description,
                    "Location": item.location,
                    "Link": item.link,
                    "Source": item.source,
                },
            }
        )
    _save_records(records)
    return new_ids
