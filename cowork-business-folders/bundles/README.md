# Bundle packs

A **pack** composes several business folders that share **one memory tree** and merge
into **one morning brief + one end-of-day log**. Instead of four folders each with their
own memory and their own brief, the whole business speaks with one memory and reports up
once.

## Anatomy of a pack manifest
Each `*.yaml` here declares:
- `folders` — the folders to install, in order (the operating layer first).
- `shared_memory` — the single `memory/` tree every folder reads and writes.
- `merged_reports` — which folder owns the combined brief and log.
- `install_notes` — how to wire the shared memory when you install.

## Installing a pack
1. Install the **first** folder (always an operating layer like `business-os`) and finish its `setup.md`.
2. Add each remaining folder from the manifest.
3. Point every folder's `memory/` at the shared tree (a symlink to the operating layer's
   `memory/`, or keep everything in one combined folder).
4. Turn on scheduling **only** on the operating layer — its brief and log read the shared
   memory the others write to.

## Available packs
| Pack | Status | For |
|---|---|---|
| [`main-street`](main-street.yaml) | ✅ manifest (folders in progress) | Local retail & service |
| `capital` | 🛠️ | Growth / lending prep |
| `agency` | 🛠️ | Marketing agencies |
| `warehouse` | 🛠️ | Manufacturing |
| `practice` | 🛠️ | Professional services |
| `hq` | 🛠️ | Leadership teams |

> A pack is only as installable as its folders. `main-street` currently ships with
> `business-os`; the other three folders are on the roadmap (see the catalog in the
> top-level README).
