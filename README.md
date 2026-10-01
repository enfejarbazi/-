# راهنمای فارسی بازی و سواد دیجیتال

A fast, dependency-free Persian editorial site hosted on GitHub Pages.

## Editing and building

Edit editorial content in `scripts/content.py`, shared templates in
`scripts/build_site.py`, and styles in `assets/css/site.css`.

```bash
python scripts/build_site.py
python scripts/validate_site.py
node scripts/test_tools.cjs
```

Commit generated HTML together with its source. GitHub Pages serves the files
directly; no package install, bundler, JavaScript rendering, or third-party font
request is required. Keep `.nojekyll`.

## Content and search

Existing routes are preserved. Indexable pages have unique titles/descriptions,
canonical URLs, social metadata and JSON-LD. Collection pages connect the topics.
Search and 404 pages are noindex and excluded from the sitemap. Update the actual
revision date in the builder when content changes; do not refresh dates just for
search engines. Search rankings and rich results are not guaranteed.

Site search, URL parsing and the illustrative odds calculator run locally.
They do not send inputs to a server, store inputs or create bets.

## Images

Original AI-generated artwork lives in `assets/images/` as responsive WebP
variants and social JPEGs. Both illustrations are identified as such on the site.
Do not represent the stadium image as evidence of a real venue or event.

Generation briefs: (1) forest-green editorial still life with an ivory sphere,
emerald glass arch and brass objects; (2) empty football pitch at dusk, a ball
near the touchline, no people or branding. Generated with the built-in image
generation tool, then optimized for web delivery. Do not regenerate them during
an ordinary content build.

The existing Gandom font is served locally. The redesigned SVG mark is a
code-native vector.

## Editorial boundaries

No fabricated user reviews, operator ratings, license confirmations or payment
experiences. Brand guides state their verification limits. Medical, legal and
financial qualifications are not invented for the author. External technical
sources are for explanations, not endorsements.

Contact reports use the public repository's GitHub Issues. Do not post private
account details. Hosting and external sites have their own privacy policies.
