# Calculation Methodology

Open this file to explain a result, resolve a method dispute, or verify supported inputs.

## Reduction

`reduce(n, preserve_master=true)` repeatedly sums decimal digits until the value is one digit or `11`, `22`, or `33`. When `preserve_master=false`, continue to one digit.

## Date Numbers

| Number | Formula |
|---|---|
| Life Path | Reduce month, day, and four-digit year separately with master preservation; add those three values; reduce again with master preservation. |
| Birthday | Reduce the calendar day (`1–31`) with master preservation; retain the original day in the trace. |
| Attitude | Add month and day; reduce with master preservation. |
| Personal Year | Add birth month, birth day, and digits of the target year; reduce to one digit without master preservation. |

Example: `1992-07-16` → month `7`, day `1+6=7`, year `1+9+9+2=21→3`; total `7+7+3=17→8`.

## Name Numbers

Normalize Unicode Latin accents, uppercase the result, then ignore spaces, hyphens, apostrophes, and punctuation.

| Value | Letters |
|---:|---|
| 1 | A J S |
| 2 | B K T |
| 3 | C L U |
| 4 | D M V |
| 5 | E N W |
| 6 | F O X |
| 7 | G P Y |
| 8 | H Q Z |
| 9 | I R |

| Number | Formula |
|---|---|
| Expression | Reduce the sum of all mapped letters, preserving master numbers. |
| Soul Urge | Reduce mapped vowels `A E I O U`; include `Y` only with `--y-as-vowel`. |
| Personality | Reduce mapped consonants; exclude `Y` only with `--y-as-vowel`. |
| Maturity | Reduce Life Path + Expression, preserving master numbers. |

## Birth Grid And Connections

Use the reference-compatible ascending layout:

```text
1 2 3
4 5 6
7 8 9
```

| Marker | Calculation |
|---|---|
| Circle `○` | Count every non-zero digit in the zero-padded birth date `YYYYMMDD`. |
| Triangle `△` | Add every birth-date digit. Mark each digit of that total; if its digit sum is still two digits, mark those intermediate digits too. |
| Square `□` | Repeatedly sum the derived value to one digit and mark that final root. |

Ignore `0`; it has no grid cell. A cell is active when it has at least one circle, triangle, or square.

Show a connection only when all three cells are active:

- rows: `1–2–3`, `4–5–6`, `7–8–9`
- columns: `1–4–7`, `2–5–8`, `3–6–9`
- diagonals: `1–5–9`, `3–5–7`

Keep this grid-root calculation separate from Life Path reduction. The grid root is always one digit; a Life Path master number may be displayed as `11/2`, `22/4`, or `33/6` without being replaced by its root.

## Method Boundaries

- Use the exact Gregorian date supplied; time, timezone, and birthplace are irrelevant to this method.
- Require at least one `A–Z` letter before producing name numbers.
- Do not auto-transliterate Chinese or infer a stroke-based system.
- Method variants are valid topics for explanation, but never mix formulas within one report.
- Treat a completed grid line as a visual coverage relationship, not proof of ability or prediction.
