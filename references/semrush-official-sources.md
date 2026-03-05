# SEMrush Official Sources

Use these sources as the canonical reference when updating issue mappings or playbook guidance.

## 1) Issue guidance and categories

- URL: https://www.semrush.com/kb/542-site-audit-issues-list
- Contains:
  - category-level framing (Crawlability, On Page SEO, Content, Technical SEO, HTTPS, International SEO, AMP, Performance, Internal Linking, AI Search)
  - per-issue "About the issue" and "How to fix it" sections

## 2) Official issue ID and title list

- API endpoint: `GET /reports/v1/projects/{ID}/siteaudit/meta/issues`
- Doc: https://developer.semrush.com/api/v3/projects/site-audit/
- Contains:
  - official issue IDs
  - issue titles

## 3) Registry maintenance workflow

1. Prefer API `meta/issues` output for ID-title completeness.
2. Align domain mapping with categories in the SEMrush KB issue catalog.
3. Keep `references/issue-registry.json` as the local runtime source of truth.
4. Validate with:

```bash
python3 scripts/validate_registry.py \
  --rules references/issue-registry.json \
  --official-csv "<semrush-export>.csv"
```

If API output is available, also pass:

```bash
python3 scripts/validate_registry.py \
  --rules references/issue-registry.json \
  --official-meta-json "<meta-issues>.json"
```

For KB-title based coverage checks, generate and validate against a local catalog:

```bash
python3 scripts/build_kb_issue_catalog.py \
  --input "<kb-fetch>.txt" \
  --output references/semrush-kb-issue-catalog.json
```

```bash
python3 scripts/validate_registry.py \
  --rules references/issue-registry.json \
  --official-kb-catalog references/semrush-kb-issue-catalog.json
```
