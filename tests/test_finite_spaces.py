
import unittest

from topolab.core.finite_spaces import FiniteTopologicalSpace


class TestFiniteTopologicalSpace(unittest.TestCase):

    def test_valid_topology(self):
        space = FiniteTopologicalSpace(
            {"a", "b", "c"},
            [
                set(),
                {"a"},
                {"a", "b"},
                {"a", "b", "c"},
            ],
        )

        self.assertTrue(space.validate().is_topology)

    def test_missing_union(self):
        space = FiniteTopologicalSpace(
            {"a", "b", "c"},
            [
                set(),
                {"a"},
                {"b"},
                {"a", "b", "c"},
            ],
        )

        result = space.validate()
        self.assertFalse(result.is_topology)
        self.assertTrue(
            any("unions" in error for error in result.errors)
        )

    def test_missing_intersection(self):
        space = FiniteTopologicalSpace(
            {"a", "b", "c"},
            [
                set(),
                {"a", "b"},
                {"b", "c"},
                {"a", "b", "c"},
            ],
        )

        result = space.validate()
        self.assertFalse(result.is_topology)
        self.assertTrue(
            any("intersections" in error for error in result.errors)
        )

    def test_missing_empty_set(self):
        space = FiniteTopologicalSpace(
            {"a", "b"},
            [{"a"}, {"a", "b"}],
        )

        result = space.validate()
        self.assertFalse(result.is_topology)
        self.assertTrue(
            any("empty set" in error for error in result.errors)
        )

    def test_missing_universe(self):
        space = FiniteTopologicalSpace(
            {"a", "b"},
            [set(), {"a"}],
        )

        result = space.validate()
        self.assertFalse(result.is_topology)
        self.assertTrue(
            any("whole set X" in error for error in result.errors)
        )

    def test_element_outside_universe(self):
        space = FiniteTopologicalSpace(
            {"a", "b"},
            [set(), {"a"}, {"a", "b"}, {"a", "b", "c"}],
        )

        result = space.validate()
        self.assertFalse(result.is_topology)
        self.assertTrue(
            any("outside X" in error for error in result.errors)
        )


if __name__ == "__main__":
    unittest.main()
