# Playbook: Internal Linking and Architecture

## Target Issues

`108,122,123,136,201,206,207,212,213,214,215,216,217`

## Root Causes

- weak internal graph and high click depth
- anchor quality issues
- nofollow misuse on internal links
- resource links encoded as page links

## Allowed Auto Actions

- remove unintended `nofollow` in internal links
- replace empty/non-descriptive anchor text when intent is clear
- add strategic links to high-value orphan/low-link pages

## Required Validation

- incoming internal links increase for targeted pages
- anchor-text quality checks pass for edited links
