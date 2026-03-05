#!/usr/bin/env python3
"""Validate issue-registry integrity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_ACTIONABILITY = {"auto_fixable", "semi_auto", "manual"}
VALID_PRIORITY = {"P0", "P1", "P2", "P3"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate issue registry schema.")
    parser.add_argument("--rules", required=True, help="Path to issue-registry.json")
    args = parser.parse_args()

    data = json.loads(Path(args.rules).read_text(encoding="utf-8"))
    domains = data.get("domains", {})
    issues = data.get("issues", {})

    errors: list[str] = []
    if not domains:
        errors.append("domains is empty")
    if not issues:
        errors.append("issues is empty")

    for domain, meta in domains.items():
        p = meta.get("priority")
        if p not in VALID_PRIORITY:
            errors.append(f"domain '{domain}' has invalid priority '{p}'")
        if not meta.get("playbook"):
            errors.append(f"domain '{domain}' missing playbook")

    for issue_id, meta in issues.items():
        if not issue_id.isdigit():
            errors.append(f"issue id '{issue_id}' is not numeric")
        domain = meta.get("domain")
        if domain not in domains:
            errors.append(f"issue '{issue_id}' references unknown domain '{domain}'")
        actionability = meta.get("actionability")
        if actionability not in VALID_ACTIONABILITY:
            errors.append(
                f"issue '{issue_id}' has invalid actionability '{actionability}'"
            )
        if not meta.get("name"):
            errors.append(f"issue '{issue_id}' missing name")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("OK: registry schema is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
