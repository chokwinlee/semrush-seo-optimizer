# Playbook: HTTPS and Security

## Official Basis

- SEMrush Site Audit category: HTTPS Implementation
- Source: https://www.semrush.com/kb/542-site-audit-issues-list
- Use the per-issue "How to fix it" guidance from SEMrush when deciding exact remediation.

## Root Causes

- HTTP remnants on an HTTPS site
- mixed-content assets
- missing redirect or canonical migration controls
- certificate, protocol, or server policy problems

## Allowed Auto Actions

- rewrite internal HTTP links to HTTPS
- replace mixed-content references where source is in repository
- align sitemap URL protocol with canonical site protocol

## Manual Escalation

- certificates, TLS versions, cipher suites, HSTS, SNI, WAF, or CDN restrictions

## Required Validation

- no HTTP internal references in fixed pages
- mixed-content checks pass on touched templates or routes
