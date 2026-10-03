# Changelog

All notable changes to the Decision Object format. Drafts (0.x) may break compatibility; see [VERSIONING.md](VERSIONING.md).

## 0.3.0 — 2026-10-03 (first public draft)

- Request / response / ack structure; `kind`: decision, review, task, command, brief.
- Response: `conditions` (option plus conditions), `standing_rule` (a draft "from now on" rule), and `decided_by: expiry` for "nobody answered, the recommendation was applied", which is explicitly not human consent.
- Schema and 30 example records. Versions before 0.3 were internal iterations and were not published.
