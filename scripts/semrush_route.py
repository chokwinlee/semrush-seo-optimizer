#!/usr/bin/env python3
"""Parse SEMrush issue CSV and route issues via registry rules."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

SEVERITY_WEIGHT = {"ERROR": 100, "WARNING": 50, "NOTICE": 10}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

HEADER_ALIASES = {
    "Issue Id": "issue_id",
    "Issue Type": "issue_type",
    "Issue": "issue_name",
    "Failed checks": "failed_checks",
    "Total checks": "total_checks",
    "Changed from last audit": "delta",
}


def normalize_header(name: str) -> str:
    return HEADER_ALIASES.get(name.strip(), name.strip().lower().replace(" ", "_"))


def parse_int(value: str | None, default: int | None = None) -> int | None:
    if value is None:
        return default
    text = str(value).strip()
    if text == "":
        return default
    try:
        return int(text)
    except ValueError:
        return default


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return []
        normalized_fields = [normalize_header(h) for h in reader.fieldnames]
        for raw in reader:
            row = {}
            for original, normalized in zip(reader.fieldnames, normalized_fields):
                row[normalized] = raw.get(original)
            rows.append(row)
    return rows


def resolve_domain(issue_name: str, fallback_keywords: dict[str, str]) -> str | None:
    issue_l = issue_name.lower()
    for keyword, domain in fallback_keywords.items():
        if keyword.lower() in issue_l:
            return domain
    return None


def compute_score(issue_type: str, failed_checks: int) -> float:
    weight = SEVERITY_WEIGHT.get(issue_type, 0)
    return weight + math.log10(failed_checks + 1) * 20


def route(rows: list[dict[str, Any]], registry: dict[str, Any]) -> dict[str, Any]:
    issues = registry["issues"]
    domains = registry["domains"]
    fallback_keywords = registry.get("fallback_keywords", {})

    prioritized_queue: list[dict[str, Any]] = []
    unknown_issue_ids: list[int] = []
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    manual_handoffs: list[dict[str, Any]] = []

    invalid_rows = 0
    for row in rows:
        issue_id = parse_int(row.get("issue_id"))
        issue_type = str(row.get("issue_type", "")).strip().upper()
        issue_name = str(row.get("issue_name", "")).strip()
        failed_checks = parse_int(row.get("failed_checks"))

        if issue_id is None or issue_type not in SEVERITY_WEIGHT or failed_checks is None:
            invalid_rows += 1
            continue
        if failed_checks <= 0:
            continue

        meta = issues.get(str(issue_id))
        domain = None
        actionability = "manual"
        if meta is not None:
            domain = meta["domain"]
            actionability = meta["actionability"]
        else:
            unknown_issue_ids.append(issue_id)
            domain = resolve_domain(issue_name, fallback_keywords)
            if domain is None:
                domain = "unmapped"

        priority = domains.get(domain, {}).get("priority", "P3")
        playbook = domains.get(domain, {}).get("playbook")
        item = {
            "issue_id": issue_id,
            "issue_type": issue_type,
            "issue_name": issue_name,
            "failed_checks": failed_checks,
            "domain": domain,
            "priority": priority,
            "playbook": playbook,
            "actionability": actionability,
            "score": round(compute_score(issue_type, failed_checks), 3),
        }
        prioritized_queue.append(item)
        by_domain[domain].append(item)

        if actionability == "manual":
            manual_handoffs.append(
                {
                    "issue_id": issue_id,
                    "issue_name": issue_name,
                    "owner": "platform_or_seo_ops",
                    "reason": "No deterministic in-repo fix",
                }
            )

    prioritized_queue.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x["priority"], 99),
            -SEVERITY_WEIGHT.get(x["issue_type"], 0),
            -x["failed_checks"],
            x["issue_id"],
        )
    )

    summary = {
        "rows_total": len(rows),
        "rows_invalid": invalid_rows,
        "rows_actionable": len(prioritized_queue),
        "unknown_issue_count": len(set(unknown_issue_ids)),
    }
    return {
        "summary": summary,
        "prioritized_queue": prioritized_queue,
        "by_domain": dict(by_domain),
        "unknown_issue_ids": sorted(set(unknown_issue_ids)),
        "manual_handoffs": manual_handoffs,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    lines = ["# SEMrush Routing Report", ""]
    s = payload["summary"]
    lines.extend(
        [
            "## Input Summary",
            f"- Rows total: {s['rows_total']}",
            f"- Rows invalid: {s['rows_invalid']}",
            f"- Actionable rows: {s['rows_actionable']}",
            f"- Unknown issue IDs: {s['unknown_issue_count']}",
            "",
            "## Priority Queue",
        ]
    )
    for item in payload["prioritized_queue"]:
        lines.append(
            f"- [#{item['issue_id']}] {item['issue_name']} | {item['issue_type']} | "
            f"{item['priority']} | {item['domain']} | {item['actionability']}"
        )
    lines.append("")

    lines.append("## Unknown Issue IDs")
    if payload["unknown_issue_ids"]:
        lines.append("- " + ", ".join(str(x) for x in payload["unknown_issue_ids"]))
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Manual Handoffs")
    if payload["manual_handoffs"]:
        for handoff in payload["manual_handoffs"]:
            lines.append(
                f"- [#{handoff['issue_id']}] {handoff['issue_name']} -> {handoff['owner']} "
                f"({handoff['reason']})"
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Validation Checklist")
    lines.extend(
        [
            "- [ ] Lint/build checks passed after changes",
            "- [ ] SEO checks re-run",
            "- [ ] Unknown issues reviewed",
        ]
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Route SEMrush issues by registry rules.")
    parser.add_argument("--input", required=True, help="Path to SEMrush CSV export")
    parser.add_argument("--rules", required=True, help="Path to issue-registry.json")
    parser.add_argument("--output-json", required=True, help="Output path for JSON")
    parser.add_argument("--output-md", required=True, help="Output path for markdown")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when unknown issue IDs are detected.",
    )
    args = parser.parse_args()

    rows = read_rows(Path(args.input))
    registry = load_registry(Path(args.rules))
    payload = route(rows, registry)

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(to_markdown(payload), encoding="utf-8")

    if args.strict and payload["unknown_issue_ids"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
