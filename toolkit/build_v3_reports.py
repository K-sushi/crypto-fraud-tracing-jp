from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build integrated v3 operational reports.")
    parser.add_argument("--structured-dir", default="artifacts/structured_reports")
    parser.add_argument("--dossier-dir", default="artifacts/case_dossiers")
    parser.add_argument("--lead-dir", default="artifacts/lead_packets")
    parser.add_argument("--snapshot-path", default="artifacts/current_state_snapshot.json")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--out-dir", default="reports_v3_drafts")
    return parser.parse_args()


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_dir_map(dir_path: Path) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if not dir_path.exists():
        return out
    for path in sorted(dir_path.glob("*.json")):
        data = load_json(path)
        case_id = data.get("case_id") or path.stem
        out[case_id] = data
    return out


def load_snapshot_map(path: Path) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    data = load_json(path)
    return {row.get("case_id"): row for row in data.get("cases", []) if row.get("case_id")}


def get_section(payload: Dict[str, Any], title_prefix: str) -> str:
    for section in payload.get("sections", []):
        title = str(section.get("title", "")).strip().lower()
        if title.startswith(title_prefix.lower()):
            return str(section.get("body", "")).strip()
    return ""


def get_standardized(payload: Dict[str, Any], key: str) -> str:
    section = payload.get("case_profile", {}).get("standardized_sections", {}).get(key, {})
    if isinstance(section, dict):
        return str(section.get("body", "")).strip()
    return ""


def first_nonempty(*values: str) -> str:
    for value in values:
        if str(value).strip():
            return str(value).strip()
    return ""


def normalize_path(path_str: str) -> str:
    return path_str.replace("\\", "/") if path_str else ""


def infer_v3_name(source_file: str) -> str:
    stem = Path(source_file).stem
    if stem.endswith("_v1"):
        return stem[:-3] + "_v3.md"
    return stem + "_v3.md"


def infer_reanalysis_report_path(case_id: str, reports_dir: Path) -> str:
    candidate = reports_dir / f"{case_id}.md"
    return normalize_path(str(candidate)) if candidate.exists() else case_id


def format_list(items: List[str], fallback: str = "- none") -> str:
    rows = [f"- {item}" for item in items if str(item).strip()]
    return "\n".join(rows) if rows else fallback


def format_addresses(items: List[str]) -> str:
    rows = [f"- `{item}`" for item in items if str(item).strip()]
    return "\n".join(rows) if rows else "- none"


def format_dimensions(scorecard: Dict[str, Any]) -> str:
    dimensions = scorecard.get("dimensions", {})
    ordered = [
        "provenance",
        "fund_flow_closure",
        "attribution_leverage",
        "freshness",
        "reproducibility",
        "machine_readability",
        "cross_case_schema",
        "presentation_quality",
        "legal_operational_packaging",
        "comparative_intelligence",
    ]
    lines = ["| Dimension | Score |", "|:---|---:|"]
    for key in ordered:
        if key in dimensions:
            lines.append(f"| `{key}` | {int(dimensions[key])} |")
    return "\n".join(lines)


def format_axes(scorecard: Dict[str, Any]) -> str:
    axes = scorecard.get("axes", {})
    ordered = ["artifact_ops", "live_intel", "action_economics"]
    lines = ["| Axis | Current | Max | Status |", "|:---|---:|---:|:---|"]
    for key in ordered:
        axis = axes.get(key, {})
        if axis:
            lines.append(
                f"| `{key}` | {int(axis.get('current_score', 0))} | {int(axis.get('max_score', 0))} | {axis.get('integration_status', 'unknown')} |"
            )
    return "\n".join(lines)


def format_reanalysis(dossier: Dict[str, Any], reports_dir: Path) -> str:
    items = dossier.get("linked_reanalysis", [])
    if not items:
        return "- linked reanalysis not available"
    rows = []
    for item in items:
        case_id = str(item.get("case_id") or "").strip()
        ref = infer_reanalysis_report_path(case_id, reports_dir)
        rows.append(
            "\n".join(
                [
                    f"- source: `{ref}`",
                    f"  - drift_zero: `{bool(item.get('has_drift_zero'))}`",
                    f"  - command_set: `{bool(item.get('has_command_set'))}`",
                    f"  - immutable_reference_count: `{int(item.get('immutable_reference_count') or 0)}`",
                ]
            )
        )
    return "\n".join(rows)


def build_report(
    payload: Dict[str, Any],
    dossier: Dict[str, Any],
    packet: Dict[str, Any],
    snapshot_case: Dict[str, Any],
    reports_dir: Path,
) -> str:
    scorecard = payload.get("scorecard", {})
    open_loops = snapshot_case.get("open_loops", [])
    exec_summary = first_nonempty(
        get_section(payload, "1. executive summary"),
        get_standardized(payload, "incident"),
    )
    delta_body = first_nonempty(
        get_standardized(payload, "delta_analysis"),
        get_section(payload, "8. delta analysis"),
    )
    limitations = first_nonempty(
        get_standardized(payload, "limitations"),
        get_section(payload, "16. limitations"),
    )
    next_steps = first_nonempty(
        get_section(payload, "17. next steps"),
        get_standardized(payload, "actionable_findings"),
        format_list(open_loops),
    )
    title = str(payload.get("title") or dossier.get("title") or "Integrated Operational Report")

    v1_source = normalize_path(payload.get("source_file", ""))
    v2_summary = format_reanalysis(dossier, reports_dir)
    html_path = normalize_path(dossier.get("report_artifacts", {}).get("html_artifact", {}).get("path", ""))
    dossier_path = f"artifacts/case_dossiers/{payload.get('case_id')}.json"
    lead_path = f"artifacts/lead_packets/{payload.get('case_id')}.json"
    snapshot_path = "artifacts/current_state_snapshot.json"

    monitored = snapshot_case.get("monitored_addresses", [])
    tier1 = packet.get("tier1_lead", {}) or snapshot_case.get("tier1_lead", {})
    execution = packet.get("execution_priority", {})
    recoverability = packet.get("recoverability", {})
    disclosure = packet.get("disclosure_readiness", {})
    monetization = packet.get("monetization_potential", {})

    return f"""# {title} - v3 Integrated Operational Report

**Document class:** `integrated_operational_report`  
**Case ID:** `{payload.get("case_id", "")}`  
**Source narrative:** `{v1_source}`  
**HTML artifact:** `{html_path}`  
**Snapshot artifact:** `{snapshot_path}`  
**Lead packet:** `{lead_path}`  
**Case dossier:** `{dossier_path}`

---

## 1. Executive Decision Summary

{exec_summary or "Executive summary not available."}

## 2. Case Status Now

- current scorecard total: `{int(scorecard.get("total", 0))}/10000`
- target_10000_gap: `{int(scorecard.get("target_10000_gap", 0))}`
- freshness_status: `{snapshot_case.get("freshness_status", "unknown")}`
- last_checked_utc: `{snapshot_case.get("last_checked_utc", "unknown")}`
- monitored address count: `{len(monitored)}`
- live_monitored_count: `{int(snapshot_case.get("live_monitored_count", 0))}`
- live_attempted_count: `{int(snapshot_case.get("live_attempted_count", 0))}`

## 3. What Remains Proven from v1

- narrative source: `{v1_source}`
- evidence chain count: `{len(dossier.get("evidence_chain", []))}`
- section coverage: `{int(dossier.get("section_coverage", 0))}`
- evidence chain coverage: `{int(dossier.get("evidence_chain_coverage", 0))}`
- key section keys:
{format_list([f"`{key}`" for key in dossier.get("standardized_section_keys", [])])}

## 4. What v2 Re-analysis Confirmed

{v2_summary}

## 5. Current State Snapshot

- address_state_coverage: `{int(dossier.get("address_state_coverage", 0))}`
- last_activity_coverage: `{int(dossier.get("last_activity_coverage", 0))}`
- last_outbound_coverage: `{int(dossier.get("last_outbound_coverage", 0))}`
- explorer_hits: `{int(dossier.get("operational_artifacts", {}).get("snapshot", {}).get("explorer_hits", 0))}`
- activity_rows: `{int(dossier.get("operational_artifacts", {}).get("snapshot", {}).get("activity_rows", 0))}`

Monitored addresses:
{format_addresses(monitored)}

## 6. Priority Lead and Why Now

- tier1_lead: `{tier1.get("label", "unknown")}`
- tier1_reason: {tier1.get("reason", "unknown")}
- disclosure_target: `{packet.get("disclosure_target", "unknown")}`
- request_basis: {packet.get("request_basis", "unknown")}
- why_now: {packet.get("why_now", "unknown")}

## 7. Recoverability and Action Path

- execution_priority: `{execution.get("label", "unknown")}` / score `{int(execution.get("score", 0))}`
- recoverability: `{recoverability.get("label", "unknown")}` / score `{int(recoverability.get("score", 0))}`
- disclosure_readiness: `{disclosure.get("status", "unknown")}` / support_strength `{int(disclosure.get("support_strength", 0))}`
- monetization_potential: `{monetization.get("trend", "unknown")}` / score `{int(monetization.get("score", 0))}`

Addresses of interest:
{format_addresses(packet.get("addresses_of_interest", []))}

## 8. Open Loops

{format_list(open_loops)}

## 9. Evidence and Immutable References

- source_sha256: `{payload.get("source_sha256", "")}`
- evidence_chain:
{format_list([f"`{item}`" for item in dossier.get("evidence_chain", [])])}

## 10. Confidence and Limits

### Current score axes

{format_axes(scorecard)}

### Current score dimensions

{format_dimensions(scorecard)}

### Limitations carried forward

{limitations or "Limitations section not available."}

## 11. Delta Since v1

{delta_body or "Delta section not available."}

## 12. Immediate Next Action

{next_steps or "Next steps section not available."}
"""


def main() -> None:
    args = parse_args()
    structured_dir = Path(args.structured_dir)
    dossier_map = load_dir_map(Path(args.dossier_dir))
    lead_map = load_dir_map(Path(args.lead_dir))
    snapshot_map = load_snapshot_map(Path(args.snapshot_path))
    reports_dir = Path(args.reports_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for path in sorted(structured_dir.glob("*.json")):
        payload = load_json(path)
        case_id = payload.get("case_id")
        if not case_id:
            continue
        dossier = dossier_map.get(case_id, {})
        packet = lead_map.get(case_id, {})
        snapshot_case = snapshot_map.get(case_id, {})
        text = build_report(payload, dossier, packet, snapshot_case, reports_dir)
        out_name = infer_v3_name(payload.get("source_file", path.stem))
        (out_dir / out_name).write_text(text, encoding="utf-8")
        count += 1

    print(f"Wrote {count} v3 report(s) to {out_dir}.")


if __name__ == "__main__":
    main()
