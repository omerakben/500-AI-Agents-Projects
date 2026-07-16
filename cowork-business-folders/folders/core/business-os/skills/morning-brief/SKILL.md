# Morning Brief

**When to use:** the owner asks for a brief, or the 8:00 scheduled task runs.

## Inputs
- `memory/profile.md` — priorities, hard rules, key facts.
- `memory/logs/` — the last day or two, to carry over anything open.
- `memory/decisions.md` — recent decisions that imply follow-ups.
- If connected: today's Google Calendar events and unread Gmail threads flagged as needing a reply.

## Steps
1. Read the profile and the two most recent daily logs. Note anything left open.
2. If Calendar is connected, list today's meetings; flag any without prep.
3. If Gmail is connected, scan unread threads for ones that need a **decision** (not FYIs).
4. Assemble, using `templates/brief.md`:
   - **Top 3 priorities** for today (from open items + profile priorities).
   - **Needs your decision** — anything blocked on the owner.
   - **On the calendar** — meetings, with a note where prep is missing.
   - **Overdue / slipping** — items open more than 2 days.
5. Save to `reports/brief-<YYYY-MM-DD>.md` and give the owner the highlights in chat.

## Output
- `reports/brief-<date>.md`
- A short chat summary leading with what needs a decision.
