# Life Numerology Report — Sources And Decisions

## Source Inventory

| Source | Trust | Contribution | Usage constraints |
|---|---|---|---|
| Agent Skills `skill-writer` workflow and validator | local authority / high | New-skill workflow, script-backed shape, SPEC, precision pass, trigger tests, and validation contract. | Authoring-time guidance only. |
| Existing deterministic astrology Skill prior art | local prior art / medium-high | Traceability, failure recovery, and cautious interpretation boundary. | Pattern source only; no formulas copied. |
| [World Numerology — Life Path](https://www.worldnumerology.com/numerology-life-path/) | practitioner source / medium | Reduce month, day, and year separately; preserve master numbers. | Numerology is not scientific authority. |
| [World Numerology course, part 2](https://www.worldnumerology.com/numerology-course-classes/classes/numerology-workshop-part-2.pdf) | practitioner source / medium | Repeating 1–9 Latin-letter mapping and full birth-name usage. | Paraphrased; no long excerpts. |
| [Numerology.com — Expression Number](https://www.numerology.com/articles/your-numerology-chart/expression-number/) | practitioner source / medium | Expression number from all birth-name letters; preserve 11/22/33. | Used only to cross-check convention. |
| [World Numerology — Soul Urge](https://www.worldnumerology.com/numerology-soul-urge/) | practitioner source / medium | Soul Urge from vowels in the full birth name. | Used only to cross-check convention. |
| [Wikipedia — Numerology](https://en.wikipedia.org/wiki/Numerology) | tertiary / medium | Frames numerology as belief in mystical relationships between numbers and events. | Boundary/context only. |
| User-supplied `numbers of life.html` plus its local application bundle | direct implementation / high for reference behavior | Birth digits as circles, derived-sum digits as triangles, final root as a square, zero omission, and ascending `1–9` layout. | Behavior was independently reimplemented; source code/CSS was not copied and no remote dependency was retained. |

## Synthesis Decisions

| Decision | Status | Rationale |
|---|---|---|
| Class = `workflow-process` | adopted | The task has preconditions, an ordered calculation flow, failure handling, validation, and safety boundaries. |
| Primary shape = `script-backed-workflow` | adopted | Date parsing, reductions, name normalization, escaping, and HTML generation are error-prone in prose. |
| Secondary mechanic = validation loop | adopted | Unit tests and structural checks can catch silent arithmetic and rendering drift. |
| Inline-only guidance | rejected | It would invite inconsistent manual calculations and unsafe HTML interpolation. |
| Reference-only expert shape | rejected | Optional knowledge is not the main risk; deterministic transformation is. |
| Provider-specific mechanics | rejected | Standard Python and relative paths keep the skill portable. |
| Pythagorean Latin mapping | adopted | It is explicit, reproducible, and commonly documented in modern Western numerology sources. |
| Master numbers `11`, `22`, `33` | adopted | Sources vary, so the selected convention is disclosed and tested. |
| `Y` defaults to consonant | adopted | Avoids hidden linguistic guessing; callers can opt into vowel treatment. |
| Chinese stroke calculation | deferred | No single compatible mapping was supplied; silent conversion would be misleading. |
| Reference-compatible nine grid | adopted | The user supplied an executable implementation with explicit marker-count behavior. |
| Eight complete-cell connections | adopted | Three rows, three columns, and two diagonals are drawn only when every participating cell is active. |
| Line interpretation labels | deferred | Meanings vary by school; the report displays objective positions only. |

## Coverage Matrix

| Dimension | Status | Evidence |
|---|---|---|
| Preconditions and input validation | covered | `SKILL.md`, script CLI, unit tests. |
| Core and edge calculations | covered | Methodology reference and master-number tests. |
| Nine-grid markers and connections | covered | Reference bundle, deterministic calculator, zero/no-line/repeated-intermediate tests. |
| Failure handling | covered | Non-Latin names, invalid dates, blocked paths, missing runtime. |
| Privacy and safety | covered | No network calls, output-only persistence, symbolic-use disclaimer. |
| HTML result contract | covered | Self-contained renderer, escaping tests, report examples. |
| Trigger precision | covered | Should/should-not query sets below. |
| Alternate numerology schools | partial | Explicitly out of scope; future work requires a separately named method. |

## Trigger Quality Sets

Should trigger:

- 「幫我算生命靈數並輸出 HTML」
- 「我的生命路徑數是多少？」
- 「用生日與英文全名算表達數、靈魂數、人格數」
- “Create a numerology report for 1992-07-16.”
- 「幫我算 2027 個人流年數」
- 「用生日做生命靈數九宮格，顯示數字連線」

Should not trigger:

- 「幫我排八字」
- 「用紫微斗數看流年」
- 「計算這組資料的平均數」
- 「設計一個通用 HTML 儀表板」
- 「西洋占星本命盤怎麼看？」

Description optimization: added `九宮格` and `數字連線` trigger aliases while retaining domain wording that excludes adjacent astrology and generic arithmetic.

## Source Adaptation

| Item | Decision |
|---|---|
| Source intent | Turn a Gregorian birth date into source-marked digits in a `1–9` display. |
| Local target | Add structured grid data, completed-line detection, accessible HTML, and regression tests to the existing report generator. |
| Fidelity boundary | Preserve digit inputs, marker categories, zero omission, intermediate-value handling, and ascending layout. |
| Local replacement | Replace the React/Tailwind runtime with standard-library Python and self-contained HTML/CSS/SVG. |
| Added behavior | Compute and display eight possible complete-cell lines; the reference page itself did not draw lines. |
| Omitted material | Interactive date input, URL query state, downloaded vendor bundle, and reference styling. |
| Rights handling | Reimplemented observable behavior only; bundled source code and CSS are not redistributed. |

## Precision Pass

- Added `SKILL.md` sections because no existing project rule existed.
- Moved provenance and shape rationale to this file.
- Kept optional formula depth in `references/methodology.md`.
- Kept universal safety and data rules in `SKILL.md` so they cannot be skipped.
- Added only two routed references: one exact lookup and one output-quality lookup.
- Narrowed the existing methodology and examples references instead of adding a third runtime reference.
- Added nine-grid rules to `SKILL.md` because every generated report now includes the grid.

## Open Gaps And Retrieval Stop

- Alternate Chinese name and Chaldean systems remain out of scope until a method is explicitly chosen.
- Interpretation language is original and intentionally compact; it is not validated as psychological assessment.
- Line-specific symbolic meanings remain deliberately unassigned because schools use inconsistent labels.
- Collection stopped because the supplied executable bundle fully exposed the marker algorithm; the new line invariant is explicit and covered by tests.
