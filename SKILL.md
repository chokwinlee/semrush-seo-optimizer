---
name: semrush-seo-autofix
description: Parse SEMrush Site Audit CSV exports and execute prioritized SEO remediation workflows. Use whenever users share SEMrush issue data (CSV or pasted table), ask to fix technical SEO problems, need issue routing with playbook guidance, or want a structured remediation report. Also triggers on mentions of SEMrush site audit, SEO issue triage, crawlability fixes, structured data errors, or bulk SEO remediation.
---

# SEMrush SEO Autofix

Convert a SEMrush Site Audit export into a prioritized fix plan, execute the fixes, and produce an auditable report.

## How It Works

The skill routes each issue row through a machine-readable registry (`references/issue-registry.json`) that maps SEMrush issue IDs to domains, priorities, actionability tags, and playbooks. Issues the registry doesn't recognize are flagged — never silently skipped.

The registry covers 80+ SEMrush issue IDs across 9 domains: crawlability/indexing, HTTPS/security, metadata/content, structured data, performance, international SEO, internal linking, images/media, and AI search (GEO).

## When To Use

- User shares a SEMrush Site Audit CSV or pastes issue rows.
- User asks "fix my SEMrush issues" or similar.
- User wants to triage SEO issues by priority and actionability.

## Workflow

### 1. Route Issues

Run the routing script to parse the CSV and produce a prioritized queue:

```bash
python3 scripts/semrush_route.py \
  --input <csv-path> \
  --rules references/issue-registry.json \
  --output-json output/route.json \
  --output-md output/route.md
```

Add `--strict` to fail on unknown issue IDs (recommended for CI).

The script outputs:
- **JSON**: structured data with `prioritized_queue`, `unknown_issue_ids`, `manual_handoffs`
- **Markdown**: human-readable report with the same sections

### 2. Review the Queue

Read the routing output. Issues are sorted by priority bucket (P0 first), then severity, then volume. Each item includes:
- `priority`: P0 (crawl/index blockers) through P3 (low-impact content)
- `actionability`: `auto_fixable`, `semi_auto`, or `manual`
- `playbook`: which reference doc to follow

If there are unknown issue IDs, add them to `references/issue-registry.json` before proceeding. Don't guess — unknown issues must be explicitly classified.

### 3. Apply Fixes

Work through the queue in priority order. For each issue, read the corresponding playbook in `references/playbook-*.md`. The playbook tells you what to check, what to change, and how to validate.

If the project is Next.js on Vercel, also read `references/nextjs-vercel.md` for framework-specific guidance (metadata APIs, canonical URL patterns, robots/sitemap route handling).

Respect the actionability tags:
- **auto_fixable**: deterministic code/config edits — go ahead and apply
- **semi_auto**: partial automation possible, but confirm with the user
- **manual**: external/infra dependency — document as a handoff, don't attempt

### 4. Validate

After applying fixes:
- Run the project's lint and build
- Re-run the routing script if the input CSV changed
- Verify that fixed issues would no longer appear in a re-audit

### 5. Report

Produce a remediation report (see `assets/remediation-report-template.md`) covering:
- Which issues were fixed and what changed
- Validation results
- Manual handoffs with owner and required action
- Risks and follow-up items

## Hard Rules

- Never treat hidden/excluded SEMrush checks as a fix.
- Never claim an issue is resolved without validation evidence.
- Never apply content changes to pages with broken canonicals or blocked indexing — fix crawlability first.
- Escalate infra-owned issues (certificates, CDN, TLS, firewall) as manual handoffs.

## Reference Files

Read these as needed — they don't all need to be loaded upfront:

- `references/reference.md` — Input/output contracts, severity weights, priority definitions
- `references/issue-registry.json` — Machine-readable issue-to-domain-to-playbook mapping
- `references/playbook-*.md` — Domain-specific remediation strategies (9 files)
- `references/nextjs-vercel.md` — Next.js + Vercel adapter guidance
- `references/schemas.md` — JSON and Markdown output schemas
- `assets/remediation-report-template.md` — Report template
- `scripts/semrush_route.py` — CSV parser and issue router
- `scripts/validate_registry.py` — Registry integrity checker
