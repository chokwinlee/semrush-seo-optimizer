# Adapter: Next.js + Vercel

This adapter applies when the target repository is a Next.js project deployed on Vercel.

## Adapter Scope

- Metadata and canonical generation patterns
- robots and sitemap route handling
- internal link conventions in App Router
- static asset and route-level performance implications

## Adapter Rules

1. Prefer framework-native metadata APIs over ad-hoc tag injection.
2. Keep canonical URL construction centralized and deterministic.
3. Avoid client-only SEO fixes for pages that should render on the server.
4. Keep route-level SEO output stable between environments.
5. Apply minimal changes and preserve App Router idioms.

## Validation Expectations

- Build and lint pass after metadata/canonical changes.
- robots/sitemap endpoints remain valid.
- No regressions in route resolution for edited pages.
