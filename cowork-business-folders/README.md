# Cowork Business Folders

**Ready-to-operate business folders for [Claude Cowork](https://claude.com/product/cowork) (Claude Desktop).**

Download the folder for your business → point Claude Cowork at it → teach it your specifics → turn on scheduling. First useful output in ~20 minutes. No prompt engineering required.

> Think of this as **"[eve](https://vercel.com/eve) for Claude Cowork"** — every business is a standardized, versioned, downloadable directory instead of a pile of prompts.

---

## How it works

```
1. Install   →  Copy a folder (or a bundle pack) to your machine.
2. Teach     →  Walk the setup.md checklist so it learns your business, tools, and hard rules.
3. Activate  →  Open the folder in Claude Cowork and turn on the morning brief + EOD log.
```

Claude Cowork reads and writes files **inside** the folder, runs **scheduled tasks** scoped to it, and uses the **skills** and **connectors** the folder declares. Your data stays in plain markdown files you own.

### The one principle that makes this work

Every folder separates **capability** from your **living workspace**:

| Capability (we ship & version) | Living workspace (you own) |
|---|---|
| `skills/`, `workflows/`, `templates/`, `schedules/` | `memory/`, `reports/` |
| Updated when you pull a new version | **Never overwritten** on update |

Pull an update and your profile, decisions, logs, and reports are untouched.

---

## Install a single folder

Each folder is self-contained, so you can grab just one without cloning the whole repo:

```bash
# With degit (recommended — no git history):
npx degit omerakben/500-ai-agents-projects/cowork-business-folders/folders/core/business-os my-business

# Or sparse-checkout a single folder:
git clone --no-checkout --depth 1 https://github.com/omerakben/500-ai-agents-projects.git
cd 500-ai-agents-projects
git sparse-checkout set cowork-business-folders/folders/core/business-os
git checkout
```

Then open `my-business/` in Claude Cowork and follow its `README.md`.

---

## Catalog

Legend: ✅ available · 🛠️ planned

### Core — the operating layer every business builds on
| Folder | Status | What it does |
|---|---|---|
| [`business-os`](folders/core/business-os) | ✅ | Operating layer: memory, morning brief, EOD log, decision log |
| `agency-os` | 🛠️ | Multi-client operating layer with namespaced memory |
| `front-desk` | 🛠️ | General admin: inbox triage, scheduling, follow-ups |

### Finance
| Folder | Status | What it does |
|---|---|---|
| `books-and-close` | 🛠️ | Bookkeeping and month-end close |
| `cash-and-capital` | 🛠️ | Cash-flow forecasting and financing documents |

### Growth
| Folder | Status | What it does |
|---|---|---|
| `marketing-engine` | 🛠️ | Content creation and campaigns |
| `sales-desk` | 🛠️ | Pipeline management and outreach |
| `product-studio` | 🛠️ | Product specs, research synthesis, release notes |
| `support-desk` | 🛠️ | Customer service and knowledge base |

### Operations
| Folder | Status | What it does |
|---|---|---|
| `ops-and-erp` | 🛠️ | Order and inventory management |
| `data-desk` | 🛠️ | Metrics, dashboards, incident triage |
| `safety-and-compliance` | 🛠️ | EHS and audit tracking |
| `compliance-desk` | 🛠️ | SOC 2 / ISO 27001 / GDPR evidence collection |

### People
| Folder | Status | What it does |
|---|---|---|
| `people-desk` | 🛠️ | Hiring, onboarding, performance reviews |
| `founder-cos` | 🛠️ | Chief-of-staff functions |

### Professional services
| Folder | Status | What it does |
|---|---|---|
| `law-office` | 🛠️ | Legal intake and matter management |
| `client-practice` | 🛠️ | Therapy / coaching session prep |
| `grants-and-giving` | 🛠️ | Nonprofit fundraising |

### Commerce
| Folder | Status | What it does |
|---|---|---|
| `storefront` | 🛠️ | E-commerce listings and margin management |
| `field-service` | 🛠️ | Trades and construction quoting |

---

## Bundle packs

A **pack** composes several folders that share **one memory tree** and merge into **one morning brief + one EOD report**.

| Pack | Status | For | Folders |
|---|---|---|---|
| [`main-street`](bundles/main-street.yaml) | ✅ (manifest) | Local retail & service | `business-os` + `front-desk` + `books-and-close` + `marketing-engine` |
| `capital` | 🛠️ | Growth / lending prep | `business-os` + `cash-and-capital` + `data-desk` |
| `agency` | 🛠️ | Marketing agencies | `agency-os` + `marketing-engine` + `sales-desk` |
| `warehouse` | 🛠️ | Manufacturing | `business-os` + `ops-and-erp` + `safety-and-compliance` |
| `practice` | 🛠️ | Professional services | `business-os` + `client-practice` + `books-and-close` |
| `hq` | 🛠️ | Leadership teams | `founder-cos` + `data-desk` + `people-desk` |

---

## Contributing a folder

1. Read the [**folder standard**](standard/SPEC.md).
2. Copy the blank scaffold: `cp -r templates/_blank-folder folders/<category>/<your-folder>`.
3. Fill in `folder.yaml`, `CLAUDE.md`, `setup.md`, and at least one skill + one schedule.
4. Lint it: `python tools/lint.py folders/<category>/<your-folder>`.
5. Open a PR.

The goal: scale this toward **500 ready-to-operate businesses**, the way this repo scaled to 500 AI agents.

---

## Related

- 🧠 [Claude Cowork](https://claude.com/product/cowork) — the runtime this targets
- 🗂️ [Claude Folder Farm](https://claude-folder-farm.omer-ozzy-akben.chatgpt.site/) — the catalog concept this formalizes
- ⚙️ [Vercel eve](https://vercel.com/eve) — the file-based agent architecture that inspired the standard
- 🤖 [500 AI Agents Projects](../README.md) — the parent catalog
