#!/usr/bin/env python3
"""Validate issue-registry integrity."""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
from pathlib import Path

VALID_ACTIONABILITY = {"auto_fixable", "semi_auto", "manual"}
VALID_PRIORITY = {"P0", "P1", "P2", "P3"}


def load_official_issues_from_csv(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        issues: dict[str, str] = {}
        for row in reader:
            issue_id = str(row.get("Issue Id", "")).strip()
            issue_name = str(row.get("Issue", "")).strip()
            if issue_id.isdigit() and issue_name:
                issues[issue_id] = issue_name
    return issues


def load_official_issues_from_meta_json(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("issues", [])
    issues: dict[str, str] = {}
    for item in items:
        issue_id = str(item.get("id", "")).strip()
        title = str(item.get("title", "")).strip()
        if issue_id.isdigit() and title:
            issues[issue_id] = title
    return issues


def load_official_issues_from_kb_catalog(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("issues", [])
    issues: dict[str, str] = {}
    for idx, item in enumerate(items):
        title = str(item.get("title", "")).strip()
        if title:
            issues[f"kb_{idx + 1}"] = title
    return issues


def normalize_issue_name(text: str) -> str:
    value = text.strip().lower()
    value = value.replace("’", "'").replace("`", "")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    replacements = {
        "format errors in ": "invalid ",
        "size of html on a page is too large": "large html page size",
        "no redirect or canonical to https homepage from http version": "neither canonical url nor 301 redirect from http homepage",
        "amp pages with html issues": "amp pages with html issues",
        "amp pages with style and layout issues": "amp pages with style and layout issues",
        "amp pages with templating issues": "amp pages with templating issues",
        "pages couldn t be crawled": "pages not crawled",
        "pages couldn t be crawled dns resolution issues": "dns resolution issue",
        "pages couldn t be crawled incorrect url formats": "we couldn t open the page s url",
        "pages not crawled dns resolution issues": "dns resolution issue",
        "pages don t have title tags": "title tag is missing or empty",
        "5xx status code": "5xx errors",
        "4xx status code": "4xx errors",
        "pages returning 5xx status code": "5xx errors",
        "pages returning 4xx status code": "4xx errors",
        "pages returning 5xx errors": "5xx errors",
        "pages returning 4xx errors": "4xx errors",
        "dns resolution issues": "dns resolution issue",
        "incorrect url formats": "we couldn t open the page s url",
        "too much text within the title tags": "title element is too long",
        "without enough text within the title tags": "title element is too short",
        "without an h1 heading": "missing h1",
        "too many parameters in their urls": "too many url parameters",
        "without character encoding declared": "encoding not declared",
        "blocked internal resources in robots txt": "disallowed internal resources",
        "javascript and css total size that is too large": "too large javascript and css total size",
        "more than one h1 tag": "multiple h1 tags",
        "blocked external resources in robots txt": "disallowed external resources",
        "issues with duplicate title tags": "duplicate title tag",
        "pages with duplicate content issues": "duplicate content",
        "format errors in robots txt file": "invalid robots txt format",
        "format errors in sitemap xml files": "invalid sitemap xml format",
        "pages with a www resolve issue": "www resolve issues",
        "pages with no viewport tag": "viewport not configured",
        "amp pages with no canonical tag": "missing canonical tags in amp pages",
        "issues with expiring or expired certificate": "certificate expiration",
        "issues with incorrect certificate name": "certificate registered to incorrect name",
        "pages with a meta refresh tag": "meta refresh redirects",
        "invalid structured data items": "structured data that contains markup errors",
        "missing the viewport width value": "viewport width not set",
        "pages with too much text within the title tags": "title element is too long",
        "pages without enough text within the title tags": "title element is too short",
        "pages without an h1 heading": "missing h1",
        "images without alt attributes": "missing alt attributes",
        "pages with too many parameters in their urls": "too many url parameters",
        "pages without character encoding declared": "encoding not declared",
        "pages containing frames": "frames used",
        "internal links containing nofollow attribute": "nofollow attributes in internal links",
        "subdomains don t support sni": "no sni support",
        "homepage does not use https encryption": "https encryption not used",
        "links on https pages leading to http page": "links lead to http pages for https site",
        "issues with blocked internal resources in robots txt": "disallowed internal resources",
        "pages have a javascript and css total size that is too large": "too large javascript and css total size",
        "pages with only one incoming internal linksource formatted as page link": "pages with only one internal link",
        "pages that need more than 3 clicks to be reached": "page crawl depth",
        "outgoing external links containing no follow attributes": "nofollow attributes in external links",
        "subdomains don t support hsts": "no hsts support",
        "urls longer than 200 characters": "too long urls",
        "pages with more than one h1 tag": "multiple h1 tags",
        "orphaned pages in sitemap": "orphaned sitemap pages",
        "issues with blocked external resources in robots txt": "disallowed external resources",
        "no viewport tag": "viewport not configured",
        "amp pages with no canonical tag": "missing canonical tags in amp pages",
        "amp page has no canonical tag": "missing canonical tags in amp pages",
        "expiring or expired certificate": "certificate expiration",
        "old security protocol": "old security protocol version",
        "incorrect certificate name": "certificate registered to incorrect name",
        "broken canonical link": "broken canonical urls",
        "slow load speed": "slow page load speed",
        "meta refresh tag": "meta refresh redirects",
        "duplicate h1 and title tags": "duplicate content in h1 and title",
        "underscore in the url": "underscores in url",
        "low word count": "low word count",
        "pages with a low word count": "low word count",
        "without enough text within the title tags": "title element is too short",
        "without an h1 heading": "missing h1",
        "without character encoding declared": "encoding not declared",
        "without doctype declared": "doctype not declared",
        "pages without enough text within the title tags": "title element is too short",
        "pages without an h1 heading": "missing h1",
        "pages without character encoding declared": "encoding not declared",
        "one incoming internal linksource formatted as page link": "pages with only one internal link",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def validate_official_coverage(
    registry_issues: dict[str, dict], official_issues: dict[str, str], *, fuzzy_names: bool
) -> list[str]:
    errors: list[str] = []
    normalized_registry_names = [
        normalize_issue_name(str(meta.get("name", "")))
        for meta in registry_issues.values()
        if str(meta.get("name", "")).strip()
    ]
    normalized_registry_name_set = set(normalized_registry_names)
    for issue_id, official_name in official_issues.items():
        registry_meta = registry_issues.get(issue_id)
        if registry_meta is not None:
            registry_name = str(registry_meta.get("name", "")).strip()
            if registry_name != official_name:
                if not (
                    fuzzy_names
                    and normalize_issue_name(registry_name)
                    == normalize_issue_name(official_name)
                ):
                    errors.append(
                        "name mismatch for issue "
                        f"'{issue_id}' (registry='{registry_name}', official='{official_name}')"
                    )
            continue

        if fuzzy_names:
            normalized_official = normalize_issue_name(official_name)
            if normalized_official in normalized_registry_name_set:
                continue
            best_ratio = 0.0
            for normalized_registry in normalized_registry_names:
                ratio = difflib.SequenceMatcher(
                    None, normalized_official, normalized_registry
                ).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
            if best_ratio >= 0.72:
                continue

        errors.append(f"registry missing official issue '{issue_id}: {official_name}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate issue registry schema.")
    parser.add_argument("--rules", required=True, help="Path to issue-registry.json")
    parser.add_argument(
        "--official-csv",
        help=(
            "Optional SEMrush export CSV path for coverage validation "
            "(expects 'Issue Id' and 'Issue' columns)."
        ),
    )
    parser.add_argument(
        "--official-meta-json",
        help=(
            "Optional JSON from SEMrush /siteaudit/meta/issues endpoint "
            "for official ID/title coverage validation."
        ),
    )
    parser.add_argument(
        "--official-kb-catalog",
        help=(
            "Optional KB issue catalog JSON (references/semrush-kb-issue-catalog.json) "
            "for fuzzy title-coverage validation."
        ),
    )
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

    official_issues: dict[str, str] = {}
    if args.official_csv:
        official_issues.update(load_official_issues_from_csv(Path(args.official_csv)))
    if args.official_meta_json:
        official_issues.update(
            load_official_issues_from_meta_json(Path(args.official_meta_json))
        )
    if args.official_kb_catalog:
        official_issues.update(
            load_official_issues_from_kb_catalog(Path(args.official_kb_catalog))
        )
    if official_issues:
        errors.extend(
            validate_official_coverage(
                issues,
                official_issues,
                fuzzy_names=bool(args.official_kb_catalog),
            )
        )

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("OK: registry schema is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
