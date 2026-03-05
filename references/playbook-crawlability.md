# Playbook: Crawlability and Indexing

## Target Issues

`1,2,4,8,9,10,11,16,17,18,19,38,39,40,44,109,124,125,203,209`

## Root Causes

- Broken/invalid internal URLs
- robots/sitemap misconfiguration
- canonical conflicts or invalid canonical targets
- indexability blocked by directives/headers

## Allowed Auto Actions

- Fix malformed internal links
- Repair robots and sitemap syntax/content
- Remove duplicate canonical tags; enforce one canonical target
- Replace meta refresh with server redirects where possible

## Required Validation

- No broken internal link targets among fixed URLs
- Sitemap contains canonical, indexable, `200` URLs
- Canonical checks pass on edited pages
