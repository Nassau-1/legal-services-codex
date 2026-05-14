# Codex Export

The generated export in this directory is produced by `python scripts/build_codex_port.py`.

- Skills: `151`
- Commands: `0`
- Items with compatibility findings: `145`

## Usage

- read generated exported skills from `skills/`
- read generated exported commands from `commands/`
- inspect generated `registry.json` for source mapping and connector metadata
- inspect generated `compatibility-report.md` before assuming a skill is fully Codex-native
- use hand-authored `coordinators/` and `task-packs/` for the managed-agent-to-Codex workflow layer

Do not hand-edit generated files such as `skills/`, `commands/`, `registry.json`, or `compatibility-report.md`. Update the canonical source under `plugins/` and regenerate.

`coordinators/` and `task-packs/` are hand-authored and intentionally preserved across rebuilds.
