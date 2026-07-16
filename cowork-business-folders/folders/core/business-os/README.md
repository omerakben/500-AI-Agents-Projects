# Business OS

> The operating layer every business runs on: memory, a morning brief, an end-of-day log, and a decision record. Start here, then add specialist folders around it.

## 20-minute quickstart
1. **Install** — copy this folder to your machine (see the repo README for a one-line `degit`).
2. **Teach it** — open [`setup.md`](setup.md) and fill in `memory/profile.md` (~10 min).
3. **First win** — open this folder in Claude Cowork and ask:
   > "Give me my morning brief."
   It reads your profile and today's context and saves a brief to `reports/`.
4. **Activate** — create two scheduled tasks from `schedules/`: the morning brief (8:00)
   and the EOD log (18:00).

## What's inside
| Path | What it is |
|---|---|
| `CLAUDE.md` | How this folder operates (its instructions). |
| `skills/` | `morning-brief`, `eod-log`, `decision-log`, `meeting-prep`. |
| `schedules/` | Timed prompts for the morning brief and EOD log. |
| `workflows/weekly-review.md` | A Friday roll-up of the week. |
| `templates/` | Report and decision templates. |
| `memory/` | **Your** data — profile, decisions, people, daily logs. |
| `reports/` | Generated briefs and reviews. |

## Why "OS"?
Every other folder in the catalog (finance, sales, support…) plugs into this one. In a
bundle pack they share this folder's `memory/` tree, so the whole business speaks with
one memory and reports up through one morning brief.

## Connectors
Optional. See [`connectors.md`](connectors.md). Works fully with none — you just type or
paste context instead of it being pulled in.
