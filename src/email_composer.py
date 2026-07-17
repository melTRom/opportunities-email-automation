"""
Stage 4: Template fill via Claude API.

Takes the filtered, deduped list of OpportunityItems and drafts the weekly
email: Outlook-style, professional, scannable, grouped listings, targeted at
CS students. This is a single Claude API text call (no multimodal needed
here) with the structured list serialized into the prompt.
"""
from src.models import OpportunityItem

EMAIL_SYSTEM_PROMPT = """\
You write a weekly opportunities/events email for computer science students.
Tone: clear, professional, concise, opportunity-focused -- no fluff, no
exclamation-point marketing voice. Format like a well-organized Outlook email:

- Short intro (1-2 sentences, no greeting fluff)
- Items grouped under headers (e.g. "Internships & Jobs", "Workshops & Events",
  "Deadlines This Week") -- group sensibly based on what's in the list
- Each item: **Title** -- Date -- one-line description -- Location (if any) --
  link on its own line
- Plain text or simple markdown, no heavy HTML

Return only the email body (subject line first, then a blank line, then the
body). No preamble, no commentary about your choices.
"""


def draft_email(items: list[OpportunityItem], model: str) -> str:
    """
    Serialize items into the prompt and return the drafted email text
    (subject + body) from a single Claude API call.
    """
    raise NotImplementedError
