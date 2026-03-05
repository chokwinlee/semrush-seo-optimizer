# Playbook: Performance

## Target Issues

`21,33,41,111,129,130,131,132,133,134,135,208`

## Root Causes

- broken asset references
- oversized HTML and JS/CSS payloads
- server/cache/compression policy gaps

## Allowed Auto Actions

- fix broken asset URLs in code-owned paths
- remove unnecessary inline payloads
- reduce obvious redirect chains in routing config

## Manual Escalation

- server compression/caching headers
- hosting and runtime bottlenecks

## Required Validation

- no broken JS/CSS links on fixed pages
- build artifacts validate referenced assets
