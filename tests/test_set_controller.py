import unittest
from topolab.services.set_controller import SetController


class TestSetControllerParsing(unittest.TestCase):
    def test_parse_plain_and_braced_sets(self):
        self.assertEqual(SetController._parse_set("a, b", "A"), {"a", "b"})
        self.assertEqual(SetController._parse_set("{a, b}", "A"), {"a", "b"})

    def test_parse_empty_set_notations(self):
        self.assertEqual(SetController._parse_set("∅", "A"), set())
        self.assertEqual(SetController._parse_set("{}", "A"), set())
        self.assertEqual(SetController._parse_set("", "A"), set())

    def test_rejects_duplicate_elements(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            SetController._parse_set("a, b, a", "A")

    def test_rejects_missing_elements(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            SetController._parse_set("a,,b", "A")

    def test_rejects_unbalanced_braces(self):
        with self.assertRaisesRegex(ValueError, "balanced braces"):
            SetController._parse_set("{a, b", "A")

    def test_rejects_unsupported_element_syntax(self):
        with self.assertRaisesRegex(ValueError, "invalid element"):
            SetController._parse_set("a, x-y", "A")


class TestSetControllerCalculations(unittest.TestCase):
    def setUp(self):
        self.controller = SetController()

    def calculate(self, index, a="a, b", b="b, c", universe="a, b, c, d"):
        return self.controller.calculate(index, a, b, universe)

    def test_union(self):
        result = self.calculate(0)
        self.assertTrue(result["ok"])
        self.assertIn("{a, b, c}", result["result"])

    def test_intersection(self):
        self.assertIn("{b}", self.calculate(1)["result"])

    def test_difference_is_ordered(self):
        self.assertIn("A \\ B = {a}", self.calculate(2)["result"])

    def test_complement_is_relative_to_universe(self):
        result = self.calculate(3, a="a, b", universe="a, b, c")
        self.assertIn("{c}", result["result"])

    def test_complement_rejects_set_outside_universe(self):
        result = self.calculate(3, a="z", universe="a, b, c")
        self.assertFalse(result["ok"])
        self.assertIn("subset of the universe", result["message"])

    def test_power_set_has_all_subsets(self):
        result = self.calculate(4, a="a, b")
        self.assertTrue(result["ok"])
        self.assertIn("2^2 = 4", result["explanation"])
        self.assertIn("∅", result["result"])
        self.assertIn("{a, b}", result["result"])

    def test_power_set_size_limit_is_reported(self):
        result = self.calculate(4, a="a, b, c, d, e, f, g, h, i")
        self.assertFalse(result["ok"])
        self.assertIn("limited", result["message"])

    def test_cartesian_product_keeps_ordered_pairs(self):
        result = self.calculate(5, a="a, b", b="1")
        self.assertIn("(a, 1)", result["result"])
        self.assertIn("(b, 1)", result["result"])

    def test_cartesian_product_limit_is_reported(self):
        result = self.calculate(
            5, a="a, b, c, d, e, f, g, h, i, j, k",
            b="1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        )
        self.assertFalse(result["ok"])
        self.assertIn("limited", result["message"])

    def test_subset_test(self):
        self.assertIn("A ⊆ B: True", self.calculate(6, a="a", b="a, b")["result"])

    def test_equality_test(self):
        self.assertIn("A = B: True", self.calculate(7, a="a, b", b="b, a")["result"])

    def test_disjointness_test(self):
        self.assertIn(
            "A and B are disjoint: True",
            self.calculate(8, a="a", b="b")["result"],
        )

    def test_invalid_operation_index(self):
        result = self.calculate(99)
        self.assertFalse(result["ok"])
        self.assertIn("valid", result["message"])


if __name__ == "__main__":
    unittest.main()
