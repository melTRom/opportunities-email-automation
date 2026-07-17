"""
Stage 3: Date filtering.

Keep only items whose date is today-or-later (start of this week through the
future). Items with no extractable date are kept but flagged, so a human can
decide during review rather than silently dropping potentially-relevant items.
"""
from datetime import date
from src.models import OpportunityItem


def filter_current_and_future(
    items: list[OpportunityItem], today: date | None = None
) -> list[OpportunityItem]:
    """
    Return items where item.date is None (undated -- kept for manual review)
    or item.date >= start of the current week (Monday). Drops anything
    strictly before that.
    """
    raise NotImplementedError
