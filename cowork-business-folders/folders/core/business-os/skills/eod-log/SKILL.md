# End-of-Day Log

**When to use:** the owner wraps up, or the 18:00 scheduled task runs.

## Inputs
- Today's `reports/brief-<date>.md`, if one exists.
- Anything the owner tells you happened today.
- If connected: today's sent mail and completed calendar events for a memory jog.

## Steps
1. Ask (or infer from context) three things: what got done, what didn't, what's new.
2. Write `memory/logs/<YYYY-MM-DD>.md` with:
   - **Done** — completed items.
   - **Open / carried to tomorrow** — with why.
   - **New** — anything that surfaced (a lead, an issue, a commitment).
3. If any durable fact emerged (a decision, a new contact, a changed price), propose an
   update to `memory/decisions.md` or `memory/people.md` and apply it once confirmed.
4. One-line summary to the owner.

## Output
- `memory/logs/<date>.md`
- Proposed updates to `memory/decisions.md` / `memory/people.md` as needed.

> Follows the hard rule: never overwrite the owner's words silently — append or confirm.
