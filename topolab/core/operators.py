
"""Topological operators for finite topological spaces."""

from .finite_spaces import FiniteSet, FiniteTopologicalSpace


def interior(
    space: FiniteTopologicalSpace,
    subset: FiniteSet,
) -> FiniteSet:
    """Return the largest open subset contained in A."""
    _validate_subset(space, subset)

    result = frozenset()

    for open_set in space.open_sets:
        if open_set.issubset(subset):
            result = result | open_set

    return result


def closure(space: FiniteTopologicalSpace, subset: FiniteSet) -> FiniteSet:
    """Return the smallest closed set containing A."""
    _validate_subset(space, subset)

    result = space.universe

    for open_set in space.open_sets:
        if open_set.isdisjoint(subset):
            closed_set = space.universe - open_set
            result = result & closed_set

    return result


def boundary(
    space: FiniteTopologicalSpace,
    subset: FiniteSet,
) -> FiniteSet:
    """Return the boundary of A: closure(A) minus interior(A)."""
    return closure(space, subset) - interior(space, subset)


def _validate_subset(
    space: FiniteTopologicalSpace,
    subset: FiniteSet,
) -> None:
    """Ensure that A is a subset of the underlying universe."""
    if not subset.issubset(space.universe):
        raise ValueError("The selected set must be a subset of X.")
