# Life Numerology Report Specification

## Intent

`life-numerology-report` turns a Gregorian birth date and optional Romanized birth name into traceable symbolic numerology calculations and a polished Traditional Chinese HTML report. Deterministic arithmetic stays in the bundled script; interpretation stays cautious and reflective.

## Scope

In scope:

- Date numbers: Life Path, Birthday, Attitude, and Personal Year.
- Reference-compatible `1–9` birth grid with circle/triangle/square source markers and eight possible straight-line connections.
- Name numbers: Expression, Soul Urge, Personality, and Maturity.
- Master numbers `11`, `22`, and `33`.
- Pythagorean Latin-letter mapping, optional `Y`-as-vowel behavior, JSON diagnostics, and standalone HTML output.

Out of scope:

- Chinese stroke-count numerology, Chaldean numerology, compatibility scoring, or deterministic future prediction.
- Scientific, medical, legal, financial, hiring, or safety conclusions.
- Automatic transliteration of non-Latin names.

## Users And Trigger Context

- Primary users: Traditional Chinese readers requesting a 生命靈數 calculation or report.
- Common requests: 算生命靈數、生命路徑數、姓名靈數、個人流年、輸出 HTML 命盤。
- Should not trigger for: ordinary arithmetic, statistics, Chinese 八字/紫微斗數, astrology charts, or generic HTML design.

## Runtime Contract

- Required first actions: collect and validate an ISO Gregorian birth date; collect a Romanized birth name only for name metrics.
- Required outputs: structured calculation data, birth-grid cells/connections, and, by default, a standalone HTML report.
- Non-negotiable constraints: use the script, show arithmetic traces, escape user input, and label interpretation as symbolic.
- Expected bundled files: `scripts/generate_report.py`, `references/methodology.md`, and `references/report-examples.md`.

## Source And Evidence Model

Authoritative-for-this-skill sources:

- The explicit calculation contract in `references/methodology.md`.
- Regression tests under `tests/`.
- Provenance and adopted decisions in `SOURCES.md`.

Useful improvement sources:

- Positive examples: correct traces and helpful non-deterministic wording.
- Negative examples: master-number drift, incorrect grid markers or forced lines, unsafe certainty, unescaped names, incorrect `Y` handling, and non-Latin names silently ignored.
- Validation results: unit tests, structural validation, and browser/print inspection.

Data that must not be stored:

- Unnecessary identity details, private histories, or contact data.
- Birth data outside the explicit report requested by the user.

## Reference Architecture

- `SKILL.md` contains runtime routing, commands, validation, failure handling, and boundaries.
- `references/methodology.md` contains exact formula decisions and supported-input rules.
- `references/report-examples.md` contains transformed output examples.
- `scripts/` contains deterministic calculation and HTML rendering.
- `tests/` contains regression checks.
- No separate assets are required; HTML is self-contained.

## Validation

- Lightweight validation: run the skill-writer structural validator.
- Deeper validation: run all unit tests and generate both date-only and name-inclusive reports.
- Holdouts: master-number dates, zero-heavy dates, no-line grids, repeated intermediate values, accented Latin names, non-Latin-only names, invalid dates, and `Y` vowel/consonant variants.
- Acceptance gates: valid frontmatter, all routed files exist, tests pass, nine grid cells render, expected SVG lines match computed connections, receipt reports success, HTML is self-contained, and the disclaimer is visible.

## Known Limitations

- Numerology has multiple schools; this skill intentionally implements one documented modern Pythagorean convention.
- `Y` is linguistically ambiguous and therefore user-selectable.
- Name metrics require Latin letters and do not claim equivalence with Chinese stroke systems.
- Grid lines indicate cell coverage only; line interpretations vary across numerology schools and are not scored here.
- Interpretations are compact prompts, not individualized counseling.

## Maintenance Notes

- Update `SKILL.md` when triggers, command use, workflow, or boundaries change.
- Update `SOURCES.md` when adopting a new convention or evidence source.
- Update tests whenever calculation, escaping, or output fields change.
- Add a reference only when a distinct runtime lookup cannot stay concise in an existing file.
