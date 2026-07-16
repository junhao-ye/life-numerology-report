# Report Examples

Open this file when checking output quality or handling ambiguous/private inputs.

## Happy Path

Input:

```text
birth date: 1992-07-16
name: Avery Lin
target year: 2027
```

Expected behavior:

- Generate all eight supported numbers.
- Show `7 + 7 + 3 = 17 → 8` for Life Path.
- State whether `Y` is a consonant.
- Render nine grid cells, marker legend, and only the connections whose three cells are active.
- Produce a standalone Traditional Chinese HTML report with a visible symbolic-use note.

## Privacy-Robust Variant

Input:

```text
birth date: 1992-07-16
name omitted
```

Expected behavior:

- Generate Life Path, Birthday, Attitude, and Personal Year.
- Say name-based metrics were omitted; do not ask for a name unless those metrics are required.
- Store nothing except the explicit output file and make no network call.
- Still generate the date-based nine-grid and connection display.

## Anti-Pattern And Correction

Anti-pattern:

> 你天生注定創業，明年一定會成功投資；中文名我直接換成字母算。

Corrected behavior:

> 在本報告採用的象徵框架中，這組數字可作為檢視自主性與承擔方式的提示。它不預測投資結果；姓名數需由你提供羅馬拼音後才能計算。

Grid anti-pattern:

> 只要同一排出現兩個數字，就把第三格補上並畫線。

Corrected behavior:

> 缺少的格位保持空白；只有三格都至少有一個來源標記時，才顯示完整連線。
