# Connector Configuration

This directory is the Codex-side configuration surface for the MCP-dependent workflows that came from the imported legal managed-agent layer.

These docs do not assume Anthropic deployment tooling. They document:

- the connector names preserved in the migration map
- the environment-variable names used by the imported cookbooks
- which workflows depend on which connector
- the expected access mode for each connector

## Current Inventory

| Connector name | Env var | Primary workflows | Expected access |
| --- | --- | --- | --- |
| `asana` | `ASANA_MCP_URL` | `launch-radar` | read-only |
| `atlassian` | `ATLASSIAN_MCP_URL` | `launch-radar` | read-only |
| `box` | `BOX_MCP_URL` | `diligence-grid` | read-only |
| `courtlistener` | `COURTLISTENER_MCP_URL` | `docket-watcher` | read-only |
| `definely` | `DEFINELY_MCP_URL` | `diligence-grid` | read-only |
| `docusign` | `DOCUSIGN_MCP_URL` | `renewal-watcher` | read-only |
| `gdrive` | `GDRIVE_MCP_URL` | `diligence-grid`, `docket-watcher`, `launch-radar`, `reg-monitor`, `renewal-watcher` | read-only |
| `imanage` | `IMANAGE_MCP_URL` | `diligence-grid`, `renewal-watcher` | read-only |
| `ironclad` | `IRONCLAD_MCP_URL` | `renewal-watcher` | read-only |
| `linear` | `LINEAR_MCP_URL` | `launch-radar` | read-only |
| `trellis` | `TRELLIS_MCP_URL` | `docket-watcher` | read-only |

## Setup Rules

1. Configure only the connectors you actually need for the workflows you plan to run.
2. Treat every connector as optional until a task pack explicitly requires it.
3. Default to read-only access. If a future workflow needs write access, document that separately before enabling it.
4. Mirror any local connector URL setup into `.env.example` naming so the repo, docs, and workflow notes stay aligned.

## Recommended Setup Order

1. Populate the relevant URLs in [`.env.example`](../../.env.example) or a local untracked `.env`.
2. Configure the same endpoints in the Codex connector or MCP surface available on this machine.
3. Confirm the workflow-to-connector mapping in [`workflow-matrix.md`](./workflow-matrix.md).
4. When a workflow is run, state whether the connector path or a reviewed local-material fallback path was used.
