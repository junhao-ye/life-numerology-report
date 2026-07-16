---
name: life-numerology-report
description: Creates traceable Traditional Chinese 生命靈數 calculations, 1–9 九宮格數字與連線, and standalone HTML reports from a Gregorian birth date and optional Romanized birth name. Use for 生命靈數、生命路徑數、主命數、生日數、姓名靈數、九宮格、數字連線、表達數、靈魂渴望數、人格數、成熟數、個人流年數, or a numerology HTML report.
---

# Life Numerology Report

Generate deterministic numerology data before writing any interpretation. Treat the result as a reflective symbolic framework, not a factual prediction.

## Runtime Contract

1. Collect the Gregorian birth date in `YYYY-MM-DD` form.
2. Collect the full birth name only when name-based numbers are requested. Ask for Romanized spelling when the supplied name has no Latin letters.
3. Use `scripts/generate_report.py`; do not calculate core numbers from memory.
4. Choose the target year from the user's request. Default to the current calendar year.
5. Write a standalone `.html` report to a user-approved writable path.
6. Return the core-number summary, completed 九宮格 lines, and the generated file path.

## Command

Run from the skill root:

```text
python scripts/generate_report.py --birth-date YYYY-MM-DD [--name "FULL ROMANIZED BIRTH NAME"] [--target-year YYYY] [--y-as-vowel] --output PATH.html
```

| Argument | Required | Behavior |
|---|---:|---|
| `--birth-date` | yes | Valid Gregorian date in ISO form. |
| `--name` | no | Full birth name using Latin letters; accents are normalized. |
| `--target-year` | no | Personal-year calculation; defaults to the current year. |
| `--y-as-vowel` | no | Treat `Y` as a vowel. Default: consonant. |
| `--output` | yes for HTML | Creates parent directories and writes one self-contained HTML file. |
| `--format json` | no | Print the structured calculation to stdout instead of generating HTML. |

The script is non-interactive. On success, HTML mode prints a JSON receipt containing `status`, `output`, and `core_numbers`. On invalid input it exits non-zero with a concise error. If `python` is unavailable, try `python3` or the workspace-bundled Python runtime with the same arguments. If no Python runtime is available, explain that deterministic generation is blocked; do not silently substitute mental arithmetic.

## Calculation And Output Rules

| Area | Requirement |
|---|---|
| Date method | Reduce month, day, and year separately, preserving `11`, `22`, and `33`, then reduce their sum. |
| Name method | Use the Pythagorean repeating `1–9` Latin-letter mapping. |
| Name metrics | Expression = all letters; Soul Urge = vowels; Personality = consonants. |
| Birth grid | Count non-zero birth-date digits as circles, derived-sum digits as triangles, and the final root as a square in a `1–9` grid. |
| Connections | Show a line only when all three cells in one of the three rows, three columns, or two diagonals are active. |
| Traceability | Show source values, sums, reduction steps, and the selected `Y` rule. |
| Chinese names | Do not invent stroke-count or transliteration rules. Request Romanization or omit name metrics. |
| HTML | Escape user input, embed no remote scripts/fonts, and remain readable when printed. |
| Interpretation | Use possibilities and reflection prompts; avoid certainty, diagnosis, or high-stakes advice. |

## Validation Loop

1. Generate the report.
2. Run `python -m unittest discover -s tests -v` after script changes.
3. Confirm the receipt has `status: ok` and the file exists.
4. Inspect the HTML for the title, core numbers, nine grid cells, expected connection lines, calculation trace, privacy note, and symbolic-use disclaimer.
5. Fix and rerun until all checks pass.

## Failure Handling

| Failure | Recovery |
|---|---|
| Missing or invalid date | Ask for one valid Gregorian date in `YYYY-MM-DD` form. |
| Name has no Latin letters | Ask for Romanization, or proceed with date-only numbers after saying name metrics will be omitted. |
| `Y` is ambiguous | Default to consonant and state the rule; use `--y-as-vowel` only when requested. |
| `python` command is unavailable | Try `python3` or the workspace-bundled Python runtime; otherwise report the blocker. |
| Output path is blocked | Select a writable path and rerun. |
| User asks for certainty | Reframe the reading as symbolic reflection and preserve the computed data. |

## References

| File | Open when |
|---|---|
| `references/methodology.md` | Explaining formulas, 九宮格 markers/connections, resolving master-number or `Y` disputes, or checking supported inputs. |
| `references/report-examples.md` | Checking a happy path, privacy-robust variant, or common anti-pattern before delivery. |

## Boundaries

Do not present numerology as scientifically validated prediction. Do not use it to decide medical, legal, financial, employment, or safety-critical matters. Minimize personal data: the local script makes no network calls and stores only the explicitly requested output file.

