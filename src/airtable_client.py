"""
Stage 2 support + Stage 5 write-back: Airtable REST access via pyairtable.

Expected Airtable table fields (adjust names here if your base differs):
Title, Date, Description, Location, Link, Source

MVP scope: read all existing records once per run for dedupe; write new,
non-duplicate records only after explicit user confirmation in review.py.
"""
from src.models import OpportunityItem


def fetch_existing_records(base_id: str, table_name: str, pat: str) -> list[dict]:
    """
    Return all existing Airtable records as raw dicts (including Airtable's
    own record 'id'), used as the comparison set for dedupe.py.
    """
    raise NotImplementedError


def write_new_records(
    items: list[OpportunityItem], base_id: str, table_name: str, pat: str
) -> list[str]:
    """
    Write non-duplicate items to Airtable. Only called after review.py has
    gotten explicit confirmation. Returns the list of newly created record IDs.
    """
    raise NotImplementedError
