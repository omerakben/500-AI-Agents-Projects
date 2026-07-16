# The Cowork Business Folder Standard

**Version 0.1**

This document defines the on-disk structure every business folder in this catalog follows. A folder that conforms to this standard installs, runs, and updates predictably inside Claude Cowork — and can be linted, composed into bundles, and contributed by anyone.

The standard is inspired by [Vercel eve](https://vercel.com/eve)'s file-based agent architecture, adapted to the [Claude Cowork](https://claude.com/product/cowork) runtime (Claude Desktop reading/writing a local folder, running scheduled tasks, using skills and connectors).

---

## Design principles

1. **Capability is separate from the living workspace.** Everything we ship (`skills/`, `workflows/`, `templates/`, `schedules/`, instructions) can be updated without touching what the user owns (`memory/`, `reports/`). Updates must never overwrite user data.
2. **Plain markdown the user owns.** Memory, decisions, logs, and reports are human-readable files. No lock-in, no database.
3. **First useful output in ~20 minutes.** Every folder ships a "same-day win" the user reaches by following `setup.md` once.
4. **Instructions live at the top.** `CLAUDE.md` is the folder's operating manual — Cowork reads it to know its role, its hard rules, and how to use the rest of the folder.
5. **Everything is composable.** A folder is a unit; a bundle is a manifest that composes several folders under one memory tree.

---

## Directory layout

```
<folder-slug>/
├── folder.yaml         # REQUIRED  Manifest: identity, connectors, skills, schedules
├── CLAUDE.md           # REQUIRED  Folder instructions: role, hard rules, operating guide
├── README.md           # REQUIRED  Human quickstart (the 20-minute path)
├── setup.md            # REQUIRED  "Teach it your business" onboarding checklist
├── connectors.md       # REQUIRED  Which Cowork connectors to enable and why
├── skills/             # REQUIRED  ≥1 reusable playbook, each in its own dir with SKILL.md
│   └── <skill-slug>/
│       └── SKILL.md
├── workflows/          # optional  Multi-step procedures (referenced by skills/schedules)
│   └── <workflow>.md
├── schedules/          # REQUIRED  ≥1 scheduled-task prompt (e.g. morning brief, EOD log)
│   └── <schedule>.md
├── templates/          # optional  Documents/emails/reports the business produces
│   └── <template>.md
├── memory/             # REQUIRED  User-owned living workspace (seeded with empty stubs)
│   ├── profile.md
│   ├── decisions.md
│   ├── people.md
│   └── logs/
│       └── .gitkeep
└── reports/            # REQUIRED  Generated owner-facing outputs (starts empty)
    └── .gitkeep
```

### Capability vs. workspace

| Ships & versioned by the catalog | Owned & written by the user |
|---|---|
| `folder.yaml`, `CLAUDE.md`, `README.md`, `setup.md`, `connectors.md` | `memory/` |
| `skills/`, `workflows/`, `templates/`, `schedules/` | `reports/` |

An update to a folder replaces the left column and leaves the right column alone.

---

## `folder.yaml` — the manifest

The single machine-readable source of truth. Validated by [`folder.schema.json`](folder.schema.json).

```yaml
# REQUIRED
slug: business-os               # kebab-case, matches directory name
name: Business OS               # human-readable
category: core                  # core | finance | growth | operations | people | professional | commerce
version: 0.1.0                  # semver; bump when capability changes
summary: >                      # one sentence
  The operating layer for any business: memory, a morning brief,
  an end-of-day log, and a running decision record.
same_day_win: >                 # what the user gets in the first session
  A morning brief generated from your profile and today's priorities.

# REQUIRED — how the user reaches Cowork
connectors:                     # each: name + required|optional + why
  - name: Google Calendar
    required: false
    why: Pull today's meetings into the morning brief.
  - name: Gmail
    required: false
    why: Summarize unread threads that need a decision.

# REQUIRED — capability declared for linting & the catalog
skills:
  - slug: morning-brief
    summary: Assemble a prioritized start-of-day brief.
  - slug: decision-log
    summary: Capture a decision with context, options, and rationale.

schedules:
  - slug: morning-brief
    cadence: "weekdays 08:00"   # human cadence; the user sets the real trigger in Cowork
    summary: Generate and save the morning brief.
  - slug: eod-log
    cadence: "weekdays 18:00"
    summary: Log what happened today and update memory.

# optional
workflows:
  - slug: weekly-review
    summary: Roll up the week and set next week's priorities.
maintainers:
  - omerakben
```

---

## `CLAUDE.md` — folder instructions

Read by Cowork on every run. Structure:

```markdown
# <Name> — operating instructions

## Role
Who you are for this business, in 1–2 sentences.

## Hard rules
Non-negotiables. e.g. "Never send an email without showing me a draft first."
"Never invent numbers — if a figure isn't in memory/ or a connector, ask."

## How this folder works
- Where memory lives, what each file means.
- When to write to memory/ vs reports/.
- How to run each skill and schedule.

## Voice & output
Tone, formatting, length defaults for owner-facing output.
```

`CLAUDE.md` must state at least one **hard rule** and must point to `memory/` as the source of truth.

---

## `skills/<slug>/SKILL.md`

A focused, reusable playbook. Structure:

```markdown
# <Skill name>

**When to use:** trigger conditions.

## Inputs
What the skill needs (files, connectors, a question from the user).

## Steps
1. …
2. …

## Output
Where the result goes (`reports/…`, a message, an updated `memory/…`).
```

Every folder ships **at least one skill**.

---

## `schedules/<slug>.md`

A prompt the user pastes into a Cowork scheduled task. Structure:

```markdown
# <Schedule name>  ·  cadence: weekdays 08:00

<The exact prompt Cowork runs on schedule. Reference skills by name and
write outputs to memory/ or reports/. Keep it self-contained.>
```

Every folder ships **at least one schedule** — this is what makes it "operate" rather than sit idle.

---

## `memory/` — the living workspace

Ships with **empty stubs** the user fills in during setup:

- `profile.md` — the business: what it does, who runs it, key facts, hard rules.
- `decisions.md` — an append-only decision log.
- `people.md` — customers, staff, vendors, contacts.
- `logs/` — dated daily/EOD logs.

The linter checks these exist but must **not** ship them pre-filled with fake data.

---

## Versioning & updates

- `version` in `folder.yaml` is semver. Bump **minor** for new skills/workflows, **patch** for fixes, **major** for a breaking layout change.
- Updating a folder = re-copying the capability files. A `CHANGELOG.md` is encouraged for folders past `1.0.0`.

---

## Conformance checklist

A folder conforms when:

- [ ] `folder.yaml` exists and validates against `folder.schema.json`.
- [ ] `slug` in `folder.yaml` matches the directory name.
- [ ] `CLAUDE.md`, `README.md`, `setup.md`, `connectors.md` all exist and are non-empty.
- [ ] `CLAUDE.md` contains a "Hard rules" section.
- [ ] `skills/` contains ≥1 skill with a `SKILL.md`, and every skill in `folder.yaml` has a matching directory.
- [ ] `schedules/` contains ≥1 schedule, and every schedule in `folder.yaml` has a matching file.
- [ ] `memory/` contains `profile.md`, `decisions.md`, `people.md`, and `logs/`.
- [ ] `reports/` exists (may be empty).

Run `python tools/lint.py <folder>` to check.
