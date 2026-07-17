"""
Stage 2: Dedupe against existing Airtable records.

MVP approach: fuzzy match on title (rapidfuzz) combined with exact/near date
match. Good enough to prove the pipeline; not meant to be bulletproof --
edge cases like "the same event listed with a slightly different date because
last year's flyer got reused" are a known limitation, noted in README.
"""
from src.models import OpportunityItem

def mark_duplicates(
    new_items: list[OpportunityItem],
    existing_records: list[dict],
    threshold: int,
) -> list[OpportunityItem]:
    """
    For each new item, compare against existing_records (from
    airtable_client.fetch_existing_records). If title similarity >= threshold
    AND dates match (or both are None), set is_duplicate=True and
    duplicate_of=<airtable record id>. Returns the same list, mutated in place
    for clarity at the call site.
    """
    raise NotImplementedError
