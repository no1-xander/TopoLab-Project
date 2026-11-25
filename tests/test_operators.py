
import unittest

from topolab.core.finite_spaces import FiniteTopologicalSpace
from topolab.core.operators import interior, closure, boundary


class TestTopologicalOperators(unittest.TestCase):

    def setUp(self):
        self.space = FiniteTopologicalSpace(
            {"a", "b", "c"},
            [
                set(),
                {"a"},
                {"a", "b"},
                {"a", "b", "c"},
            ],
        )

    def test_interior(self):
        self.assertEqual(
            interior(self.space, frozenset({"b", "c"})),
            frozenset(),
        )

    def test_closure(self):
        self.assertEqual(
            closure(self.space, frozenset({"b"})),
            frozenset({"b", "c"}),
        )

    def test_boundary(self):
        self.assertEqual(
            boundary(self.space, frozenset({"b"})),
            frozenset({"b", "c"}),
        )

    def test_invalid_subset(self):
        with self.assertRaises(ValueError):
            interior(self.space, frozenset({"z"}))


if __name__ == "__main__":
    unittest.main()
