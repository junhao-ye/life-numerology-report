import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from generate_report import (  # noqa: E402
    build_profile,
    calculate_birth_grid,
    calculate_date_numbers,
    calculate_name_numbers,
    normalize_latin_name,
    reduce_number,
    render_html,
)


class ReductionTests(unittest.TestCase):
    def test_preserves_master_numbers(self):
        self.assertEqual(reduce_number(11), (11, [11]))
        self.assertEqual(reduce_number(22), (22, [22]))
        self.assertEqual(reduce_number(33), (33, [33]))

    def test_can_force_single_digit(self):
        self.assertEqual(reduce_number(22, preserve_master=False), (4, [22, 4]))


class DateNumberTests(unittest.TestCase):
    def test_known_life_path(self):
        numbers = calculate_date_numbers(date(1992, 7, 16), 2027)
        self.assertEqual(numbers["life_path"]["value"], 8)
        self.assertEqual(numbers["birthday"]["value"], 7)
        self.assertEqual(numbers["attitude"]["value"], 5)
        self.assertEqual(numbers["personal_year"]["value"], 7)

    def test_master_life_path(self):
        numbers = calculate_date_numbers(date(1989, 1, 1), 2026)
        self.assertEqual(numbers["life_path"]["value"], 11)


class BirthGridTests(unittest.TestCase):
    def test_reference_compatible_counts_and_connections(self):
        grid = calculate_birth_grid(date(1992, 7, 16))
        self.assertEqual(grid["raw_digits"], [1, 9, 9, 2, 0, 7, 1, 6])
        self.assertEqual(grid["major"], 35)
        self.assertIsNone(grid["intermediate"])
        self.assertEqual(grid["root"], 8)
        self.assertEqual(grid["cells"]["1"]["birth_count"], 2)
        self.assertEqual(grid["cells"]["9"]["birth_count"], 2)
        self.assertEqual(grid["cells"]["3"]["derived_count"], 1)
        self.assertEqual(grid["cells"]["8"]["root_count"], 1)
        lines = {tuple(connection["digits"]) for connection in grid["connections"]}
        self.assertEqual(lines, {(1, 2, 3), (7, 8, 9), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)})

    def test_zero_is_not_a_grid_cell_and_no_line_is_forced(self):
        grid = calculate_birth_grid(date(2000, 1, 1))
        self.assertNotIn("0", grid["cells"])
        self.assertEqual(grid["connection_count"], 0)

    def test_repeated_intermediate_is_labelled_excellence(self):
        grid = calculate_birth_grid(date(1990, 1, 9))
        self.assertEqual(grid["major"], 29)
        self.assertEqual(grid["intermediate"], 11)
        self.assertEqual(grid["intermediate_label"], "卓越數")
        self.assertEqual(grid["root"], 2)


class NameNumberTests(unittest.TestCase):
    def test_avery_lin_default_y_consonant(self):
        numbers = calculate_name_numbers("Avery Lin", life_path=8)
        self.assertEqual(numbers["expression"]["value"], 7)
        self.assertEqual(numbers["soul_urge"]["value"], 6)
        self.assertEqual(numbers["personality"]["value"], 1)
        self.assertEqual(numbers["maturity"]["value"], 6)

    def test_y_can_be_vowel(self):
        numbers = calculate_name_numbers("Avery Lin", life_path=8, y_as_vowel=True)
        self.assertEqual(numbers["soul_urge"]["value"], 22)
        self.assertEqual(numbers["personality"]["value"], 3)

    def test_accents_are_normalized(self):
        self.assertEqual(normalize_latin_name("François"), "FRANCOIS")

    def test_non_latin_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "羅馬拼音"):
            calculate_name_numbers("王小明", life_path=1)


class HtmlTests(unittest.TestCase):
    def test_date_only_report_has_warning_and_disclaimer(self):
        data = build_profile(date(1992, 7, 16), None, 2027, False)
        output = render_html(data)
        self.assertIn("日期限定版", output)
        self.assertIn("略過表達數", output)
        self.assertIn("不是科學預測", output)
        self.assertIn("九宮格與連線", output)
        self.assertIn("grid-line", output)

    def test_user_input_is_escaped(self):
        data = build_profile(date(1992, 7, 16), "A <script>alert(1)</script>", 2027, False)
        output = render_html(data)
        self.assertNotIn("<script>", output)
        self.assertIn("&lt;script&gt;", output)

    def test_html_can_be_written_as_utf8(self):
        data = build_profile(date(1992, 7, 16), "Avery Lin", 2027, False)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "report.html"
            target.write_text(render_html(data), encoding="utf-8")
            self.assertTrue(target.exists())
            self.assertIn("生命靈數洞察報告", target.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
