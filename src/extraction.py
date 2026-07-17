"""
Stage 1b: Extraction.

One Claude API call per RawItem, returning JSON matching OpportunityItem.
- text items: sent as a plain text message
- image items (.jpg/.jpeg/.png): sent as a base64 image content block
- pdf items: sent as a base64 document content block (Claude reads PDFs
  natively -- no need to rasterize pages ourselves)

All three cases share one prompt asking for the same JSON schema, so the
rest of the pipeline never has to know which input type an item came from.
"""
from src.ingestion import RawItem
from src.models import OpportunityItem

EXTRACTION_SYSTEM_PROMPT = """\
You extract structured opportunity/event data for a university CS department's
weekly student newsletter. Given a flyer, forwarded email, or note, return ONLY
a JSON object (no markdown fences, no commentary) with exactly these fields:

title (string), date (YYYY-MM-DD or null if no date/deadline is stated),
description (1-2 sentence summary, string), location (string, "" if unknown),
link (string, "" if unknown).

If the source is ambiguous or missing a field, use your best judgment and
leave the field empty/null rather than inventing details.
"""


def extract_item(raw_item: RawItem, model: str) -> OpportunityItem:
    """
    Build the appropriate multimodal message for raw_item.kind, call the
    Anthropic API once, parse the JSON response, and return an OpportunityItem
    with `source` set from raw_item.source_label.
    """
    raise NotImplementedError


def extract_all(raw_items: list[RawItem], model: str) -> list[OpportunityItem]:
    """Run extract_item over every raw item. Should not raise on a single
    item's failure -- log it and skip, so one bad flyer doesn't kill the run."""
    raise NotImplementedError
