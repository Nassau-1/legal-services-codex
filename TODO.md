# TODO

## Next Version

- [ ] Exercise the actual Codex plugin installation flow on-machine and record any manifest constraints discovered.
- [ ] Add smoke-test fixtures or example reviewed inputs for each legal task pack.
- [ ] Decide whether the legal task-pack layer should remain fully hand-authored or be generated from `codex/managed-agent-map.json`.
- [ ] Add a lightweight connector-health verification pattern for the MCP-dependent workflows.
- [ ] Review which exported duplicate skill names should receive stable friendly aliases in addition to the auto-prefixed installable names.

## Later

- [ ] Add optional repo-local review helpers for generated CSV, Markdown, and YAML outputs analogous to workbook verification in the financial port.
- [ ] Decide whether additional legal workflow packs should be elevated beyond the five imported managed-agent families.

## Rejected Or Deferred

- [ ] Full runtime parity with Anthropic Managed Agents API is deferred because it requires a different orchestration runtime than Codex exposes here.
