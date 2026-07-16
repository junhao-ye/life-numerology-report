# Life Numerology Report

一個可追溯、可測試的生命靈數 Agent Skill。輸入公曆生日與選填的羅馬拼音出生姓名，即可計算核心數字、生日九宮格與完整連線，並輸出獨立的繁體中文 HTML 報告。

> 生命靈數屬於象徵性自我反思工具，不是科學預測，也不應取代醫療、法律、財務或其他專業建議。

## 功能

- 日期數字：生命路徑數、生日數、態度數、個人流年數
- 姓名數字：表達數、靈魂渴望數、人格數、成熟數
- 主數支援：`11`、`22`、`33`
- 畢達哥拉斯 `1–9` 拉丁字母映射
- `Y` 可選擇視為母音；預設為子音
- `1–9` 生日九宮格、來源標記與八條候選連線
- JSON 計算資料與完全離線的單檔 HTML 報告
- 使用者輸入 HTML 跳脫、無遠端字型、無分析碼、無第三方 JavaScript
- Python 標準函式庫實作，執行時不需要額外依賴

## 九宮格規則

九宮格排列如下：

```text
1 2 3
4 5 6
7 8 9
```

標記來源：

- `○`：出生日期 `YYYYMMDD` 中的非零原始數字
- `△`：生日所有數字的總和，以及必要的中間化約數字
- `□`：連續化約至個位數後的九宮格根數

數字 `0` 不進入九宮格。只有三個格位都至少有一個標記時，才會形成連線：

- 橫向：`1–2–3`、`4–5–6`、`7–8–9`
- 直向：`1–4–7`、`2–5–8`、`3–6–9`
- 對角：`1–5–9`、`3–5–7`

九宮格根數與生命路徑數是不同計算欄位。主數生命路徑仍會保留為 `11/2`、`22/4` 或 `33/6`。

## 環境需求

- Python 3.10 或更新版本
- 不需要安裝第三方 Python 套件

## 快速開始

在專案根目錄執行：

```bash
python scripts/generate_report.py \
  --birth-date 1992-07-16 \
  --name "Avery Lin" \
  --target-year 2027 \
  --output report.html
```

PowerShell：

```powershell
python scripts\generate_report.py `
  --birth-date 1992-07-16 `
  --name "Avery Lin" `
  --target-year 2027 `
  --output report.html
```

日期限定版：

```bash
python scripts/generate_report.py \
  --birth-date 1992-07-16 \
  --output report.html
```

輸出 JSON：

```bash
python scripts/generate_report.py \
  --birth-date 1992-07-16 \
  --name "Avery Lin" \
  --format json
```

將 `Y` 視為母音：

```bash
python scripts/generate_report.py \
  --birth-date 1992-07-16 \
  --name "Avery Lin" \
  --y-as-vowel \
  --output report.html
```

## 參數

| 參數 | 必填 | 說明 |
|---|---:|---|
| `--birth-date` | 是 | 公曆生日，格式為 `YYYY-MM-DD` |
| `--name` | 否 | 羅馬拼音出生全名；重音拉丁字母會正規化 |
| `--target-year` | 否 | 個人流年目標年份；預設為當年 |
| `--y-as-vowel` | 否 | 將姓名中的 `Y` 視為母音 |
| `--format` | 否 | `html` 或 `json`；預設 `html` |
| `--output` | HTML 模式必填 | 輸出的 `.html` 檔案路徑 |

中文姓名不會自動套用筆劃數或任意轉寫。需要姓名數字時，請提供羅馬拼音。

## 測試

```bash
python -m unittest discover -s tests -v
```

測試涵蓋主數、姓名映射、`Y` 規則、重音字母、非拉丁姓名、HTML 跳脫、九宮格來源標記、零值處理、卓越數與連線判定。

## 作為 Agent Skill 使用

此 repo 已採 Agent Skills 結構：

```text
life-numerology-report/
├── SKILL.md
├── SPEC.md
├── SOURCES.md
├── references/
├── scripts/
└── tests/
```

將整個資料夾複製到你的 Agent Skills 目錄，重新啟動或重新載入 Agent 後，即可用「生命靈數」、「生日九宮格」、「數字連線」或「生命靈數 HTML 報告」等語句觸發。

## 隱私與使用界線

- 腳本不會進行網路請求。
- 只會寫入使用者明確指定的輸出檔案。
- 公開範例與測試使用虛構資料，不包含私人生日報告。
- 計算結果只適合作為象徵性反思提示，不是診斷或確定性預測。

## 授權

本專案採用 [MIT License](LICENSE)。

