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

SYNTHETIC_SKILLS = [
    {
        "name": "00-legal-services-index",
        "mode": "index",
        "display_name": "Legal Services Index",
        "short_description": "Browse the plugin's main practice areas and entry skills",
        "default_prompt": "Use $00-legal-services-index to find the right legal-services skill for a task.",
    },
    {
        "name": "01-commercial-legal-review",
        "mode": "alias",
        "target_skill": "review",
        "display_name": "Commercial Legal Review",
        "short_description": "Route and review inbound commercial agreements",
        "default_prompt": "Use $01-commercial-legal-review to review an inbound MSA, NDA, or SaaS agreement.",
    },
    {
        "name": "02-corporate-legal-tabular-review",
        "mode": "alias",
        "target_skill": "tabular-review",
        "display_name": "Corporate Legal Tabular Review",
        "short_description": "Run cited diligence review over a document set",
        "default_prompt": "Use $02-corporate-legal-tabular-review to build a cited diligence grid from a VDR folder.",
    },
    {
        "name": "03-privacy-legal-dsar-response",
        "mode": "alias",
        "target_skill": "dsar-response",
        "display_name": "Privacy Legal DSAR Response",
        "short_description": "Draft first-pass DSAR responses with review framing",
        "default_prompt": "Use $03-privacy-legal-dsar-response to draft a first-pass DSAR response.",
    },
    {
        "name": "04-product-legal-launch-review",
        "mode": "alias",
        "target_skill": "launch-review",
        "display_name": "Product Legal Launch Review",
        "short_description": "Review launches against product-legal calibration",
        "default_prompt": "Use $04-product-legal-launch-review to review a product launch for legal risk.",
    },
    {
        "name": "05-litigation-legal-claim-chart",
        "mode": "alias",
        "target_skill": "claim-chart",
        "display_name": "Litigation Legal Claim Chart",
        "short_description": "Build claim charts for patent or civil matters",
        "default_prompt": "Use $05-litigation-legal-claim-chart to build a claim chart from asserted claims and source materials.",
    },
    {
        "name": "06-employment-legal-termination-review",
        "mode": "alias",
        "target_skill": "termination-review",
        "display_name": "Employment Legal Termination Review",
        "short_description": "Review proposed terminations against jurisdiction-specific flags",
        "default_prompt": "Use $06-employment-legal-termination-review to review a proposed employee termination.",
    },
    {
        "name": "07-ip-legal-clearance",
        "mode": "alias",
        "target_skill": "clearance",
        "display_name": "IP Legal Clearance",
        "short_description": "Run first-pass trademark clearance screening",
        "default_prompt": "Use $07-ip-legal-clearance to run a first-pass trademark clearance screen.",
    },
    {
        "name": "08-regulatory-legal-reg-feed-watcher",
        "mode": "alias",
        "target_skill": "reg-feed-watcher",
        "display_name": "Regulatory Legal Feed Watcher",
        "short_description": "Check tracked regulatory feeds and summarize changes",
        "default_prompt": "Use $08-regulatory-legal-reg-feed-watcher to summarize what's new in the tracked regulatory feeds.",
    },
    {
        "name": "09-ai-governance-legal-use-case-triage",
        "mode": "alias",
        "target_skill": "ai-governance-legal-use-case-triage",
        "display_name": "AI Governance Legal Use Case Triage",
        "short_description": "Triage proposed AI use cases against governance rules",
        "default_prompt": "Use $09-ai-governance-legal-use-case-triage to classify a proposed AI use case against governance requirements.",
    },
    {
        "name": "10-legal-clinic-client-intake",
        "mode": "alias",
        "target_skill": "client-intake",
        "display_name": "Legal Clinic Client Intake",
        "short_description": "Run structured clinic intake with issue spotting",
        "default_prompt": "Use $10-legal-clinic-client-intake to run a structured clinic intake.",
    },
    {
        "name": "11-law-student-socratic-drill",
        "mode": "alias",
        "target_skill": "socratic-drill",
        "display_name": "Law Student Socratic Drill",
        "short_description": "Run Socratic drilling without giving away the answer",
        "default_prompt": "Use $11-law-student-socratic-drill to practice Socratic questioning on a doctrine.",
    },
    {
        "name": "12-legal-builder-hub-skill-installer",
        "mode": "alias",
        "target_skill": "skill-installer",
        "display_name": "Legal Builder Hub Skill Installer",
        "short_description": "Install community legal skills with trust checks",
        "default_prompt": "Use $12-legal-builder-hub-skill-installer to install a community legal skill with review gates.",
    },
]


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


def write_synthetic_skill(skill_dir: Path, name: str, description: str, body: str, ui: dict[str, str]) -> None:
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = (
        f"---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"---\n\n"
        f"{body.rstrip()}\n"
    )
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    write_openai_yaml(skill_dir, ui)


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
    synthetic_skill_count = 0

    for entry in SYNTHETIC_SKILLS:
        destination_skill = SKILLS_ROOT / entry["name"]
        ui = {
            "display_name": entry["display_name"],
            "short_description": entry["short_description"],
            "default_prompt": entry["default_prompt"],
        }
        if entry["mode"] == "index":
            description = "Start here to browse the main legal-services practice areas, workflows, and entry skills."
            body = """# Legal Services Index

Use this discovery skill when you want help choosing the right skill from the full legal-services corpus.

Recommended entrypoints by area:

- Commercial legal: `$01-commercial-legal-review`, `$review`, `$nda-review`, `$vendor-agreement-review`
- Corporate legal: `$02-corporate-legal-tabular-review`, `$tabular-review`, `$written-consent`, `$closing-checklist`
- Privacy legal: `$03-privacy-legal-dsar-response`, `$dsar-response`, `$dpa-review`, `$privacy-legal-use-case-triage`
- Product legal: `$04-product-legal-launch-review`, `$launch-review`, `$is-this-a-problem`, `$marketing-claims-review`
- Litigation legal: `$05-litigation-legal-claim-chart`, `$claim-chart`, `$matter-intake`, `$subpoena-triage`
- Employment legal: `$06-employment-legal-termination-review`, `$termination-review`, `$hiring-review`, `$worker-classification`
- IP legal: `$07-ip-legal-clearance`, `$clearance`, `$oss-review`, `$takedown`
- Regulatory legal: `$08-regulatory-legal-reg-feed-watcher`, `$reg-feed-watcher`, `$policy-diff`, `$gaps`
- AI governance legal: `$09-ai-governance-legal-use-case-triage`, `$ai-governance-legal-use-case-triage`, `$aia-generation`, `$vendor-ai-review`
- Legal clinic: `$10-legal-clinic-client-intake`, `$client-intake`, `$memo`, `$deadlines`
- Law student: `$11-law-student-socratic-drill`, `$socratic-drill`, `$bar-prep-questions`, `$outline-builder`
- Community skill workflows: `$12-legal-builder-hub-skill-installer`, `$registry-browser`, `$skills-qa`

Managed workflow packs:

- `$diligence-grid`
- `$docket-watcher`
- `$launch-radar`
- `$reg-monitor`
- `$renewal-watcher`

If the user's intent is ambiguous, route them to the closest practice-area entrypoint above rather than guessing a niche skill immediately.
"""
        else:
            target = entry["target_skill"]
            description = f"Alias skill for `${target}`. Use this discoverability wrapper when the explicit practice-area-prefixed name is clearer."
            body = f"""# {entry['display_name']}

This is a discoverability alias for `${target}`.

Use it when the explicit practice-area-prefixed entrypoint is clearer than the underlying base skill name.

When invoked:

1. Treat `${target}` as the canonical underlying skill.
2. Follow the full workflow and constraints from `${target}`.
3. Preserve the same review framing, source discipline, and connector assumptions as the underlying skill.
"""

        write_synthetic_skill(destination_skill, entry["name"], description, body, ui)
        synthetic_skill_count += 1

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
        "synthetic_skills": synthetic_skill_count,
        "workflow_skills": workflow_skill_count,
        "exported_skills": exported_skill_count,
        "command_wrappers": command_wrapper_count,
        "skill_count": len(entries) + synthetic_skill_count,
        "skills": [entry["name"] for entry in SYNTHETIC_SKILLS] + [entry["name"] for entry in entries],
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
