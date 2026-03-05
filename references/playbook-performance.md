# Playbook: Performance

## Official Basis

- SEMrush Site Audit categories: Performance, Technical SEO, AMP
- Source: https://www.semrush.com/kb/542-site-audit-issues-list
- Use the per-issue "How to fix it" guidance from SEMrush when deciding exact remediation.

## Root Causes

- broken asset references
- oversized HTML and JS or CSS payloads
- server, cache, or compression policy gaps
- viewport or mobile rendering configuration issues

## Allowed Auto Actions

- fix broken asset URLs in code-owned paths
- remove unnecessary inline payloads
- reduce obvious redirect chains in routing config
- add missing viewport declarations in owned templates

## Manual Escalation

- server compression and caching headers
- hosting, plugin, and runtime bottlenecks
- complex AMP rendering or templating issues

## Required Validation

- no broken JS and CSS links on fixed pages
- build artifacts validate referenced assets
- representative templates pass mobile viewport checks
