"""Topological operators for finite topological spaces."""

from itertools import combinations

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

def complement(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> FiniteSet:
    """Return the complement of a subset relative to X."""
    _validate_subset(space, subset)
    return space.universe - subset


def is_open(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> bool:
    """Check whether a subset belongs to the topology."""
    _validate_subset(space, subset)
    return subset in space.open_sets


def is_closed(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> bool:
    """A set is closed when its complement is open."""
    _validate_subset(space, subset)
    return complement(space, subset) in space.open_sets


def is_clopen(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> bool:
    """Check whether a subset is both open and closed."""
    return is_open(space, subset) and is_closed(space, subset)


def closed_sets(
    space: FiniteTopologicalSpace
) -> frozenset[FiniteSet]:
    """Return the family of all closed subsets of X."""
    return frozenset(
        subset
        for subset in _all_subsets(space.universe)
        if is_closed(space, subset)
    )


def _all_subsets(universe: FiniteSet):
    """Generate every subset of a finite universe."""
    elements = tuple(universe)

    for size in range(len(elements) + 1):
        for subset in combinations(elements, size):
            yield frozenset(subset)


def neighborhoods(
    space: FiniteTopologicalSpace,
    point: str
) -> frozenset[FiniteSet]:
    """
    Return all neighborhoods of a point.

    U is a neighborhood of x if some open V satisfies
    x in V and V is a subset of U.
    """
    if point not in space.universe:
        raise ValueError("The selected point must belong to X.")

    result = set()

    for candidate in _all_subsets(space.universe):
        for open_set in space.open_sets:
            if point in open_set and open_set.issubset(candidate):
                result.add(candidate)
                break

    return frozenset(result)


def is_accumulation_point(
    space: FiniteTopologicalSpace,
    subset: FiniteSet,
    point: str
) -> bool:
    """
    Check whether every neighborhood of point
    intersects subset without the point itself.
    """
    _validate_subset(space, subset)

    if point not in space.universe:
        raise ValueError("The selected point must belong to X.")

    remainder = subset - {point}

    for open_set in space.open_sets:
        if point in open_set and open_set.isdisjoint(remainder):
            return False

    return True


def accumulation_points(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> FiniteSet:
    """Return all accumulation points of a subset."""
    _validate_subset(space, subset)

    return frozenset(
        point
        for point in space.universe
        if is_accumulation_point(space, subset, point)
    )


def isolated_points(
    space: FiniteTopologicalSpace,
    subset: FiniteSet
) -> FiniteSet:
    """
    Return points x in subset for which an open U exists
    such that U intersect subset equals {x}.
    """
    _validate_subset(space, subset)

    result = set()

    for point in subset:
        for open_set in space.open_sets:
            if open_set.intersection(subset) == {point}:
                result.add(point)
                break

    return frozenset(result)


def hausdorff_separation(
    space: FiniteTopologicalSpace,
    first_point: str,
    second_point: str
) -> tuple[FiniteSet, FiniteSet] | None:
    """
    Find disjoint open neighborhoods of two distinct points.

    Return the pair of neighborhoods if one exists;
    otherwise return None.
    """
    if first_point not in space.universe:
        raise ValueError("The first point must belong to X.")

    if second_point not in space.universe:
        raise ValueError("The second point must belong to X.")

    if first_point == second_point:
        raise ValueError("The two points must be distinct.")

    first_neighborhoods = [
        open_set for open_set in space.open_sets
        if first_point in open_set
    ]

    second_neighborhoods = [
        open_set for open_set in space.open_sets
        if second_point in open_set
    ]

    for first in first_neighborhoods:
        for second in second_neighborhoods:
            if first.isdisjoint(second):
                return first, second

    return None


def is_hausdorff(space: FiniteTopologicalSpace) -> bool:
    """Check the Hausdorff separation property."""
    points = tuple(space.universe)

    for first_point, second_point in combinations(points, 2):
        if hausdorff_separation(
            space, first_point, second_point
        ) is None:
            return False

    return True
