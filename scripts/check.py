#!/usr/bin/env python3
"""
Lint preserved manifests plus Codex marketplace/plugin metadata and verify cross-file references.

Checks:
  1. Every *.yaml under managed-agent-cookbooks/ parses.
  2. Every preserved plugin manifest, Codex marketplace/plugin manifest, and steering-examples.json parses.
  3. Every system.file, skills[].path, callable_agents[].manifest in agent.yaml
     and subagent yamls resolves to an existing file/dir.
  4. Every managed-agent-cookbooks/<slug>/ has agent.yaml, README.md, steering-examples.json.

Exit 0 if clean, 1 otherwise. Requires: pyyaml.
"""
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: requires pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MANAGED = ROOT / "managed-agent-cookbooks"
errors: list[str] = []
checked = 0


def err(msg: str) -> None:
    errors.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


for yml in sorted(MANAGED.rglob("*.yaml")):
    checked += 1
    try:
        with open(yml, encoding="utf-8") as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        err(f"YAML parse: {rel(yml)}: {e}")


json_globs = [
    ".agents/plugins/marketplace.json",
    "plugins/legal-services-codex/.codex-plugin/plugin.json",
    "plugins/**/.claude-plugin/plugin.json",
    "managed-agent-cookbooks/*/steering-examples.json",
]
for pat in json_globs:
    for jf in sorted(ROOT.glob(pat)):
        checked += 1
        try:
            json.loads(jf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"JSON parse: {rel(jf)}: {e}")


def check_refs(yml: Path) -> None:
    try:
        data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return

    base = yml.parent

    sys_spec = data.get("system")
    if isinstance(sys_spec, dict) and "file" in sys_spec:
        p = (base / sys_spec["file"]).resolve()
        if not p.is_file():
            err(f"ref: {rel(yml)}: system.file -> {sys_spec['file']} (not found)")

    for s in data.get("skills") or []:
        if isinstance(s, dict) and "path" in s:
            p = (base / s["path"]).resolve()
            if not p.exists():
                err(f"ref: {rel(yml)}: skills.path -> {s['path']} (not found)")
        if isinstance(s, dict) and "from_plugin" in s:
            p = (base / s["from_plugin"]).resolve()
            if not (p / "skills").is_dir():
                err(f"ref: {rel(yml)}: skills.from_plugin -> {s['from_plugin']} (no skills/ dir)")

    for c in data.get("callable_agents") or []:
        if isinstance(c, dict) and "manifest" in c:
            p = (base / c["manifest"]).resolve()
            if not p.is_file():
                err(f"ref: {rel(yml)}: callable_agents.manifest -> {c['manifest']} (not found)")


for yml in sorted(MANAGED.rglob("*.yaml")):
    check_refs(yml)


mp = ROOT / ".agents" / "plugins" / "marketplace.json"
for p in json.loads(mp.read_text(encoding="utf-8")).get("plugins", []):
    src_spec = p.get("source") or {}
    src_path: str | None = None
    if isinstance(src_spec, dict):
        src_path = src_spec.get("path")
    elif isinstance(src_spec, str):
        src_path = src_spec

    if not src_path:
        err(f"marketplace: {p.get('name', '<unknown>')} source is missing a local path")
        continue

    src = (ROOT / src_path).resolve()
    has_codex_plugin = (src / ".codex-plugin" / "plugin.json").is_file()
    has_legacy_plugin = (src / ".claude-plugin" / "plugin.json").is_file()
    if not (has_codex_plugin or has_legacy_plugin):
        err(
            f"marketplace: {p.get('name', '<unknown>')} source -> {src_path} "
            "(no .codex-plugin/plugin.json or .claude-plugin/plugin.json)"
        )


for d in sorted(MANAGED.iterdir()):
    if not d.is_dir():
        continue
    for req in ("agent.yaml", "README.md", "steering-examples.json"):
        if not (d / req).is_file():
            err(f"missing: {rel(d)}/{req}")


if errors:
    print(f"FAIL - {len(errors)} issue(s) across {checked} file(s):\n", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)

print(f"OK - {checked} file(s) checked, 0 issues.")
