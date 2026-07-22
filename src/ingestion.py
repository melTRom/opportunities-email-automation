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


# Extension -> kind, plus which source_label prefix to use for that kind.
# Text files are treated like forwarded emails; images/pdfs are treated like
# scanned/photographed flyers. Keyed by lowercase suffix so "FLYER.PDF" still
# matches (people don't always save files with lowercase extensions).
_EXTENSION_MAP: dict[str, tuple[Literal["text", "image", "pdf"], str]] = {
    ".txt": ("text", "email"),
    ".jpg": ("image", "flyer"),
    ".jpeg": ("image", "flyer"),
    ".png": ("image", "flyer"),
    ".pdf": ("pdf", "flyer"),
}


def load_raw_items(input_folder: str) -> list[RawItem]:
    """
    Scan input_folder and return one RawItem per supported file.
    .txt -> "text", .jpg/.jpeg/.png -> "image", .pdf -> "pdf"
    """
    folder = Path(input_folder)

    # A missing folder almost always means a typo'd path or INPUT_FOLDER env
    # var pointing somewhere that was never created. Fail loudly here instead
    # of letting iterdir() raise its own less-obvious FileNotFoundError, so
    # whoever's debugging knows exactly which path was wrong.
    if not folder.is_dir():
        raise FileNotFoundError(
            f"Input folder not found: {folder!s}. "
            f"Create it (or point INPUT_FOLDER at an existing folder) before running ingestion."
        )

    items: list[RawItem] = []
    for entry in folder.iterdir():
        # iterdir() on a non-recursive scan can still return subdirectories
        # (e.g. someone drops a nested folder in there) -- skip those rather
        # than erroring, since we only care about top-level files.
        if not entry.is_file():
            continue

        # Lowercase the suffix so ".JPG"/".PDF" etc. are recognized too --
        # file extensions casing isn't something we want this pipeline to
        # be picky about.
        mapping = _EXTENSION_MAP.get(entry.suffix.lower())
        if mapping is None:
            # Unsupported/unknown files (.gitkeep, .DS_Store, random junk)
            # are expected to show up in a folder people drop files into by
            # hand, so we silently skip them instead of raising.
            continue

        kind, label_prefix = mapping
        items.append(RawItem(path=entry, kind=kind, source_label=f"{label_prefix}:{entry.name}"))

    return items
