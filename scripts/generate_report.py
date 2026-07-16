#!/usr/bin/env python3
"""Deterministic Pythagorean numerology calculator and HTML report generator."""

from __future__ import annotations

import argparse
import html
import json
import sys
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any


MASTER_NUMBERS = {11, 22, 33}
VOWELS = set("AEIOU")
LETTER_VALUES = {chr(code): ((code - ord("A")) % 9) + 1 for code in range(ord("A"), ord("Z") + 1)}

NUMBER_GUIDE: dict[int, dict[str, Any]] = {
    1: {
        "title": "開創者",
        "theme": "自主、起步與清楚表態",
        "strengths": ["主動建立方向", "在模糊中先走一步", "重視個人判斷"],
        "shadows": ["過度獨撐", "把速度放在傾聽之前"],
        "practice": "在堅持立場前，先說清楚你需要什麼協作。",
    },
    2: {
        "title": "協調者",
        "theme": "連結、感受與細緻合作",
        "strengths": ["察覺關係氣氛", "耐心整合差異", "讓合作變得柔順"],
        "shadows": ["為和諧壓住需求", "反覆等待外界確認"],
        "practice": "保留同理，也把自己的界線說成完整句子。",
    },
    3: {
        "title": "表達者",
        "theme": "創意、語言與情緒流動",
        "strengths": ["把感受轉成作品", "帶動輕盈氣氛", "善於連結觀點"],
        "shadows": ["分散與拖延", "用熱鬧避開真正感受"],
        "practice": "每天完成一個小作品，讓靈感有落點。",
    },
    4: {
        "title": "建構者",
        "theme": "秩序、可靠與長期累積",
        "strengths": ["拆解複雜任務", "建立可重複流程", "重視承諾與品質"],
        "shadows": ["僵化控制", "把安全等同於不能改變"],
        "practice": "固定核心原則，同時為方法保留一次實驗空間。",
    },
    5: {
        "title": "探索者",
        "theme": "變化、自由與經驗學習",
        "strengths": ["快速適應變化", "勇於探索未知", "把經驗轉成洞見"],
        "shadows": ["追逐刺激", "承諾尚未成熟就轉向"],
        "practice": "先定義自由的邊界，再選一件事持續到可驗證。",
    },
    6: {
        "title": "照護者",
        "theme": "責任、美感與關係滋養",
        "strengths": ["創造歸屬感", "願意照顧共同品質", "看見可被改善之處"],
        "shadows": ["過度承擔", "用完美標準要求自己與他人"],
        "practice": "把照顧分成『我願意』與『對方需要負責』兩欄。",
    },
    7: {
        "title": "探究者",
        "theme": "內省、分析與追問本質",
        "strengths": ["深入研究", "辨識表象下的模式", "需要真實而非喧鬧"],
        "shadows": ["過度懷疑", "在準備中延後參與"],
        "practice": "為研究設定截止點，之後用一個小行動驗證理解。",
    },
    8: {
        "title": "整合者",
        "theme": "資源、影響力與結果責任",
        "strengths": ["整合人與資源", "看見規模與效益", "承擔艱難決策"],
        "shadows": ["把價值等同成就", "在壓力下過度控制"],
        "practice": "每次談結果時，也列出不可犧牲的原則與人際成本。",
    },
    9: {
        "title": "人文者",
        "theme": "包容、完成與更大的意義",
        "strengths": ["理解多元處境", "把經驗提升成意義", "願意促成完整收尾"],
        "shadows": ["理想化與失望", "難以放下已結束的人事物"],
        "practice": "辨認一件已完成的事，為它收尾，而不是繼續補救。",
    },
    11: {
        "title": "啟發者 11/2",
        "theme": "直覺、靈感與敏銳連結",
        "strengths": ["感受細微訊號", "以願景鼓舞他人", "連結理想與關係"],
        "shadows": ["神經緊繃", "把靈感變成自我壓力"],
        "practice": "先用小規模作品承接靈感，再決定是否放大。",
    },
    22: {
        "title": "實踐者 22/4",
        "theme": "宏大願景與務實建造",
        "strengths": ["把願景拆成系統", "兼顧規模與細節", "建立能服務多人的成果"],
        "shadows": ["被巨大期待壓住", "忽略基本節奏與休息"],
        "practice": "把十年願景縮成下一個可交付的十四天。",
    },
    33: {
        "title": "引導者 33/6",
        "theme": "慈悲、教導與成熟照護",
        "strengths": ["以理解支持成長", "把經驗轉成教學", "提升共同環境"],
        "shadows": ["救世情結", "把別人的課題背在自己身上"],
        "practice": "提供支持前，先確認對方的意願與你的容量。",
    },
}

NUMBER_LABELS = {
    "life_path": ("生命路徑數", "人生反覆練習的主題"),
    "birthday": ("生日數", "較自然可用的天賦傾向"),
    "attitude": ("態度數", "面對新情境的第一反應"),
    "personal_year": ("個人流年數", "目標年份的節奏提示"),
    "expression": ("表達數", "能力如何向外展開"),
    "soul_urge": ("靈魂渴望數", "內在較深的驅動"),
    "personality": ("人格數", "他人先感受到的外在風格"),
    "maturity": ("成熟數", "生命歷程逐漸整合的方向"),
}

GRID_POSITIONS = {
    1: (50, 50), 2: (150, 50), 3: (250, 50),
    4: (50, 150), 5: (150, 150), 6: (250, 150),
    7: (50, 250), 8: (150, 250), 9: (250, 250),
}

GRID_CONNECTIONS = (
    ((1, 2, 3), "1–2–3 上排", "horizontal"),
    ((4, 5, 6), "4–5–6 中排", "horizontal"),
    ((7, 8, 9), "7–8–9 下排", "horizontal"),
    ((1, 4, 7), "1–4–7 左列", "vertical"),
    ((2, 5, 8), "2–5–8 中列", "vertical"),
    ((3, 6, 9), "3–6–9 右列", "vertical"),
    ((1, 5, 9), "1–5–9 主對角", "diagonal"),
    ((3, 5, 7), "3–5–7 副對角", "diagonal"),
)


def digit_sum(value: int) -> int:
    return sum(int(ch) for ch in str(abs(value)))


def reduce_number(value: int, preserve_master: bool = True) -> tuple[int, list[int]]:
    if value < 0:
        raise ValueError("number reduction requires a non-negative integer")
    steps = [value]
    while value > 9 and not (preserve_master and value in MASTER_NUMBERS):
        value = digit_sum(value)
        steps.append(value)
    return value, steps


def reduction_text(value: int, preserve_master: bool = True) -> str:
    result, steps = reduce_number(value, preserve_master)
    if len(steps) == 1:
        suffix = "（主數保留）" if preserve_master and result in MASTER_NUMBERS else ""
        return f"{value}{suffix}"
    parts: list[str] = []
    current = value
    for next_value in steps[1:]:
        parts.append(" + ".join(str(current)))
        parts.append(f"= {next_value}")
        current = next_value
    return " → ".join(" ".join(parts[index:index + 2]) for index in range(0, len(parts), 2))


def metric(value: int, trace: str, source: Any) -> dict[str, Any]:
    return {"value": value, "trace": trace, "source": source}


def calculate_date_numbers(birth_date: date, target_year: int) -> dict[str, dict[str, Any]]:
    month_value, _ = reduce_number(birth_date.month)
    day_value, _ = reduce_number(birth_date.day)
    year_value, _ = reduce_number(birth_date.year)
    life_raw = month_value + day_value + year_value
    life_value, _ = reduce_number(life_raw)
    life_trace = (
        f"月 {reduction_text(birth_date.month)}；日 {reduction_text(birth_date.day)}；"
        f"年 {reduction_text(birth_date.year)}；{month_value} + {day_value} + {year_value} = {life_raw}"
    )
    if life_value != life_raw:
        life_trace += f" → {reduction_text(life_raw)}"
    elif life_value in MASTER_NUMBERS:
        life_trace += "（主數保留）"

    birthday_value, _ = reduce_number(birth_date.day)
    attitude_raw = birth_date.month + birth_date.day
    attitude_value, _ = reduce_number(attitude_raw)
    personal_raw = birth_date.month + birth_date.day + digit_sum(target_year)
    personal_value, _ = reduce_number(personal_raw, preserve_master=False)

    return {
        "life_path": metric(
            life_value,
            life_trace,
            {"month": month_value, "day": day_value, "year": year_value, "sum": life_raw},
        ),
        "birthday": metric(
            birthday_value,
            reduction_text(birth_date.day),
            {"calendar_day": birth_date.day},
        ),
        "attitude": metric(
            attitude_value,
            f"{birth_date.month} + {birth_date.day} = {attitude_raw} → {reduction_text(attitude_raw)}",
            {"month": birth_date.month, "day": birth_date.day, "sum": attitude_raw},
        ),
        "personal_year": metric(
            personal_value,
            (
                f"{birth_date.month} + {birth_date.day} + ({' + '.join(str(target_year))}) "
                f"= {personal_raw} → {reduction_text(personal_raw, preserve_master=False)}"
            ),
            {"month": birth_date.month, "day": birth_date.day, "target_year": target_year, "sum": personal_raw},
        ),
    }


def calculate_birth_grid(birth_date: date) -> dict[str, Any]:
    """Build the reference-compatible 1–9 grid and completed straight lines."""
    raw_digits = [int(ch) for ch in birth_date.strftime("%Y%m%d")]
    major = sum(raw_digits)
    intermediate_value = digit_sum(major)
    intermediate = intermediate_value if intermediate_value >= 10 else None
    intermediate_label = None
    if intermediate is not None:
        text = str(intermediate)
        intermediate_label = "卓越數" if len(text) == 2 and text[0] == text[1] else "後天數"
    root = digit_sum(intermediate_value)

    cells: dict[str, dict[str, int]] = {
        str(number): {"birth_count": 0, "derived_count": 0, "root_count": 0, "total_count": 0}
        for number in range(1, 10)
    }
    for number in raw_digits:
        if number:
            cells[str(number)]["birth_count"] += 1
    derived_digits = [int(ch) for ch in str(major)]
    if intermediate is not None:
        derived_digits.extend(int(ch) for ch in str(intermediate))
    for number in derived_digits:
        if number:
            cells[str(number)]["derived_count"] += 1
    if root:
        cells[str(root)]["root_count"] += 1
    for cell in cells.values():
        cell["total_count"] = cell["birth_count"] + cell["derived_count"] + cell["root_count"]

    connections = []
    for digits, label, orientation in GRID_CONNECTIONS:
        if all(cells[str(number)]["total_count"] > 0 for number in digits):
            connections.append({
                "digits": list(digits),
                "label": label,
                "orientation": orientation,
                "start": list(GRID_POSITIONS[digits[0]]),
                "end": list(GRID_POSITIONS[digits[-1]]),
            })

    return {
        "layout": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "raw_digits": raw_digits,
        "major": major,
        "intermediate": intermediate,
        "intermediate_label": intermediate_label,
        "root": root,
        "cells": cells,
        "connections": connections,
        "connection_count": len(connections),
        "marker_legend": {
            "circle": "出生日期原始數字",
            "triangle": "後天數與中間化約數字",
            "square": "九宮格根數",
        },
    }


def normalize_latin_name(name: str) -> str:
    decomposed = unicodedata.normalize("NFKD", name)
    return "".join(ch for ch in decomposed.upper() if "A" <= ch <= "Z")


def letters_trace(letters: str) -> tuple[int, str, list[dict[str, Any]]]:
    details = [{"letter": letter, "value": LETTER_VALUES[letter]} for letter in letters]
    total = sum(item["value"] for item in details)
    expression = " + ".join(f"{item['letter']}({item['value']})" for item in details)
    return total, expression, details


def calculate_name_numbers(name: str, life_path: int, y_as_vowel: bool = False) -> dict[str, dict[str, Any]]:
    letters = normalize_latin_name(name)
    if not letters:
        raise ValueError("姓名沒有可計算的拉丁字母；請提供羅馬拼音，或省略姓名數。")

    vowels = VOWELS | ({"Y"} if y_as_vowel else set())
    vowel_letters = "".join(letter for letter in letters if letter in vowels)
    consonant_letters = "".join(letter for letter in letters if letter not in vowels)

    all_total, all_expression, all_details = letters_trace(letters)
    expression_value, _ = reduce_number(all_total)
    results: dict[str, dict[str, Any]] = {
        "expression": metric(
            expression_value,
            f"{all_expression} = {all_total} → {reduction_text(all_total)}",
            {"letters": all_details, "sum": all_total},
        )
    }

    if vowel_letters:
        vowel_total, vowel_expression, vowel_details = letters_trace(vowel_letters)
        soul_value, _ = reduce_number(vowel_total)
        results["soul_urge"] = metric(
            soul_value,
            f"{vowel_expression} = {vowel_total} → {reduction_text(vowel_total)}",
            {"letters": vowel_details, "sum": vowel_total},
        )

    if consonant_letters:
        consonant_total, consonant_expression, consonant_details = letters_trace(consonant_letters)
        personality_value, _ = reduce_number(consonant_total)
        results["personality"] = metric(
            personality_value,
            f"{consonant_expression} = {consonant_total} → {reduction_text(consonant_total)}",
            {"letters": consonant_details, "sum": consonant_total},
        )

    maturity_raw = life_path + expression_value
    maturity_value, _ = reduce_number(maturity_raw)
    results["maturity"] = metric(
        maturity_value,
        f"生命路徑 {life_path} + 表達數 {expression_value} = {maturity_raw} → {reduction_text(maturity_raw)}",
        {"life_path": life_path, "expression": expression_value, "sum": maturity_raw},
    )
    return results


def build_profile(birth_date: date, name: str | None, target_year: int, y_as_vowel: bool) -> dict[str, Any]:
    if not 1 <= target_year <= 9999:
        raise ValueError("target year must be between 1 and 9999")
    numbers = calculate_date_numbers(birth_date, target_year)
    warnings: list[str] = []
    if name:
        numbers.update(calculate_name_numbers(name, numbers["life_path"]["value"], y_as_vowel))
    else:
        warnings.append("未提供羅馬拼音出生姓名，因此略過表達數、靈魂渴望數、人格數與成熟數。")
    return {
        "profile": {"name": name, "birth_date": birth_date.isoformat()},
        "method": {
            "system": "modern-pythagorean",
            "master_numbers": [11, 22, 33],
            "y_as_vowel": y_as_vowel,
            "target_year": target_year,
        },
        "numbers": numbers,
        "birth_grid": calculate_birth_grid(birth_date),
        "warnings": warnings,
        "disclaimer": "生命靈數屬象徵性自我反思工具，不是科學預測，也不替代專業建議。",
    }


def guide_for(value: int) -> dict[str, Any]:
    return NUMBER_GUIDE[value]


def render_number_card(key: str, item: dict[str, Any], primary: bool = False) -> str:
    label, subtitle = NUMBER_LABELS[key]
    guide = guide_for(item["value"])
    primary_class = " primary" if primary else ""
    return f"""
      <article class="number-card{primary_class}">
        <div class="number-orbit"><span>{item['value']}</span></div>
        <div class="number-copy">
          <p class="eyebrow">{html.escape(label)}</p>
          <h3>{html.escape(guide['title'])}</h3>
          <p class="muted">{html.escape(subtitle)}</p>
          <p>{html.escape(guide['theme'])}</p>
        </div>
      </article>"""


def render_trace_row(key: str, item: dict[str, Any]) -> str:
    label, _ = NUMBER_LABELS[key]
    return f"""
        <tr>
          <th scope="row">{html.escape(label)}</th>
          <td class="trace">{html.escape(item['trace'])}</td>
          <td><span class="result-pill">{item['value']}</span></td>
        </tr>"""


def render_grid_cell(number: int, cell: dict[str, int]) -> str:
    active_class = " active" if cell["total_count"] else ""
    birth_markers = "".join('<span class="marker circle" aria-hidden="true">○</span>' for _ in range(cell["birth_count"]))
    derived_markers = "".join('<span class="marker triangle" aria-hidden="true">△</span>' for _ in range(cell["derived_count"]))
    root_markers = "".join('<span class="marker square" aria-hidden="true">□</span>' for _ in range(cell["root_count"]))
    accessible = (
        f"數字 {number}：生日 {cell['birth_count']} 次、衍生 {cell['derived_count']} 次、"
        f"根數 {cell['root_count']} 次"
    )
    return f"""
          <div class="grid-cell{active_class}" aria-label="{accessible}">
            <strong>{number}</strong>
            <div class="cell-markers">{birth_markers}{derived_markers}{root_markers}</div>
            <small>共 {cell['total_count']} 次</small>
          </div>"""


def render_grid_line(connection: dict[str, Any]) -> str:
    x1, y1 = connection["start"]
    x2, y2 = connection["end"]
    return (
        f'<line class="grid-line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
        f'<title>{html.escape(connection["label"])}</title></line>'
    )


def render_html(data: dict[str, Any]) -> str:
    profile = data["profile"]
    numbers = data["numbers"]
    birth_grid = data["birth_grid"]
    target_year = data["method"]["target_year"]
    display_name = profile["name"] or "日期限定版"
    safe_name = html.escape(display_name)
    safe_birth = html.escape(profile["birth_date"])
    cards = "".join(
        render_number_card(key, item, primary=(key == "life_path"))
        for key, item in numbers.items()
    )
    trace_rows = "".join(render_trace_row(key, item) for key, item in numbers.items())
    life_guide = guide_for(numbers["life_path"]["value"])
    personal_guide = guide_for(numbers["personal_year"]["value"])
    expression = numbers.get("expression")
    if expression:
        expression_guide = guide_for(expression["value"])
        integration = (
            f"你的生命路徑以「{life_guide['theme']}」為主軸；姓名表達則帶出「"
            f"{expression_guide['theme']}」。可以觀察：你正在用什麼方式，讓內在主題被外界真正看見？"
        )
    else:
        integration = (
            f"本次日期限定版把焦點放在「{life_guide['theme']}」。若補上羅馬拼音出生姓名，"
            "可再檢視能力表達、內在驅動與外在印象。"
        )
    warning_html = "".join(f"<li>{html.escape(item)}</li>" for item in data["warnings"])
    y_rule = "母音" if data["method"]["y_as_vowel"] else "子音"
    strength_items = "".join(f"<li>{html.escape(item)}</li>" for item in life_guide["strengths"])
    shadow_items = "".join(f"<li>{html.escape(item)}</li>" for item in life_guide["shadows"])
    grid_cells = "".join(
        render_grid_cell(number, birth_grid["cells"][str(number)])
        for number in range(1, 10)
    )
    grid_lines = "".join(render_grid_line(connection) for connection in birth_grid["connections"])
    connection_items = "".join(
        f'<li><span class="connection-swatch"></span>{html.escape(connection["label"])}</li>'
        for connection in birth_grid["connections"]
    )
    if not connection_items:
        connection_items = '<li class="muted">目前沒有三格皆出現的完整連線。</li>'
    raw_digits_text = " · ".join(str(number) for number in birth_grid["raw_digits"])
    intermediate_card = ""
    if birth_grid["intermediate"] is not None:
        intermediate_card = f"""
            <div class="grid-stat">
              <span>{html.escape(birth_grid['intermediate_label'])}</span>
              <strong>{birth_grid['intermediate']}</strong>
              <small>總和再次相加</small>
            </div>"""

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{safe_name}｜生命靈數洞察報告</title>
  <style>
    :root {{
      --ink: #182027;
      --muted: #69727a;
      --paper: #f6f3ec;
      --card: #fffdf8;
      --line: #ddd7cc;
      --violet: #62517d;
      --violet-deep: #352d49;
      --gold: #c4963d;
      --sage: #718879;
      --shadow: 0 20px 60px rgba(42, 36, 32, .10);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 10% 0%, rgba(196,150,61,.12), transparent 28rem),
        radial-gradient(circle at 95% 12%, rgba(98,81,125,.12), transparent 32rem),
        var(--paper);
      font-family: "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", system-ui, sans-serif;
      line-height: 1.7;
    }}
    body::before {{
      content: "";
      position: fixed; inset: 0; pointer-events: none; opacity: .22;
      background-image: linear-gradient(rgba(53,45,73,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(53,45,73,.05) 1px, transparent 1px);
      background-size: 32px 32px;
      mask-image: linear-gradient(to bottom, black, transparent 70%);
    }}
    .page {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 36px 0 72px; position: relative; }}
    .hero {{
      position: relative; overflow: hidden; color: white; border-radius: 28px; padding: clamp(34px, 7vw, 76px);
      background: linear-gradient(135deg, var(--violet-deep), #5c4b73 58%, #81683f); box-shadow: var(--shadow);
    }}
    .hero::after {{ content: "{numbers['life_path']['value']}"; position: absolute; right: -2%; bottom: -28%; font: 700 clamp(180px, 34vw, 360px)/1 Georgia, serif; color: rgba(255,255,255,.055); }}
    .kicker, .eyebrow {{ margin: 0 0 8px; font-size: .76rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }}
    .kicker {{ color: #ead6a5; }}
    .hero h1 {{ max-width: 760px; margin: 0; font: 600 clamp(2.4rem, 6vw, 5.4rem)/1.06 Georgia, "Noto Serif TC", serif; letter-spacing: -.035em; }}
    .hero .lede {{ max-width: 650px; margin: 24px 0 0; color: rgba(255,255,255,.82); font-size: 1.06rem; }}
    .meta {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 30px; }}
    .meta span {{ border: 1px solid rgba(255,255,255,.24); border-radius: 999px; padding: 7px 13px; color: rgba(255,255,255,.86); font-size: .88rem; backdrop-filter: blur(8px); }}
    .section {{ margin-top: 60px; }}
    .section-heading {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(220px, 430px); gap: 32px; align-items: end; margin-bottom: 22px; }}
    .section-heading h2 {{ margin: 0; font: 600 clamp(1.7rem, 4vw, 2.8rem)/1.2 Georgia, "Noto Serif TC", serif; color: var(--violet-deep); }}
    .section-heading p {{ margin: 0; color: var(--muted); }}
    .number-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .number-card {{ display: grid; grid-template-columns: 90px 1fr; gap: 20px; align-items: center; min-height: 180px; padding: 24px; border: 1px solid var(--line); border-radius: 20px; background: rgba(255,253,248,.86); box-shadow: 0 12px 32px rgba(42,36,32,.055); }}
    .number-card.primary {{ grid-column: span 2; background: linear-gradient(120deg, #fffdf8, #f0eaf5); border-color: #cfc1dd; }}
    .number-orbit {{ width: 82px; aspect-ratio: 1; display: grid; place-items: center; border: 1px solid #c8b6d8; border-radius: 50%; position: relative; }}
    .number-orbit::before {{ content: ""; position: absolute; inset: 7px; border: 1px dashed rgba(98,81,125,.35); border-radius: 50%; }}
    .number-orbit span {{ font: 600 2.5rem/1 Georgia, serif; color: var(--violet); }}
    .number-copy h3 {{ margin: 0 0 4px; font: 600 1.45rem/1.25 Georgia, "Noto Serif TC", serif; }}
    .number-copy p {{ margin: 3px 0; }}
    .eyebrow {{ color: var(--gold); }}
    .muted {{ color: var(--muted); font-size: .9rem; }}
    .insight-grid {{ display: grid; grid-template-columns: 1.2fr .8fr; gap: 18px; }}
    .panel {{ padding: clamp(24px, 4vw, 38px); background: var(--card); border: 1px solid var(--line); border-radius: 22px; box-shadow: 0 12px 32px rgba(42,36,32,.055); }}
    .panel.dark {{ color: white; border: 0; background: var(--violet-deep); }}
    .panel h3 {{ margin: 0 0 12px; font: 600 1.45rem/1.3 Georgia, "Noto Serif TC", serif; }}
    .panel ul {{ margin: 14px 0 0; padding-left: 1.2em; }}
    .panel li + li {{ margin-top: 7px; }}
    .practice {{ margin-top: 22px; padding: 18px 20px; border-left: 3px solid var(--gold); background: rgba(196,150,61,.1); border-radius: 0 12px 12px 0; }}
    .year-number {{ float: right; margin: -10px 0 12px 18px; font: 600 5rem/1 Georgia, serif; color: #ddc993; }}
    .grid-analysis {{ display: grid; grid-template-columns: minmax(320px, .95fr) minmax(300px, 1.05fr); gap: 22px; align-items: start; }}
    .life-grid-stage {{ position: relative; aspect-ratio: 1; padding: 12px; border: 1px solid #cabbd8; border-radius: 24px; background: linear-gradient(145deg, #f5eff9, #fffaf0); overflow: hidden; }}
    .grid-lines {{ position: absolute; inset: 12px; width: calc(100% - 24px); height: calc(100% - 24px); z-index: 1; overflow: visible; }}
    .grid-line {{ stroke: var(--gold); stroke-width: 7; stroke-linecap: round; opacity: .72; filter: drop-shadow(0 2px 3px rgba(110,78,24,.22)); }}
    .life-grid {{ position: relative; z-index: 2; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); gap: 10px; height: 100%; }}
    .grid-cell {{ position: relative; display: grid; place-items: center; align-content: center; min-width: 0; padding: 8px; border: 1px solid rgba(98,81,125,.18); border-radius: 16px; background: rgba(255,253,248,.90); color: #a6a1a8; }}
    .grid-cell.active {{ color: var(--violet-deep); border-color: rgba(98,81,125,.48); background: rgba(255,253,248,.95); box-shadow: 0 8px 24px rgba(42,36,32,.08); }}
    .grid-cell strong {{ font: 600 clamp(2rem, 5vw, 3.6rem)/1 Georgia, serif; }}
    .grid-cell small {{ margin-top: 3px; color: var(--muted); font-size: .7rem; }}
    .cell-markers {{ min-height: 24px; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 1px; margin-top: 5px; font: 800 1.1rem/1 ui-monospace, monospace; }}
    .marker.circle {{ color: #387db4; }}
    .marker.triangle {{ color: #388a62; }}
    .marker.square {{ color: #b94f45; }}
    .grid-details {{ display: grid; gap: 16px; }}
    .grid-summary {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .grid-stat {{ min-height: 112px; padding: 18px; border: 1px solid var(--line); border-radius: 16px; background: var(--card); }}
    .grid-stat span, .grid-stat small {{ display: block; color: var(--muted); font-size: .78rem; }}
    .grid-stat strong {{ display: block; margin: 4px 0; font: 600 2.1rem/1 Georgia, serif; color: var(--violet); }}
    .legend-row {{ display: flex; flex-wrap: wrap; gap: 8px 14px; padding: 14px 16px; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,253,248,.75); font-size: .83rem; }}
    .legend-row span {{ white-space: nowrap; }}
    .connection-list {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 8px; }}
    .connection-list li {{ display: flex; align-items: center; gap: 10px; padding: 11px 13px; border-radius: 12px; background: rgba(196,150,61,.10); }}
    .connection-swatch {{ width: 22px; height: 4px; border-radius: 999px; background: var(--gold); flex: 0 0 auto; }}
    .grid-method {{ margin: 0; padding: 15px 17px; border-left: 3px solid var(--sage); border-radius: 0 12px 12px 0; background: rgba(113,136,121,.10); color: #4f5b53; font-size: .86rem; }}
    .table-wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 20px; background: var(--card); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 700px; }}
    th, td {{ padding: 17px 18px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }}
    tr:last-child th, tr:last-child td {{ border-bottom: 0; }}
    th {{ width: 150px; color: var(--violet-deep); }}
    .trace {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: .88rem; color: #4f565b; }}
    .result-pill {{ display: inline-grid; place-items: center; min-width: 36px; height: 36px; padding: 0 9px; border-radius: 999px; color: white; background: var(--violet); font-weight: 800; }}
    .note {{ display: grid; grid-template-columns: 42px 1fr; gap: 14px; margin-top: 24px; padding: 22px; border: 1px solid #d9cfb8; border-radius: 18px; background: #fffaf0; }}
    .note .icon {{ width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; background: #ead6a5; font-weight: 900; }}
    .note p, .note ul {{ margin: 0; }}
    .note ul {{ padding-left: 1.1em; }}
    footer {{ margin-top: 58px; padding-top: 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: .88rem; }}
    footer strong {{ color: var(--ink); }}
    @media (max-width: 760px) {{
      .section-heading, .insight-grid, .grid-analysis {{ grid-template-columns: 1fr; }}
      .number-grid {{ grid-template-columns: 1fr; }}
      .number-card.primary {{ grid-column: auto; }}
      .hero {{ border-radius: 20px; }}
      .life-grid-stage {{ width: min(100%, 520px); margin-inline: auto; }}
    }}
    @media (max-width: 480px) {{
      .page {{ width: min(100% - 20px, 1120px); padding-top: 10px; }}
      .number-card {{ grid-template-columns: 66px 1fr; padding: 18px; gap: 14px; }}
      .number-orbit {{ width: 62px; }}
      .number-orbit span {{ font-size: 2rem; }}
    }}
    @media print {{
      body {{ background: white; }}
      body::before {{ display: none; }}
      .page {{ width: 100%; padding: 0; }}
      .hero, .panel.dark {{ print-color-adjust: exact; -webkit-print-color-adjust: exact; }}
      .section {{ break-inside: avoid; margin-top: 34px; }}
      .number-card, .panel, .table-wrap, .grid-cell {{ box-shadow: none; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header class="hero">
      <p class="kicker">Life Numerology · Symbolic Reflection</p>
      <h1>{safe_name}<br>生命靈數洞察報告</h1>
      <p class="lede">以可追溯的數字計算整理一組自我觀察線索。把它當成提問的入口，而不是替你決定人生的答案。</p>
      <div class="meta">
        <span>出生日期 · {safe_birth}</span>
        <span>目標流年 · {target_year}</span>
        <span>系統 · 現代畢達哥拉斯</span>
        <span>Y 規則 · 視為{y_rule}</span>
      </div>
    </header>

    <section class="section" aria-labelledby="snapshot-title">
      <div class="section-heading">
        <div><p class="eyebrow">01 · Core Numbers</p><h2 id="snapshot-title">核心數字速覽</h2></div>
        <p>每個數字描述不同觀察角度；生命路徑數是主軸，其餘數字用來補足節奏、表達與內在動機。</p>
      </div>
      <div class="number-grid">{cards}</div>
    </section>

    <section class="section" aria-labelledby="reading-title">
      <div class="section-heading">
        <div><p class="eyebrow">02 · Reading</p><h2 id="reading-title">把主題放回生活</h2></div>
        <p>{html.escape(integration)}</p>
      </div>
      <div class="insight-grid">
        <article class="panel">
          <h3>生命路徑 {numbers['life_path']['value']} · {html.escape(life_guide['title'])}</h3>
          <p>{html.escape(life_guide['theme'])}，可能是你在不同階段反覆遇見的練習。</p>
          <div class="insight-grid">
            <div><p class="eyebrow">可用資源</p><ul>{strength_items}</ul></div>
            <div><p class="eyebrow">需要留意</p><ul>{shadow_items}</ul></div>
          </div>
          <p class="practice"><strong>本週微行動：</strong>{html.escape(life_guide['practice'])}</p>
        </article>
        <article class="panel dark">
          <span class="year-number">{numbers['personal_year']['value']}</span>
          <p class="kicker">{target_year} Personal Year</p>
          <h3>{html.escape(personal_guide['title'])}</h3>
          <p>今年的象徵節奏偏向「{html.escape(personal_guide['theme'])}」。它適合用來安排反思焦點，不代表事件必然發生。</p>
          <p class="practice"><strong>年度提醒：</strong>{html.escape(personal_guide['practice'])}</p>
        </article>
      </div>
    </section>

    <section class="section" aria-labelledby="grid-title">
      <div class="section-heading">
        <div><p class="eyebrow">03 · Birth Grid</p><h2 id="grid-title">九宮格與連線</h2></div>
        <p>參考頁規則：圓形是出生日期原始數字、三角形是後天衍生數字、方形是最終根數；任一標記出現即視為該格啟動。</p>
      </div>
      <div class="grid-analysis">
        <div class="life-grid-stage">
          <svg class="grid-lines" viewBox="0 0 300 300" aria-hidden="true">{grid_lines}</svg>
          <div class="life-grid">{grid_cells}</div>
        </div>
        <div class="grid-details">
          <div class="grid-summary">
            <div class="grid-stat">
              <span>生日原始數字</span>
              <strong>{html.escape(raw_digits_text)}</strong>
              <small>數字 0 不進九宮格</small>
            </div>
            <div class="grid-stat">
              <span>後天數</span>
              <strong>{birth_grid['major']}</strong>
              <small>生日所有數字相加</small>
            </div>
            {intermediate_card}
            <div class="grid-stat">
              <span>九宮格根數</span>
              <strong>{birth_grid['root']}</strong>
              <small>連續相加至個位數</small>
            </div>
            <div class="grid-stat">
              <span>完整連線</span>
              <strong>{birth_grid['connection_count']}</strong>
              <small>三格皆有標記才成立</small>
            </div>
          </div>
          <div class="legend-row" aria-label="九宮格標記圖例">
            <span><b class="marker circle">○</b> 出生原始數字</span>
            <span><b class="marker triangle">△</b> 後天衍生數字</span>
            <span><b class="marker square">□</b> 最終根數</span>
          </div>
          <div>
            <p class="eyebrow">已形成連線</p>
            <ul class="connection-list">{connection_items}</ul>
          </div>
          <p class="grid-method">連線只描述九宮格中的數字覆蓋關係，不代表能力高低或事件必然發生；它也不取代本報告採用的生命路徑數計算。</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="trace-title">
      <div class="section-heading">
        <div><p class="eyebrow">04 · Calculation</p><h2 id="trace-title">計算過程</h2></div>
        <p>日期先分別化約月、日、年；姓名採拉丁字母 1–9 循環映射。主數 11、22、33 在指定步驟保留。</p>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>指標</th><th>可追溯算式</th><th>結果</th></tr></thead>
          <tbody>{trace_rows}</tbody>
        </table>
      </div>
      {f'<div class="note"><div class="icon">i</div><div><ul>{warning_html}</ul></div></div>' if warning_html else ''}
    </section>

    <section class="section" aria-labelledby="questions-title">
      <div class="section-heading">
        <div><p class="eyebrow">05 · Reflection</p><h2 id="questions-title">三個帶走的問題</h2></div>
        <p>數字的價值不在標籤，而在它是否幫你看見更具體的選擇。</p>
      </div>
      <div class="number-grid">
        <article class="panel"><p class="eyebrow">01</p><h3>我正在哪件事上，把優勢用成了壓力？</h3></article>
        <article class="panel"><p class="eyebrow">02</p><h3>今年的節奏，需要我開始、深化、調整，還是完成什麼？</h3></article>
        <article class="panel"><p class="eyebrow">03</p><h3>下一個七天內，哪個小行動最能驗證我的理解？</h3></article>
        <article class="panel"><p class="eyebrow">Method</p><h3>保留有共鳴的提示，也允許自己不同意。</h3></article>
      </div>
    </section>

    <footer>
      <p><strong>使用界線：</strong>{html.escape(data['disclaimer'])} 不應據此做醫療、法律、財務、雇用或安全關鍵決策。</p>
      <p><strong>隱私：</strong>本報告由本機腳本產生，不載入遠端字型、分析碼或第三方服務；資料只存在於你指定的這個檔案。</p>
    </footer>
  </main>
</body>
</html>
"""


def parse_birth_date(raw: str) -> date:
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError("出生日期必須是有效的公曆 YYYY-MM-DD。") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a traceable Traditional Chinese numerology report.")
    parser.add_argument("--birth-date", required=True, help="Gregorian birth date in YYYY-MM-DD format")
    parser.add_argument("--name", help="Full Romanized birth name; optional for date-only reports")
    parser.add_argument("--target-year", type=int, default=date.today().year, help="Personal-year target; default: current year")
    parser.add_argument("--y-as-vowel", action="store_true", help="Treat Y as a vowel; default: consonant")
    parser.add_argument("--format", choices=("html", "json"), default="html", help="Output format")
    parser.add_argument("--output", help="HTML output path; required for HTML format")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        birth_date = parse_birth_date(args.birth_date)
        data = build_profile(birth_date, args.name, args.target_year, args.y_as_vowel)
        if args.format == "json":
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        if not args.output:
            raise ValueError("HTML 模式需要 --output PATH.html。")
        output = Path(args.output)
        if output.suffix.lower() != ".html":
            raise ValueError("HTML 輸出路徑必須以 .html 結尾。")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_html(data), encoding="utf-8")
        receipt = {
            "status": "ok",
            "output": str(output.resolve()),
            "core_numbers": {key: value["value"] for key, value in data["numbers"].items()},
            "warnings": data["warnings"],
        }
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
