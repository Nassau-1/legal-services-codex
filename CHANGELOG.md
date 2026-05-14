# Changelog

Use reverse chronological order. Keep entries factual and date-stamped.

## 2026-05-14T00:00:00+02:00

- Created `legal-services-codex` as a separate governed repository under `projects/`.
- Imported Anthropic's `claude-for-legal` source content into preserved `plugins/vertical-plugins/`, `plugins/partner-built/`, and `managed-agent-cookbooks/` provenance layers.
- Added a Codex export pipeline, managed-agent migration map, installable plugin build, connector documentation, and legal-specific task packs following the `financial-services-codex` porting method.
- Added a `v0.1.1` plugin discovery layer with a top-level index skill and explicit practice-area alias entrypoints.
- Corrected the installable plugin surface in `v0.1.2` to match the financial porting method more closely by removing synthetic preview skills and filtering internal scaffolding skills from the top-level install bundle.
- Corrected install metadata in `v0.1.3` so generated `openai.yaml` descriptions are parsed from multiline frontmatter correctly and surface real skill blurbs instead of malformed placeholders.
