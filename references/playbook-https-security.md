# Playbook: HTTPS and Security

## Target Issues

`26,27,28,29,30,31,32,42,126,127,128,205`

## Root Causes

- HTTP remnants on HTTPS site
- mixed-content assets
- missing redirect/canonical migration controls
- certificate/protocol/server policy problems

## Allowed Auto Actions

- Rewrite internal HTTP links to HTTPS
- Replace mixed content references where source is in repository
- Align sitemap URL protocol with canonical site protocol

## Manual Escalation

- Certificates, TLS versions, cipher suites, HSTS, SNI, WAF/CDN restrictions

## Required Validation

- No HTTP internal references in fixed pages
- Mixed-content checks pass on touched templates/routes
