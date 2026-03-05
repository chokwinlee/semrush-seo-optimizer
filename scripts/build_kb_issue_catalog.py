#!/usr/bin/env python3
"""Build a local issue catalog from SEMrush KB export text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def extract_issues(text: str) -> list[dict[str, str]]:
    lines = [line.rstrip() for line in text.splitlines()]
    issues: list[dict[str, str]] = []
    severity: str | None = None

    for idx, line in enumerate(lines):
        value = line.strip()
        if value == "### Errors":
            severity = "ERROR"
            continue
        if value == "### Warnings":
            severity = "WARNING"
            continue
        if value == "### Notices":
            severity = "NOTICE"
            continue
        if value != "About the issue":
            continue

        prev = idx - 1
        while prev >= 0 and not lines[prev].strip():
            prev -= 1
        if prev < 0:
            continue

        title = lines[prev].strip()
        if not title or title.startswith("###") or title in {"About the issue", "How to fix it"}:
            continue
        issues.append({"title": title, "severity": severity or "UNKNOWN"})

    # Deduplicate by title while preserving order.
    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for issue in issues:
        key = issue["title"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(issue)

    return deduped


def main() -> int:
    parser = argparse.ArgumentParser(description="Build KB issue catalog JSON.")
    parser.add_argument("--input", required=True, help="Path to fetched KB text file")
    parser.add_argument("--output", required=True, help="Path to output JSON catalog")
    parser.add_argument(
        "--source-url",
        default="https://www.semrush.com/kb/542-site-audit-issues-list",
        help="Source URL for metadata",
    )
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    issues = extract_issues(text)
    payload = {"source": args.source_url, "issues": issues}
    Path(args.output).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"OK: wrote {len(issues)} issues -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
