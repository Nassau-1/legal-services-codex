# legal-services-codex

Codex-native port of Anthropic's `claude-for-legal` repository.

This repository preserves the upstream legal workflow content, practice-area playbooks, and managed-agent cookbooks, then rebuilds the runtime layer around Codex. The goal is the same one used in `financial-services-codex`: keep the useful domain content, preserve provenance, and replace Claude-specific packaging and runtime assumptions with Codex-facing skills, repo-local scripts, explicit connector setup, and generated plugin output.

> [!IMPORTANT]
> Nothing in this repository is legal advice or a substitute for attorney judgment. These assets draft and organize legal work product for review by a qualified lawyer. Every citation, classification, escalation, deadline, and draft still requires human review, source validation, and professional sign-off.

## What This Repo Is

- An attributed port of Anthropic's legal workflow materials into a Codex-first repository shape.
- A preserved source layer under `plugins/` and `managed-agent-cookbooks/` for provenance and ongoing content reuse.
- A Codex runtime layer under `codex/` plus `plugins/legal-services-codex/` for generated exports, managed-agent migration packs, and an installable Codex plugin.

## Status

- `plugins/vertical-plugins/` and `plugins/partner-built/` remain the imported upstream source material.
- `codex/` is the generated Codex-facing export surface built from that source content.
- `codex/task-packs/` is the hand-authored Codex workflow layer for Anthropic's legal managed-agent cookbooks.
- `plugins/legal-services-codex/` is the installable Codex plugin surface built from the full Codex export plus the workflow layer.
- `docs/connectors/` and `.env.example` define the connector naming and setup surface for MCP-dependent workflows.
- `scripts/build_codex_port.py` produces the Codex export and compatibility report.
- `scripts/map_managed_agents.py` summarizes the legacy managed-agent layer into a Codex migration map.
- `scripts/build_installable_plugin.py` syncs the full Codex export and task-pack workflow layer into installable plugin skills.
- The old Claude-only root install surface is not the active runtime path in this public Codex repo.

## Current Layout

```text
codex/                         Generated Codex-first skills and reports
codex/task-packs/              Hand-authored Codex task packs for the managed-agent families
plugins/vertical-plugins/      Imported practice-area legal plugins kept as canonical source
plugins/partner-built/         Imported partner-built plugin source material
plugins/legal-services-codex/  Installable Codex plugin generated from the export and task packs
managed-agent-cookbooks/       Legacy Anthropic managed-agent manifests kept for reference
scripts/                       Local validation, export, and migration helpers
docs/                          Architecture, ADRs, and Codex porting notes
```

## Working Model

### Canonical content

The source material lives under:

- `plugins/vertical-plugins/`
- `plugins/partner-built/`

Those directories contain the reusable legal domain content. The managed-agent manifests under `managed-agent-cookbooks/` are retained for provenance and workflow mapping, but they are not the active Codex runtime surface.

The imported source tree still contains some Anthropic-oriented metadata inside the upstream plugin folders because that structure is part of the provenance layer. The repo root, however, presents a Codex-first surface.

### Codex runtime surface

The Codex-facing material is generated under:

- `codex/skills/<plugin>/<skill>/`
- `codex/commands/<plugin>/` when an upstream source actually ships command markdown
- `codex/registry.json`
- `codex/compatibility-report.md`
- `codex/task-packs/registry.json`
- `codex/managed-agent-map.md`

Generate or refresh it with:

```powershell
python scripts/build_codex_port.py
python scripts/map_managed_agents.py
python scripts/build_installable_plugin.py
```

The repo-local plugin marketplace entry lives at:

- `.agents/plugins/marketplace.json`

### Using In Codex

Once installed, the plugin can be used in two ways:

- call a direct exported skill such as `$dsar-response`, `$claim-chart`, or `$clearance`
- call a workflow entrypoint such as `$renewal-watcher`, `$diligence-grid`, or `$docket-watcher`

Some upstream skill names repeat across practice areas. The installable plugin filters out internal scaffolding skills and auto-prefixes only duplicated end-user names that remain, so use names such as `$review`, `$nda-review`, `$tabular-review`, `$dsar-response`, or `$ai-governance-legal-use-case-triage`.

## Verification

Before closing porting work:

- run `python scripts/build_codex_port.py`
- run `python scripts/map_managed_agents.py`
- run `python scripts/build_installable_plugin.py`
- inspect `codex/compatibility-report.md`
- run `python scripts/check.py` when managed-agent manifests or plugin metadata are affected
- inspect `docs/connectors/` when a workflow depends on MCP-backed data providers

## License

[Apache License 2.0](./LICENSE). See also [NOTICE](./NOTICE) for attribution and derivative-work notices.
