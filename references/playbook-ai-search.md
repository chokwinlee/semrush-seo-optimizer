# Playbook: AI Search / GEO

## Target Issues

`137,219,222`

## Root Causes

- missing/invalid `llms.txt`
- low semantic HTML structure
- inconsistent AI crawler access strategy

## Allowed Auto Actions

- create/fix `llms.txt` formatting
- improve semantic layout in templates (`main`, `article`, heading hierarchy)

## Manual Decisions

- bot allow/deny policies must align with business/legal requirements

## Required Validation

- `llms.txt` is reachable at root and syntactically valid
- semantic structure checks pass on target templates
