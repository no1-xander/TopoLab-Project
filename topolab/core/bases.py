
"""Basis and subbasis operations for finite topological spaces."""

from itertools import combinations
from typing import Iterable

FiniteSet = frozenset[str]


def _format_set(subset: FiniteSet) -> str:
    if not subset:
        return "∅"
    return "{" + ", ".join(sorted(subset)) + "}"


def _validate_family(
    universe: FiniteSet,
    family: Iterable[Iterable[str]]
) -> frozenset[FiniteSet]:
    result = frozenset(frozenset(item) for item in family)

    for subset in result:
        if not subset.issubset(universe):
            raise ValueError(
                f"{_format_set(subset)} contains elements outside X."
            )

    return result


def is_basis(
    universe: FiniteSet,
    family: Iterable[Iterable[str]]
) -> bool:
    """Check the two basis conditions for a finite set."""
    basis = _validate_family(universe, family)

    # Every point of X must belong to at least one basis element.
    covered = frozenset().union(*basis) if basis else frozenset()

    if covered != universe:
        return False

    # Every point in B1 ∩ B2 must belong to a basis element
    # contained in B1 ∩ B2.
    for first, second in combinations(basis, 2):
        intersection = first & second

        for point in intersection:
            if not any(
                point in candidate
                and candidate.issubset(intersection)
                for candidate in basis
            ):
                return False

    return True


def generate_topology(
    universe: FiniteSet,
    basis: Iterable[Iterable[str]]
) -> frozenset[FiniteSet]:
    """Generate all unions of members of a valid basis."""
    basis = _validate_family(universe, basis)

    if not is_basis(universe, basis):
        raise ValueError("The supplied family is not a basis.")

    elements = tuple(basis)
    topology = {frozenset()}

    for size in range(1, len(elements) + 1):
        for selection in combinations(elements, size):
            topology.add(
                frozenset().union(*selection)
            )

    return frozenset(topology)


def finite_intersections(
    universe: FiniteSet,
    subbasis: Iterable[Iterable[str]]
) -> frozenset[FiniteSet]:
    """Return all finite intersections of subbasis members, including X."""
    family = _validate_family(universe, subbasis)
    elements = tuple(family)

    result = {universe}

    for size in range(1, len(elements) + 1):
        for selection in combinations(elements, size):
            result.add(
                frozenset.intersection(*selection)
            )

    return frozenset(result)


def generate_topology_from_subbasis(
    universe: FiniteSet,
    subbasis: Iterable[Iterable[str]]
) -> frozenset[FiniteSet]:
    """Generate the topology determined by a subbasis."""
    basis = finite_intersections(universe, subbasis)

    return generate_topology(universe, basis)
