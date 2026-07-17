"""
Centralized configuration. Every other module imports from here instead of
calling os.getenv() directly, so there's one place that knows about env vars
and one place that fails loudly if something required is missing.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root if present; real env vars still win


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.example to .env and fill it in."
        )
    return value


# --- Anthropic ---
ANTHROPIC_API_KEY = _require("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")

# --- Airtable ---
AIRTABLE_PAT = _require("AIRTABLE_PAT")
AIRTABLE_BASE_ID = _require("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Opportunities")

# --- Pipeline ---
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "data/sample_inputs")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output/drafts")
DEDUPE_THRESHOLD = int(os.getenv("DEDUPE_THRESHOLD", "85"))

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".jpg", ".jpeg", ".png"}
