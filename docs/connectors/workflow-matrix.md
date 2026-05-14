# Workflow Matrix

| Workflow | Preferred connectors | Primary outputs | Notes |
| --- | --- | --- | --- |
| `renewal-watcher` | `ironclad`, `imanage`, `docusign`, `gdrive` | renewal alert memo | Computed dates are screening leads, not calendar entries. |
| `diligence-grid` | `box`, `imanage`, `definely`, `gdrive` | diligence grid CSV, sources CSV, summary memo | Sample before fan-out and preserve verbatim quote support. |
| `docket-watcher` | `trellis`, `courtlistener`, `gdrive` | docket status memo, deadline feed YAML | Deadline mapping always requires attorney verification. |
| `launch-radar` | `linear`, `atlassian`, `asana`, `gdrive` | launch triage memo | Triage is routing, not legal approval. |
| `reg-monitor` | `gdrive` plus reviewed feed inputs | regulatory digest, gap summary memo | Materiality and policy-gap flags are screening calls only. |
