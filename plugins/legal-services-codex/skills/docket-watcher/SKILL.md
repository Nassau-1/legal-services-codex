---
name: docket-watcher
description: Run a Codex docket-watcher workflow that reviews new docket activity, maps candidate deadlines, and stages a report plus verification queue.
---

# Docket Watcher Task Pack

Use this task pack when the user needs monitored docket updates and candidate deadline mapping for active litigation matters.

Before running:

- read [`references/workers.md`](./references/workers.md)
- read [`../../../codex/managed-agent-map.md`](../../../codex/managed-agent-map.md) for provenance
- use the reusable skill content under `codex/skills/litigation-legal/`

## Inputs

Minimum inputs:

- matter list or docket scope
- review cutoff date
- jurisdiction-rule source or local rule table path

Optional inputs:

- urgency window
- reporting audience
- existing deadlines feed for comparison

## Output Contract

Primary artifacts:

- `./out/docket-report-<date>.md`
- `./out/deadlines-<date>.yaml`

Supporting scratch files are allowed under:

- `./out/tmp/docket-watcher/`

## Connector Gate

Preferred connectors:

- `trellis`
- `courtlistener`
- `gdrive`

If the docket connectors are unavailable, continue only when reviewed docket exports are already available locally. State that limitation explicitly.

## Task-Pack Flow

1. Scope the active matters and cutoff.
2. Read new docket activity.
3. Map candidate deadlines against the configured rules.
4. Write the report and deadline feed.
5. Stop for attorney verification before any calendaring action.

## Review Rules

- computed deadlines are leads, not calendar entries
- unknown courts must be surfaced as low-confidence items
- filing labels are heuristic and must be checked against the filing itself
- do not present the output as a final docketing decision
