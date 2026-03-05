# Playbook: Structured Data

## Official Basis

- SEMrush Site Audit category: Structured data markup validation checks
- Source: https://www.semrush.com/kb/542-site-audit-issues-list
- Use the per-issue "How to fix it" guidance from SEMrush when deciding exact remediation.

## Root Causes

- invalid schema properties
- missing required fields for rich result eligibility
- conflicting or fragmented JSON-LD graphs

## Allowed Auto Actions

- remove invalid properties by `@type`
- add missing required fields when source data is available
- normalize graph structure for template consistency

## Required Validation

- pass Rich Results Test for affected templates or pages
- no blocking schema validation errors
