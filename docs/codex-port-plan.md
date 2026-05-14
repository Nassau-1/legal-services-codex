# Codex Port Plan

## Objective

Convert the imported `claude-for-legal` content into a Codex-first operating surface without relying on Claude plugin installation, Anthropic managed-agent deployment, or hidden runtime helper behavior.

## Non-Goals

- preserving Anthropic runtime APIs as an execution dependency
- hiding incompatible references instead of tracking them
- claiming connector availability without local configuration

## Port Layers

### Layer 1: Repo governance and safe fork

- separate repo copy under `projects/legal-services-codex`
- detached source provenance
- workspace-standard governance files

### Layer 2: Codex export surface

- generated `codex/skills/`
- generated `codex/commands/` when source command markdown exists
- generated `codex/registry.json`
- generated `codex/compatibility-report.md`

### Layer 3: Runtime replacement

- Codex-oriented documentation replacing Claude-only operator assumptions
- connector naming and environment documentation under `docs/connectors/`
- explicit packaging of the installable Codex plugin surface

### Layer 4: Deep workflow migration

- agent workflow mapping from `managed-agent-cookbooks/`
- task-pack conversion for the five managed legal workflows
- explicit Codex orchestration patterns for headless legal monitoring and review flows

## Highest-Risk Gaps

- connector-dependent legal systems that require tenant credentials and non-public data
- managed-agent orchestration concepts with no direct Codex equivalent
- duplicated upstream skill names that collide in a flat installable plugin namespace
- workflow outputs that can be misread as legal conclusions without strong review framing

## Verification Plan

- rerun `python scripts/build_codex_port.py` after source edits
- inspect `codex/compatibility-report.md` for unresolved runtime blockers
- rerun `python scripts/map_managed_agents.py` after managed-agent changes
- rerun `python scripts/build_installable_plugin.py` after workflow or packaging changes
- run `python scripts/check.py` when plugin metadata or managed-agent manifests are changed
