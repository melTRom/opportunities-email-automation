"""
Stage 1a: Ingestion.

MVP scope: read from a local folder instead of live Trello/Gmail APIs.
Each file in INPUT_FOLDER becomes one "raw item" to send to extraction.

Real integrations (Trello API, Gmail API, Airtable-as-source-of-truth for
already-seen items) are out of scope for today but this function's return
shape is designed so swapping the source later doesn't change anything
downstream.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class RawItem:
    path: Path
    kind: Literal["text", "image", "pdf"]
    source_label: str  # e.g. "email", "flyer:workshop.pdf" -- goes into OpportunityItem.source


def load_raw_items(input_folder: str) -> list[RawItem]:
    """
    Scan input_folder and return one RawItem per supported file.
    .txt -> "text", .jpg/.jpeg/.png -> "image", .pdf -> "pdf"
    """
    raise NotImplementedError
