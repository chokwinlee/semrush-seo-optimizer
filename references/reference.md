# Reference

## Input Contract

Normalized columns:

- `issue_id` (int, required)
- `issue_type` (`ERROR|WARNING|NOTICE`, required)
- `issue_name` (string, required)
- `failed_checks` (int, required)
- `total_checks` (int, optional)
- `delta` (int, optional)

Accepted source formats:

- CSV file path
- CSV text pasted inline
- Tabular text converted to CSV before routing

## Severity and Priority

Severity weights:

- `ERROR = 100`
- `WARNING = 50`
- `NOTICE = 10`

Priority buckets:

- `P0`: crawlability/indexing blockers
- `P1`: protocol and canonical integrity
- `P2`: structured data, metadata uniqueness, internal links
- `P3`: low-impact content/readability items

Ordering inside same bucket:

1. Severity weight (desc)
2. `failed_checks` (desc)
3. `issue_id` (asc)

## Actionability Tags

- `auto_fixable`: deterministic code/config edits are available
- `semi_auto`: partial automation, human review required
- `manual`: external/infra dependent

## Unknown Issue Policy

When an issue is not in the registry:

1. Tag as `manual`
2. Add to `unknown_issue_ids` section in outputs
3. Exit non-zero if `--strict` mode is enabled
4. Update `references/issue-registry.json` in a dedicated PR before auto-fixing

## Official SEMrush Sources

- Issue guidance and categories: `https://www.semrush.com/kb/542-site-audit-issues-list`
- Issue ID and title API endpoint: `GET /reports/v1/projects/{ID}/siteaudit/meta/issues`
- Registry must be reviewed against official SEMrush sources before release.

## Output Contract

JSON output must include:

- `summary`
- `prioritized_queue`
- `by_domain`
- `unknown_issue_ids`
- `manual_handoffs`

Markdown report must include:

1. Input summary
2. Priority queue
3. Domain breakdown
4. Unknown issues
5. Manual handoffs
6. Validation checklist
