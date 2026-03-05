# Playbook: Structured Data

## Target Issues

`45`

## Root Causes

- invalid schema properties
- missing required fields for rich-result eligibility
- conflicting or fragmented JSON-LD graphs

## Allowed Auto Actions

- remove invalid properties by `@type`
- add missing required fields when source data is available
- normalize graph structure for template consistency

## Required Validation

- pass Rich Results Test for affected templates/pages
- no blocking schema validation errors
