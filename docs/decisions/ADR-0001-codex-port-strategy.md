# ADR-0001: Codex Port Strategy

- Status: accepted
- Date: 2026-05-14

## Context

The imported repository is structured around Claude plugins, Anthropic managed agents, and Anthropic-specific runtime expectations. The underlying legal workflows are useful, but the packaging and orchestration are not directly executable in Codex.

## Decision

Create and maintain a separate Codex-facing export surface under `codex/` while keeping the imported source structure for provenance.

The port strategy is:

1. keep reusable source content in `plugins/vertical-plugins/` and `plugins/partner-built/`
2. treat managed-agent manifests as legacy reference material
3. generate Codex-facing copies plus compatibility findings with `scripts/build_codex_port.py`
4. convert the five managed-agent families into explicit Codex task packs
5. replace Anthropic-only runtime assumptions incrementally with repo-local scripts and Codex-oriented guidance

## Consequences

### Positive

- preserves source provenance
- avoids risky in-place mutation of the original imported repo
- gives Codex a stable, explicit runtime surface
- makes duplicate skill-name collisions in the installable plugin surface explicit and solvable

### Negative

- introduces a generated-content layer that must be refreshed after source changes
- keeps some duplicated metadata until deeper migration is complete
- does not deliver immediate runtime parity for managed-agent orchestration

## Rejected Options

- Edit the imported repo in place.
  - Rejected because it would mix upstream/source concerns with the Codex port and increase rollback risk.

- Pretend the Claude plugin manifests are usable as-is in Codex.
  - Rejected because the runtime assumptions differ materially.
