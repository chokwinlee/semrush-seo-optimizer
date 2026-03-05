# Playbook: AI Search / GEO

## Official Basis

- SEMrush Site Audit category: AI Search (Generative Engine Optimization)
- Source: https://www.semrush.com/kb/542-site-audit-issues-list
- Use the per-issue "How to fix it" guidance from SEMrush when deciding exact remediation.

## Root Causes

- missing or invalid `llms.txt`
- low semantic HTML structure
- inconsistent AI crawler access strategy

## Allowed Auto Actions

- create or fix `llms.txt` formatting
- improve semantic layout in templates (`main`, `article`, heading hierarchy)

## Manual Decisions

- bot allow and deny policies must align with business and legal requirements

## Required Validation

- `llms.txt` is reachable at root and syntactically valid
- semantic structure checks pass on target templates
