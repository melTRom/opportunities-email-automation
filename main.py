"""
Pipeline orchestrator. Run with: python main.py

Stage order matches the README architecture diagram:
ingest -> extract -> dedupe -> date-filter -> draft email -> review -> write
"""
import config
from src.ingestion import load_raw_items
from src.extraction import extract_all
from src.airtable_client import fetch_existing_records, write_new_records
from src.dedupe import mark_duplicates
from src.date_filter import filter_current_and_future
from src.email_composer import draft_email
from src.review import present_for_review


def run_pipeline() -> None:
    print("== 1. Ingesting raw items ==")
    raw_items = load_raw_items(config.INPUT_FOLDER)
    print(f"Found {len(raw_items)} files in {config.INPUT_FOLDER}")

    print("== 2. Extracting structured data via Claude ==")
    items = extract_all(raw_items, model=config.ANTHROPIC_MODEL)
    print(f"Extracted {len(items)} items")

    print("== 3. Fetching existing Airtable records ==")
    existing = fetch_existing_records(
        config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME, config.AIRTABLE_PAT
    )
    print(f"Found {len(existing)} existing records")

    print("== 4. Marking duplicates ==")
    items = mark_duplicates(items, existing, config.DEDUPE_THRESHOLD)

    print("== 5. Filtering to current + future dates ==")
    items = filter_current_and_future(items)
    new_items = [i for i in items if not i.is_duplicate]
    print(f"{len(new_items)} new, non-duplicate items remain after filtering")

    print("== 6. Drafting weekly email via Claude ==")
    email_text = draft_email(new_items, model=config.ANTHROPIC_MODEL)

    print("== 7. Review gate ==")
    confirmed = present_for_review(email_text, new_items)
    if not confirmed:
        print("Not confirmed -- nothing written to Airtable. Exiting.")
        return

    print("== 8. Writing new records to Airtable ==")
    written_ids = write_new_records(
        new_items, config.AIRTABLE_BASE_ID, config.AIRTABLE_TABLE_NAME, config.AIRTABLE_PAT
    )
    print(f"Wrote {len(written_ids)} new records.")


if __name__ == "__main__":
    run_pipeline()
