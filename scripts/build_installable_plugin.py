#!/usr/bin/env python3
"""Build the installable Codex plugin surface from the full Codex export."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "legal-services-codex"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
EXPORT_REGISTRY = ROOT / "codex" / "registry.json"
COORDINATORS_REGISTRY = ROOT / "codex" / "coordinators" / "registry.json"
TASK_PACKS_REGISTRY = ROOT / "codex" / "task-packs" / "registry.json"


WORKFLOW_UI = {
    "diligence-grid": {
        "display_name": "Diligence Grid",
        "short_description": "Run cited legal diligence grid workflows",
        "default_prompt": "Use $diligence-grid to review a VDR folder into a cited diligence grid.",
    },
    "docket-watcher": {
        "display_name": "Docket Watcher",
        "short_description": "Monitor matters and map candidate deadlines",
        "default_prompt": "Use $docket-watcher to review new filings and stage a docket update memo.",
    },
    "launch-radar": {
        "display_name": "Launch Radar",
        "short_description": "Triage upcoming launches for legal review",
        "default_prompt": "Use $launch-radar to screen this week's launch tracker for legal routing.",
    },
    "reg-monitor": {
        "display_name": "Reg Monitor",
        "short_description": "Generate legal and compliance change digests",
        "default_prompt": "Use $reg-monitor to summarize new regulatory developments since last Friday.",
    },
    "renewal-watcher": {
        "display_name": "Renewal Watcher",
        "short_description": "Screen contract renewals and notice deadlines",
        "default_prompt": "Use $renewal-watcher to scan the contract register for upcoming cancel-by dates.",
    },
}

EXCLUDED_EXPORTED_SKILLS = {
    "auto-updater",
    "cold-start-interview",
    "comments",
    "customize",
    "disable",
    "matter-workspace",
    "related-skills-surfacer",
    "registry-browser",
    "semester-handoff",
    "session",
    "skill-manager",
    "skills-qa",
    "status",
    "uninstall",
}

ACRONYMS = {
    "3": "3",
    "aba": "ABA",
    "ai": "AI",
    "bd": "BD",
    "bu": "BU",
    "cim": "CIM",
    "clm": "CLM",
    "crm": "CRM",
    "dcf": "DCF",
    "dd": "DD",
    "dmca": "DMCA",
    "dpa": "DPA",
    "dpia": "DPIA",
    "dsar": "DSAR",
    "er": "ER",
    "esg": "ESG",
    "ev": "EV",
    "fi": "FI",
    "fmla": "FMLA",
    "fto": "FTO",
    "fx": "FX",
    "gdpr": "GDPR",
    "gl": "GL",
    "ib": "IB",
    "ic": "IC",
    "ipo": "IPO",
    "ir": "IR",
    "js": "JS",
    "kyc": "KYC",
    "lbo": "LBO",
    "lp": "LP",
    "ma": "M&A",
    "mcp": "MCP",
    "msa": "MSA",
    "nav": "NAV",
    "nda": "NDA",
    "oss": "OSS",
    "pe": "PE",
    "pia": "PIA",
    "pfl": "PFL",
    "ppt": "PPT",
    "pptx": "PPTX",
    "qa": "Q&A",
    "rv": "RV",
    "sec": "SEC",
    "sp": "SP",
    "sql": "SQL",
    "tlh": "TLH",
    "ui": "UI",
    "vdr": "VDR",
    "wacc": "WACC",
    "xls": "XLS",
    "xlsx": "XLSX",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_clean_skills_dir() -> None:
    SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    for path in SKILLS_ROOT.iterdir():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def rewrite_skill_text(text: str) -> str:
    return text.replace("../../managed-agent-map.md", "../../../codex/managed-agent-map.md")


def normalize_frontmatter_name(text: str, skill_name: str) -> str:
    return re.sub(
        r"(?m)^name:\s*.+$",
        f"name: {skill_name}",
        text,
        count=1,
    )


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.search(r"(?ms)^---\r?\n(.*?)\r?\n---\r?\n?", text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip("\"'")
    return meta, text[match.end() :]


def slug_to_title(slug: str) -> str:
    parts = re.split(r"[-_]+", slug)
    titled: list[str] = []
    for part in parts:
        lower = part.lower()
        if lower in ACRONYMS:
            titled.append(ACRONYMS[lower])
        elif part.isdigit():
            titled.append(part)
        else:
            titled.append(part.capitalize())
    return " ".join(titled)


def first_sentence(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""
    match = re.search(r"^(.+?[.!?])(?:\s|$)", cleaned)
    return match.group(1) if match else cleaned


def shorten(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def lower_first(text: str) -> str:
    if not text:
        return text
    return text[0].lower() + text[1:]


def build_ui(skill_name: str, source_text: str, explicit: dict[str, str] | None = None) -> dict[str, str]:
    if explicit:
        return explicit

    meta, _ = parse_frontmatter(source_text)
    description = meta.get("description", "").strip()
    display_name = slug_to_title(skill_name)
    short_description = shorten(first_sentence(description) or display_name, 110)
    default_prompt = f"Use ${skill_name} when you need to {lower_first(short_description.rstrip('.'))}."
    return {
        "display_name": display_name,
        "short_description": short_description,
        "default_prompt": default_prompt,
    }


def write_openai_yaml(skill_dir: Path, ui: dict[str, str]) -> None:
    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    content = (
        "interface:\n"
        f"  display_name: {json.dumps(ui['display_name'])}\n"
        f"  short_description: {json.dumps(ui['short_description'])}\n"
        f"  default_prompt: {json.dumps(ui['default_prompt'])}\n"
    )
    (agents_dir / "openai.yaml").write_text(content, encoding="utf-8")


def copy_skill_directory(source_dir: Path, destination_skill: Path, skill_name: str, ui: dict[str, str]) -> None:
    shutil.copytree(source_dir, destination_skill)
    skill_file = destination_skill / "SKILL.md"
    if skill_file.exists():
        skill_text = skill_file.read_text(encoding="utf-8")
        skill_text = normalize_frontmatter_name(rewrite_skill_text(skill_text), skill_name)
        skill_file.write_text(skill_text, encoding="utf-8")
    write_openai_yaml(destination_skill, ui)


def build_command_wrapper(
    source_file: Path,
    destination_skill: Path,
    skill_name: str,
    plugin_name: str,
    command_name: str,
) -> None:
    source_text = source_file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(source_text)
    command_description = meta.get("description", f"Run the {plugin_name} {command_name} command playbook").strip()
    arg_hint = meta.get("argument-hint", "").strip()
    wrapper_description = (
        f"{command_description.rstrip('.')}. "
        f"Use when the user wants the Codex equivalent of the upstream `/{plugin_name}:{command_name}` command playbook."
    )
    wrapper_text = (
        f"---\n"
        f"name: {skill_name}\n"
        f"description: {wrapper_description}\n"
        f"---\n\n"
        f"# {slug_to_title(plugin_name)} / {slug_to_title(command_name)} Command Playbook\n\n"
        f"This installable skill wraps the exported command playbook from "
        f"`{source_file.relative_to(ROOT).as_posix()}`.\n\n"
    )
    if arg_hint:
        wrapper_text += f"Original argument hint: `{arg_hint}`.\n\n"
    wrapper_text += body.lstrip()

    destination_skill.mkdir(parents=True, exist_ok=True)
    (destination_skill / "SKILL.md").write_text(wrapper_text, encoding="utf-8")

    short_description = shorten(first_sentence(command_description), 110)
    display_name = f"{slug_to_title(plugin_name)} {slug_to_title(command_name)} Command"
    default_prompt = (
        f"Use ${skill_name} to run the {plugin_name} {command_name} playbook"
        + (f" for {arg_hint}." if arg_hint else ".")
    )
    write_openai_yaml(
        destination_skill,
        {
            "display_name": display_name,
            "short_description": short_description,
            "default_prompt": default_prompt,
        },
    )


def build_exported_skill_entries() -> list[dict[str, str]]:
    registry = read_json(EXPORT_REGISTRY)
    raw_entries: list[dict[str, str]] = []
    skill_name_counts: dict[str, int] = {}

    for plugin_name, plugin_data in sorted(registry["plugins"].items()):
        for skill in plugin_data.get("skills", []):
            base_name = skill["name"]
            if base_name in EXCLUDED_EXPORTED_SKILLS:
                continue
            skill_name_counts[base_name] = skill_name_counts.get(base_name, 0) + 1
            raw_entries.append(
                {
                    "kind": "exported_skill",
                    "base_name": base_name,
                    "plugin_name": plugin_name,
                    "source_path": skill["destination"],
                }
            )
        for command in plugin_data.get("commands", []):
            raw_entries.append(
                {
                    "kind": "command_wrapper",
                    "name": f"command-{plugin_name}-{command['name']}",
                    "plugin_name": plugin_name,
                    "command_name": command["name"],
                    "source_path": command["destination"],
                }
            )

    entries: list[dict[str, str]] = []
    for entry in raw_entries:
        if entry["kind"] == "command_wrapper":
            entries.append(entry)
            continue

        base_name = entry["base_name"]
        resolved_name = (
            base_name
            if skill_name_counts[base_name] == 1
            else f"{entry['plugin_name']}-{base_name}"
        )
        entries.append(
            {
                "kind": entry["kind"],
                "name": resolved_name,
                "plugin_name": entry["plugin_name"],
                "source_path": entry["source_path"],
            }
        )

    return entries


def build_workflow_entries() -> list[dict[str, str]]:
    coordinators = read_json(COORDINATORS_REGISTRY)["coordinators"]
    task_packs = read_json(TASK_PACKS_REGISTRY)["task_packs"]

    entries: list[dict[str, str]] = []
    for item in coordinators:
        entries.append(
            {
                "kind": "workflow_skill",
                "name": item["name"],
                "source_path": str(Path(item["entry_skill"]).parent),
            }
        )
    for item in task_packs:
        entries.append(
            {
                "kind": "workflow_skill",
                "name": item["name"],
                "source_path": str(Path(item["entry_skill"]).parent),
            }
        )
    return entries


def build_entries() -> list[dict[str, str]]:
    entries = build_workflow_entries() + build_exported_skill_entries()
    names = [entry["name"] for entry in entries]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate installable skill names: {', '.join(duplicates)}")
    return entries


def main() -> None:
    ensure_clean_skills_dir()
    entries = build_entries()

    exported_skill_count = 0
    workflow_skill_count = 0
    command_wrapper_count = 0

    for entry in entries:
        destination_skill = SKILLS_ROOT / entry["name"]
        source_path = ROOT / entry["source_path"]

        if entry["kind"] == "command_wrapper":
            build_command_wrapper(
                source_path,
                destination_skill,
                entry["name"],
                entry["plugin_name"],
                entry["command_name"],
            )
            command_wrapper_count += 1
            continue

        source_text = (source_path / "SKILL.md").read_text(encoding="utf-8")
        ui = build_ui(entry["name"], source_text, WORKFLOW_UI.get(entry["name"]))
        copy_skill_directory(source_path, destination_skill, entry["name"], ui)

        if entry["kind"] == "workflow_skill":
            workflow_skill_count += 1
        else:
            exported_skill_count += 1

    summary = {
        "plugin": "legal-services-codex",
        "workflow_skills": workflow_skill_count,
        "exported_skills": exported_skill_count,
        "command_wrappers": command_wrapper_count,
        "skill_count": len(entries),
        "skills": [entry["name"] for entry in entries],
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
