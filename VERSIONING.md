# Versioning

The format follows [Semantic Versioning](https://semver.org/).

## Draft period (0.x)

- Any minor release (0.3 → 0.4) **may break compatibility**. Breaking changes are listed first in the changelog with a short migration note.
- Each published version keeps its own schema file under `schema/v0.N/`, and old files are never edited after release, so a record can always be validated against the version it was written for.
- The namespace `io.github.f46msgd/decision` and the schema `$id` may change before 1.0.
- Changes are driven by real examples: a proposal should come with at least one record the current version expresses badly.

## From 1.0

- **Patch** (1.0.x): clarifications, typo fixes, new examples. No schema change.
- **Minor** (1.x): only additive, optional fields or new enum values that old consumers can ignore.
- **Major** (2.0): anything that can make a previously valid record invalid, or change the meaning of an existing field.

A consumer that sees an unknown optional field must ignore it. A consumer that sees an unknown `kind` or `status` should show the card read-only with `title`, `why`, and `note`.
