"""Exact calculations for user-entered finite topological spaces."""
from topolab.core.finite_spaces import FiniteTopologicalSpace
from topolab.core.operators import (accumulation_points, boundary, closed_sets,
    closure, interior, is_hausdorff, isolated_points)


def _labels(text, allow_empty=True):
    if not text.strip():
        if allow_empty:
            return frozenset()
        raise ValueError("Enter at least one point in X.")
    values = [item.strip() for item in text.split(",")]
    if any(not value for value in values) or len(values) != len(set(values)):
        raise ValueError("Use distinct, nonempty comma-separated labels.")
    return frozenset(values)


def _fmt(values):
    return "∅" if not values else "{" + ", ".join(sorted(values)) + "}"


def check_finite_topology_example(universe_text, topology_text, subset_text=""):
    """Input X as a,b,c; τ as ∅;X;a;b;a,b; and A as a,b."""
    try:
        universe = _labels(universe_text, False)
        if len(universe) > 10:
            raise ValueError("Use at most 10 points in this checker.")
        raw = [member.strip() for member in topology_text.split(";")]
        if not topology_text.strip() or any(not item for item in raw):
            raise ValueError("Separate topology members with semicolons.")
        family = []
        for item in raw:
            if item in {"∅", "{}", "empty"}:
                family.append(frozenset())
            elif item == "X":
                family.append(universe)
            else:
                member = _labels(item)
                if not member <= universe:
                    raise ValueError("A topology member contains points outside X.")
                family.append(member)
        space = FiniteTopologicalSpace(universe, family)
        check = space.validate()
        if not check.is_topology:
            return {"valid": False, "isTopology": False,
                    "message": "This family is not a topology.",
                    "errors": list(check.errors)}
        subset = _labels(subset_text)
        if not subset <= universe:
            raise ValueError("A must be a subset of X.")
        inside, closed = interior(space, subset), closure(space, subset)
        return {"valid": True, "isTopology": True,
            "message": "The entered family satisfies the topology axioms.",
            "openSets": sorted(_fmt(s) for s in space.open_sets),
            "closedSets": sorted(_fmt(s) for s in closed_sets(space)),
            "interior": _fmt(inside), "closure": _fmt(closed),
            "boundary": _fmt(boundary(space, subset)),
            "accumulationPoints": _fmt(accumulation_points(space, subset)),
            "isolatedPoints": _fmt(isolated_points(space, subset)),
            "hausdorff": is_hausdorff(space)}
    except ValueError as error:
        return {"valid": False, "isTopology": False,
                "message": str(error), "errors": [str(error)]}
