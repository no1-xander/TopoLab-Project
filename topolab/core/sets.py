"""Finite set and finite-map operations used throughout TopoLab.

The functions in this module work with finite, hashable Python objects. They
model the elementary set constructions in Chapter 1; they do not attempt to
enumerate infinite sets such as R or Q.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from itertools import chain, combinations
from typing import TypeVar


T = TypeVar("T", bound=Hashable)
U = TypeVar("U", bound=Hashable)
V = TypeVar("V", bound=Hashable)
FiniteSet = frozenset[T]
FiniteMap = Mapping[T, U]


def as_frozenset(elements: Iterable[T]) -> frozenset[T]:
    """Return an immutable set representation of elements."""
    return frozenset(elements)


def is_subset(first: Iterable[T], second: Iterable[T]) -> bool:
    """Return whether every element of first belongs to second."""
    return frozenset(first).issubset(frozenset(second))


def are_equal(first: Iterable[T], second: Iterable[T]) -> bool:
    """Test set equality by mutual inclusion."""
    return frozenset(first) == frozenset(second)


def power_set(elements: Iterable[T]) -> frozenset[frozenset[T]]:
    """Return P(X), the family of all subsets of a finite set X.

    The result contains 2**n subsets for an input with n distinct
    elements, so this operation grows exponentially.
    """
    values = tuple(frozenset(elements))
    return frozenset(
        frozenset(subset)
        for size in range(len(values) + 1)
        for subset in combinations(values, size)
    )


def union(first: Iterable[T], second: Iterable[T]) -> frozenset[T]:
    """Return A union B."""
    return frozenset(first) | frozenset(second)


def intersection(first: Iterable[T], second: Iterable[T]) -> frozenset[T]:
    """Return A intersect B."""
    return frozenset(first) & frozenset(second)


def difference(first: Iterable[T], second: Iterable[T]) -> frozenset[T]:
    """Return A minus B."""
    return frozenset(first) - frozenset(second)


def complement(subset: Iterable[T], universe: Iterable[T]) -> frozenset[T]:
    """Return the complement E minus A relative to the explicit universe E."""
    whole = frozenset(universe)
    selected = frozenset(subset)
    if not selected.issubset(whole):
        raise ValueError(
            "The set whose complement is requested must be a subset of the universe."
        )
    return whole - selected


def are_disjoint(first: Iterable[T], second: Iterable[T]) -> bool:
    """Return whether A intersect B is empty."""
    return frozenset(first).isdisjoint(frozenset(second))


def union_all(family: Iterable[Iterable[T]]) -> frozenset[T]:
    """Return the union of a family of sets (the empty union is empty)."""
    return frozenset(chain.from_iterable(family))


def intersection_all(
    family: Iterable[Iterable[T]], universe: Iterable[T]
) -> frozenset[T]:
    """Return the intersection of a family, relative to its ambient universe.

    Supplying the universe makes the empty-family convention explicit: the
    intersection of no subsets of E is E.
    """
    result = frozenset(universe)
    for member in family:
        result = result.intersection(member)
    return result


def cartesian_product(
    first: Iterable[T], second: Iterable[U]
) -> frozenset[tuple[T, U]]:
    """Return A x B as a set of ordered pairs."""
    return frozenset((left, right) for left in first for right in second)


def cardinality(elements: Iterable[T]) -> int:
    """Return the number of distinct elements in a finite set."""
    return len(frozenset(elements))


def _validate_finite_map(mapping: Mapping[T, U], domain: Iterable[T]) -> frozenset[T]:
    """Validate that a dictionary-like map is defined on exactly the domain."""
    expected = frozenset(domain)
    actual = frozenset(mapping.keys())
    if actual != expected:
        missing = expected - actual
        extra = actual - expected
        details = []
        if missing:
            details.append(f"missing domain elements: {missing!r}")
        if extra:
            details.append(f"keys outside the domain: {extra!r}")
        raise ValueError(
            "The mapping must be defined on exactly the stated domain ("
            + "; ".join(details)
            + ")."
        )
    return expected


def image(mapping: Mapping[T, U], subset: Iterable[T]) -> frozenset[U]:
    """Return f(A) for A contained in the domain of a finite map f."""
    selected = frozenset(subset)
    domain = frozenset(mapping.keys())
    if not selected.issubset(domain):
        raise ValueError("The image can only be taken of a subset of the map's domain.")
    return frozenset(mapping[element] for element in selected)


def preimage(mapping: Mapping[T, U], subset: Iterable[U]) -> frozenset[T]:
    """Return f^-1(B), the preimage of B under a finite map f."""
    selected = frozenset(subset)
    return frozenset(element for element, value in mapping.items() if value in selected)


def is_injective(mapping: Mapping[T, U], domain: Iterable[T] | None = None) -> bool:
    """Return whether a finite map is one-to-one on its stated domain."""
    actual_domain = (
        frozenset(mapping.keys())
        if domain is None
        else _validate_finite_map(mapping, domain)
    )
    values = [mapping[element] for element in actual_domain]
    return len(values) == len(set(values))


def is_surjective(mapping: Mapping[T, U], codomain: Iterable[U]) -> bool:
    """Return whether every element of the stated codomain is attained."""
    target = frozenset(codomain)
    if not frozenset(mapping.values()).issubset(target):
        raise ValueError("Every map value must belong to the stated codomain.")
    return frozenset(mapping.values()) == target


def is_bijective(mapping: Mapping[T, U], codomain: Iterable[U]) -> bool:
    """Return whether a finite map is both injective and surjective."""
    return is_injective(mapping) and is_surjective(mapping, codomain)


def compose(
    first: Mapping[T, U], second: Mapping[U, V]
) -> dict[T, V]:
    """Return second composed with first; first acts before second."""
    first_values = frozenset(first.values())
    second_domain = frozenset(second.keys())
    if not first_values.issubset(second_domain):
        raise ValueError(
            "The image of the first map must be contained in the domain of the second map."
        )
    return {element: second[value] for element, value in first.items()}


def inverse_bijection(
    mapping: Mapping[T, U], codomain: Iterable[U]
) -> dict[U, T]:
    """Return the inverse function of a finite bijection.

    This is different from preimage(), which is defined for every map
    and returns a set for any target subset.
    """
    target = frozenset(codomain)
    if not is_bijective(mapping, target):
        raise ValueError("An inverse function exists here only for a bijective map.")
    return {value: element for element, value in mapping.items()}


__all__ = [
    "FiniteMap", "FiniteSet", "are_disjoint", "are_equal", "as_frozenset",
    "cardinality", "cartesian_product", "complement", "compose",
    "difference", "image", "intersection", "intersection_all",
    "inverse_bijection", "is_bijective", "is_injective", "is_subset",
    "is_surjective", "power_set", "preimage", "union", "union_all",
]
