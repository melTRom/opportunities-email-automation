"""
Stage 5: Human review gate.

Nothing gets written to Airtable and no email is considered "final" until
this function returns True. MVP implementation is a terminal prompt; the
interface is kept separate from airtable_client so swapping in a real UI
(Streamlit, Slack approval, etc.) later doesn't touch the write logic.
"""
from src.models import OpportunityItem


def present_for_review(draft_email_text: str, new_items: list[OpportunityItem]) -> bool:
    """
    Display the draft email and the list of new (non-duplicate) items that
    would be written to Airtable. Prompt for explicit y/n confirmation.
    Returns True only on explicit affirmative confirmation.
    """
    raise NotImplementedError
