# Architecture

## Context

- project: `legal-services-codex`
- purpose: `Codex-native port of Anthropic legal workflow plugins and managed-agent assets`
- date: `2026-05-14`

## Goals

- preserve the useful legal workflow content from the imported source repo
- expose that content through a Codex-first file layout instead of Claude-only plugin packaging
- make connector requirements, managed-agent assumptions, and remaining compatibility gaps explicit
- provide a generated Codex runtime surface and an installable plugin without mutating upstream provenance content

## Components

- `plugins/vertical-plugins/`
  - canonical reusable legal skill content imported from the source repo
- `plugins/partner-built/`
  - partner-authored legal plugin source retained for provenance
- `managed-agent-cookbooks/`
  - Anthropic managed-agent manifests retained for workflow mapping only
- `codex/`
  - generated Codex-facing export of the reusable skills, compatibility metadata, and reports
- `codex/task-packs/`
  - hand-authored runnable task packs for the five managed-agent families
- `plugins/legal-services-codex/`
  - installable Codex plugin generated from the export and task-pack workflow layer
- `docs/connectors/`
  - connector inventory, workflow mapping, and Codex-side MCP naming guidance
- `scripts/build_codex_port.py`
  - generates the Codex runtime surface and inventories incompatible legacy references
- `scripts/build_installable_plugin.py`
  - syncs the exported skills and task packs into installable plugin skill folders plus UI metadata
- `scripts/map_managed_agents.py`
  - summarizes the legacy managed-agent layer into a Codex migration map

## Data And Control Flow

1. Source content is maintained in `plugins/vertical-plugins/` and `plugins/partner-built/`.
2. `scripts/build_codex_port.py` copies and rewrites the reusable markdown into `codex/`.
3. The build script emits `codex/registry.json` and `codex/compatibility-report.md` so remaining Claude-only assumptions stay visible.
4. Hand-authored workflow layers under `codex/task-packs/` map the managed-agent cookbook layer into Codex-native execution guides.
5. `scripts/build_installable_plugin.py` converts the generated export and task-pack guides into plugin-installable skill folders under `plugins/legal-services-codex/`.
6. Connector-dependent workflows resolve their MCP naming and environment expectations through `docs/connectors/` and `.env.example`.
7. Codex-targeted work should prefer the generated `codex/` surface, task-pack workflow layer, installable plugin build, and repo-local scripts over legacy plugin manifests.

## Boundaries

### In Scope

- markdown skills and practice-area playbooks
- connector inventories and configuration references
- managed-agent migration mapping
- repo-local validation, export, and packaging scripts

### Out Of Scope For This First Port Pass

- authenticated access to third-party paid legal systems without tenant configuration
- one-to-one runtime parity with Claude Cowork dispatch
- Anthropic Managed Agents API deployment as the active Codex execution path
- automatic replacement of every vendor-specific research, CLM, or docketing dependency

## Operational Notes

- The repository copy is intentionally detached from the imported source remote to avoid accidental upstream edits.
- The generated portion of `codex/` should be refreshed after canonical source changes, while the hand-authored `codex/task-packs/` layer is intentionally preserved across rebuilds.
- The installable plugin is a generated build surface and should be regenerated from the canonical workflow sources rather than edited manually.
