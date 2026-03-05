# Playbook: Crawlability and Indexing

## Official Basis

- SEMrush Site Audit category: Crawlability and Architecture
- Source: https://www.semrush.com/kb/542-site-audit-issues-list
- Use the per-issue "How to fix it" guidance from SEMrush when deciding exact remediation.

## Root Causes

- broken or invalid internal URLs
- robots.txt and sitemap misconfiguration
- canonical conflicts or invalid canonical targets
- indexability blocked by directives or headers

## Allowed Auto Actions

- fix malformed internal links
- repair robots and sitemap syntax or content
- remove duplicate canonical tags and enforce one canonical target
- replace meta refresh redirects with server redirects when possible

## Required Validation

- no broken internal link targets among fixed URLs
- sitemap contains canonical, indexable, `200` URLs
- canonical checks pass on edited pages
