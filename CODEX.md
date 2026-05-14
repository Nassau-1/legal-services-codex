# Codex Repository Rules

This repository is a Codex-first port of legacy Claude-oriented legal workflow assets.

## Runtime Surface

- Treat `codex/` as the primary Codex-facing runtime surface.
- Treat `codex/task-packs/` as the hand-authored workflow layer on top of the generated export.
- Treat `plugins/legal-services-codex/` as the installable plugin build output generated from those workflow layers.
- Treat `plugins/vertical-plugins/` and `plugins/partner-built/` as canonical source material.
- Treat `managed-agent-cookbooks/` as a legacy compatibility and reference surface unless a task explicitly targets it.
- Treat upstream `.claude-plugin/` folders inside imported plugin trees as provenance metadata, not as the active install path for this repo.
- Treat `docs/connectors/` plus `.env.example` as the naming and configuration surface for MCP-dependent workflows.

## Porting Discipline

- When porting shared content, edit the canonical source first, then regenerate `codex/` with `python scripts/build_codex_port.py`.
- When workflow skills change, regenerate the installable plugin surface with `python scripts/build_installable_plugin.py`.
- Do not add new Claude-only assumptions to the Codex surface.
- Replace hidden platform behavior with repo-local scripts, explicit docs, or normal files whenever possible.
- Keep connector references declarative and auditable.

## Verification

- Re-run the Codex export after source changes and inspect the generated compatibility report.
- If a task-pack output depends on connector-backed facts, state whether the connector path or a local reviewed-material fallback was used.
- Do not describe any generated legal output as a final legal conclusion without explicit human verification.

## Documentation

- Keep `README.md`, `SECURITY.md`, `CHANGELOG.md`, `TODO.md`, and `docs/architecture.md` current.
- Record material migration decisions under `docs/decisions/`.
- Use ISO dates in architecture notes, ADRs, and changelog entries.
