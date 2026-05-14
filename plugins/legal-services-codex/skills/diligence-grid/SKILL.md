---
name: diligence-grid
description: Run a Codex diligence-grid workflow that monitors a VDR or performs a schema-based tabular review over a diligence folder with citation-per-cell discipline.
---

# Diligence Grid Task Pack

Use this task pack when the user needs a legal diligence document set monitored or converted into a cited review grid.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../../../codex/managed-agent-map.md`](../../../codex/managed-agent-map.md) for provenance
- use the reusable skill content under `codex/skills/corporate-legal/`

## Inputs

Minimum inputs:

- deal or folder identifier
- reviewed folder scope or VDR source
- requested schema or confirmation to use the default M&A diligence schema

Optional inputs:

- request-list categories
- materiality thresholds
- output filename convention

## Output Contract

Primary artifacts:

- `./out/diligence-grid-<deal>.csv`
- `./out/diligence-grid-<deal>-sources.csv`
- `./out/diligence-grid-<deal>.md`

Supporting scratch files are allowed under:

- `./out/tmp/diligence-grid/`

## Connector Gate

Preferred connectors:

- `box`
- `imanage`
- `definely`
- `gdrive`

If the connectors are unavailable, continue only when the document set is already available locally and reviewed for access scope. State that limitation explicitly.

## Task-Pack Flow

1. Scope the deal folder and review mode.
2. Sample the schema on a small document subset.
3. Extract grid rows with citation-per-cell discipline.
4. Normalize and write the grid artifacts.
5. Stop for lawyer review.

## Review Rules

- every filled cell must carry a typed value and supporting quote
- a cell with no quote is an unsupported claim
- outputs are leads, not legal findings
- do not treat materiality classifications as final lawyer calls
