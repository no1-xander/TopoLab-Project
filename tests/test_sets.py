import unittest

from topolab.core.sets import (
    are_disjoint, are_equal, cardinality, cartesian_product, complement,
    compose, difference, image, intersection, intersection_all,
    inverse_bijection, is_bijective, is_injective, is_subset, is_surjective,
    power_set, preimage, union, union_all,
)


class TestFiniteSetOperations(unittest.TestCase):
    def setUp(self):
        self.universe = {1, 2, 3, 4}
        self.a = {1, 2, 3}
        self.b = {3, 4}

    def test_subset_and_double_inclusion_equality(self):
        self.assertTrue(is_subset({1, 2}, self.a))
        self.assertFalse(is_subset({1, 5}, self.a))
        self.assertTrue(are_equal({1, 2, 2}, {2, 1}))

    def test_power_set_has_two_to_n_members(self):
        result = power_set({1, 2, 3})
        self.assertEqual(len(result), 8)
        self.assertIn(frozenset(), result)
        self.assertIn(frozenset({1, 2, 3}), result)

    def test_union_intersection_and_difference(self):
        self.assertEqual(union(self.a, self.b), frozenset({1, 2, 3, 4}))
        self.assertEqual(intersection(self.a, self.b), frozenset({3}))
        self.assertEqual(difference(self.a, self.b), frozenset({1, 2}))

    def test_complement_uses_explicit_universe(self):
        self.assertEqual(complement({1, 3}, self.universe), frozenset({2, 4}))

    def test_complement_rejects_elements_outside_universe(self):
        with self.assertRaises(ValueError):
            complement({1, 9}, self.universe)

    def test_disjoint_sets(self):
        self.assertTrue(are_disjoint({1, 2}, {3, 4}))
        self.assertFalse(are_disjoint(self.a, self.b))

    def test_union_of_empty_family(self):
        self.assertEqual(union_all([]), frozenset())

    def test_intersection_of_empty_family_is_universe(self):
        self.assertEqual(intersection_all([], self.universe), frozenset(self.universe))

    def test_intersection_of_family(self):
        self.assertEqual(
            intersection_all([{1, 2, 3}, {2, 3}, {2, 4}], self.universe),
            frozenset({2}),
        )

    def test_cartesian_product_preserves_order(self):
        result = cartesian_product({1, 2}, {"a"})
        self.assertEqual(result, frozenset({(1, "a"), (2, "a")}))
        self.assertNotEqual(cartesian_product({1}, {2}), cartesian_product({2}, {1}))

    def test_cardinality_counts_distinct_elements(self):
        self.assertEqual(cardinality([1, 1, 2, 3]), 3)


class TestFiniteFunctions(unittest.TestCase):
    def setUp(self):
        self.function = {"a": 1, "b": 2, "c": 2}

    def test_image_of_subset(self):
        self.assertEqual(image(self.function, {"a", "c"}), frozenset({1, 2}))

    def test_image_rejects_non_domain_element(self):
        with self.assertRaises(ValueError):
            image(self.function, {"z"})

    def test_preimage_is_defined_without_inverse_function(self):
        self.assertEqual(preimage(self.function, {2}), frozenset({"b", "c"}))
        self.assertEqual(preimage(self.function, {9}), frozenset())

    def test_injective(self):
        self.assertFalse(is_injective(self.function))
        self.assertTrue(is_injective({"a": 1, "b": 2}))

    def test_surjective_depends_on_codomain(self):
        self.assertTrue(is_surjective(self.function, {1, 2}))
        self.assertFalse(is_surjective(self.function, {1, 2, 3}))

    def test_map_values_must_belong_to_codomain(self):
        with self.assertRaises(ValueError):
            is_surjective({"a": 4}, {1, 2})

    def test_bijective_and_inverse_function(self):
        bijection = {"a": 1, "b": 2}
        self.assertTrue(is_bijective(bijection, {1, 2}))
        self.assertEqual(inverse_bijection(bijection, {1, 2}), {1: "a", 2: "b"})

    def test_inverse_function_rejects_non_bijection(self):
        with self.assertRaises(ValueError):
            inverse_bijection(self.function, {1, 2})

    def test_composition_order_is_first_then_second(self):
        f = {"a": 1, "b": 2}
        g = {1: "x", 2: "y"}
        self.assertEqual(compose(f, g), {"a": "x", "b": "y"})

    def test_composition_rejects_incompatible_maps(self):
        with self.assertRaises(ValueError):
            compose({"a": 1}, {2: "x"})

    def test_image_of_union_is_union_of_images(self):
        f = {"a": 1, "b": 2, "c": 2}
        left = image(f, {"a", "b"} | {"c"})
        right = image(f, {"a", "b"}) | image(f, {"c"})
        self.assertEqual(left, right)

    def test_image_of_intersection_is_included_in_intersection_of_images(self):
        f = {"a": 1, "b": 1, "c": 2}
        left = image(f, {"a", "b"} & {"b", "c"})
        right = image(f, {"a", "b"}) & image(f, {"b", "c"})
        self.assertTrue(left.issubset(right))

    def test_preimage_preserves_union_intersection_and_difference(self):
        f = {"a": 1, "b": 2, "c": 3}
        first, second = {1, 2}, {2, 3}
        self.assertEqual(preimage(f, first | second), preimage(f, first) | preimage(f, second))
        self.assertEqual(preimage(f, first & second), preimage(f, first) & preimage(f, second))
        self.assertEqual(preimage(f, first - second), preimage(f, first) - preimage(f, second))

    def test_image_preimage_inclusions(self):
        f = {"a": 1, "b": 1, "c": 2}
        target = {1, 3}
        source = {"a"}
        self.assertTrue(image(f, preimage(f, target)).issubset(target))
        self.assertTrue(source.issubset(preimage(f, image(f, source))))


if __name__ == "__main__":
    unittest.main()
