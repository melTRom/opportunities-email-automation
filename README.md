# Weekly Opportunities Email Automation

Automates turning messy weekly inputs (flyer PDFs/images, forwarded email
text, Airtable records) into a reviewed, deduped, deadline-filtered weekly
opportunities email for CS students -- with a human confirmation step before
anything is written back to Airtable or considered final.

Built as a portfolio project to demonstrate an end-to-end LLM data pipeline:
multimodal extraction -> structured data -> dedupe -> filter -> generation ->
human-in-the-loop write-back.

## Architecture

```
 data/sample_inputs/*.txt,.pdf,.jpg
             |
             v
  [1] ingestion.py        -- reads local files (stand-in for Trello/Gmail APIs)
             |
             v
  [2] extraction.py        -- 1 Claude API call per item (multimodal for
             |                 images/PDFs, text for emails) -> JSON matching
             |                 src/models.py:OpportunityItem
             v
  [3] airtable_client.py   -- fetch_existing_records() reads current Airtable
             |                 table via REST API (pyairtable)
             v
  [4] dedupe.py            -- fuzzy title match (rapidfuzz) + date match
             |                 against existing records -> flags duplicates
             v
  [5] date_filter.py       -- drops anything before the current week
             |
             v
  [6] email_composer.py    -- 1 Claude API call: filtered items -> drafted
             |                 weekly email (Outlook-style, grouped listings)
             v
  [7] review.py            -- prints draft email + pending new records,
             |                 requires explicit y/n confirmation
             v
  [8] airtable_client.py   -- write_new_records() -- ONLY runs after
                               confirmation in step 7
```

`main.py` runs all 8 steps in order. Every stage takes/returns plain
`OpportunityItem` objects (`src/models.py`), so stages can be tested or
swapped independently -- e.g. later replacing `ingestion.py`'s folder scan
with real Trello/Gmail API calls shouldn't require touching anything
downstream.

## MVP scope (today) vs. later

| Area | MVP (this repo) | Production later |
|---|---|---|
| Ingestion | Local folder of sample files | Live Trello + Gmail API polling |
| Airtable | Live REST API, read + write | Same, plus schema validation/retries |
| Extraction | 1 Claude call/item, JSON schema | Add confidence scoring, human flag for low-confidence extractions |
| Dedupe | Fuzzy title + date match | Semantic/embedding-based matching, cross-field checks |
| Delivery | Draft printed for review | Actual Outlook send via Graph API |
| Review | Terminal y/n prompt | Web UI or Slack approval step |

## Setup

1. **Clone and create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Fill in `.env` with:
   - `ANTHROPIC_API_KEY` -- from [console.anthropic.com](https://console.anthropic.com)
   - `AIRTABLE_PAT` -- a [personal access token](https://airtable.com/create/tokens) scoped to `data.records:read`, `data.records:write`, `schema.bases:read`
   - `AIRTABLE_BASE_ID` -- found in your base's API docs (`airtable.com/api` when logged in)
   - `AIRTABLE_TABLE_NAME` -- must have fields: `Title`, `Date`, `Description`, `Location`, `Link`, `Source`

3. **Add sample input files**
   Drop a mix of files into `data/sample_inputs/`:
   - `.txt` files with forwarded email-style text
   - `.jpg`/`.png` flyer images
   - `.pdf` flyers

4. **Run the pipeline**
   ```bash
   python main.py
   ```
   You'll see progress through all 8 stages, then a printed draft email and
   list of pending new Airtable records. Nothing is written until you
   confirm at the prompt.

## Repo layout

```
.
├── main.py                 # orchestrator -- runs the full pipeline
├── config.py                # loads + validates all env vars in one place
├── requirements.txt
├── .env.example
├── src/
│   ├── models.py            # OpportunityItem -- shared schema, Claude's
│   │                         #   extraction JSON must match this
│   ├── ingestion.py          # Stage 1: read local sample files
│   ├── extraction.py         # Stage 1b: Claude multimodal extraction
│   ├── airtable_client.py    # Stage 2/8: Airtable REST read + write
│   ├── dedupe.py              # Stage 2: fuzzy dedupe vs Airtable
│   ├── date_filter.py         # Stage 3: drop past-dated items
│   ├── email_composer.py      # Stage 4: Claude drafts the weekly email
│   └── review.py              # Stage 5: human confirmation gate
├── data/sample_inputs/       # put test flyers/emails here (gitignored contents optional)
└── output/drafts/            # where draft artifacts can be saved (gitignored)
```

## Why these library choices

- **`anthropic`** -- official SDK, handles multimodal (image/PDF) message construction.
- **`pyairtable`** -- actively maintained wrapper over Airtable's REST API; avoids hand-rolling auth headers and pagination.
- **`rapidfuzz`** -- fast, dependency-light fuzzy string matching for the dedupe stage (title similarity).
- **`pydantic`** -- enforces the JSON schema Claude returns actually matches what downstream stages expect, and fails loudly if not.
- PDFs are sent directly to Claude as base64 documents (Claude reads PDFs natively) -- no separate PDF-to-image conversion step or Poppler dependency needed for the MVP.

## Status

Repo scaffolded; every `src/*.py` module has real function signatures and
docstrings but raises `NotImplementedError` in the body. Next step: implement
stage by stage, starting with `ingestion.py` and `extraction.py`.
