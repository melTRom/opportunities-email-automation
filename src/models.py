"""
Shared data contract between pipeline stages.

Every stage (extraction -> dedupe -> filter -> template fill -> Airtable
write) passes OpportunityItem objects around, so the JSON schema Claude is
asked to return in extraction.py must match this exactly.
"""
from __future__ import annotations
from datetime import date as date_type
from typing import Optional
from pydantic import BaseModel, Field


class OpportunityItem(BaseModel):
    title: str
    date: Optional[date_type] = Field(
        default=None,
        description="Event date or application deadline. None if not found in source.",
    )
    description: str = ""
    location: str = ""
    link: str = ""
    source: str = Field(
        description="Where this came from, e.g. 'trello', 'email', 'flyer:filename.pdf'"
    )

    # Populated later in the pipeline, not by the extraction call
    airtable_record_id: Optional[str] = Field(
        default=None,
        description="Set if/when this item is matched to or written as an Airtable record.",
    )
    is_duplicate: bool = False
    duplicate_of: Optional[str] = Field(
        default=None, description="Airtable record ID this was matched against, if duplicate."
    )

    class Config:
        # Lets us construct from Claude's raw JSON dict without extra fuss
        extra = "ignore"
