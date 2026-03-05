# Schemas

## Routing Output JSON

`semrush_route.py` writes:

```json
{
  "summary": {
    "rows_total": 0,
    "rows_invalid": 0,
    "rows_actionable": 0,
    "unknown_issue_count": 0
  },
  "prioritized_queue": [
    {
      "issue_id": 16,
      "issue_type": "ERROR",
      "issue_name": "Invalid robots.txt format",
      "failed_checks": 1,
      "domain": "crawlability_indexing",
      "priority": "P0",
      "playbook": "playbook-crawlability.md",
      "actionability": "auto_fixable",
      "score": 106.021
    }
  ],
  "by_domain": {},
  "unknown_issue_ids": [],
  "manual_handoffs": []
}
```

## Routing Output Markdown Sections

Required headings:

1. `Input Summary`
2. `Priority Queue`
3. `Unknown Issue IDs`
4. `Manual Handoffs`
5. `Validation Checklist`

## Registry JSON Minimum Fields

- top-level: `version`, `domains`, `issues`
- each domain: `priority`, `playbook`
- each issue: `name`, `domain`, `actionability`
