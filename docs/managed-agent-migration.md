# Managed-Agent Migration Notes

The imported `managed-agent-cookbooks/` tree is retained for provenance, but it is not a native Codex runtime surface.

## Current Approach

- Export the reusable content layer into `codex/`.
- Treat each `managed-agent-cookbooks/<agent>/agent.yaml` as an orchestration reference, not executable runtime config for Codex.
- Convert the cookbook layer into Codex task packs with explicit inputs, connector gates, outputs, and review stops.

## Generated Mapping

Run:

```powershell
python scripts/map_managed_agents.py
```

This generates:

- `codex/managed-agent-map.md`
- `codex/managed-agent-map.json`

Use that output to decide whether a managed-agent family should become:

- a Codex task pack
- a coordinator plus bounded worker subtasks
- a set of reusable standalone skills instead of one monolithic workflow

## Migration Heuristic

1. Keep the upstream system prompt as the domain workflow anchor.
2. Treat each subagent as a bounded responsibility, not as an API-specific primitive.
3. Re-evaluate every MCP dependency separately.
4. Replace `handoff_request` and related Anthropic steering patterns with explicit Codex sequencing.
