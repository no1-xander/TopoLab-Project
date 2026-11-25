
"""Finite topological spaces and topology validation."""

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


FiniteSet = frozenset[str]


@dataclass(frozen=True)
class TopologyValidation:
    """Result of validating a proposed topology."""

    is_topology: bool
    errors: tuple[str, ...]
    open_set_count: int
    union_checks: int
    intersection_checks: int


class FiniteTopologicalSpace:
    """Represent a finite set and a proposed family of open sets."""

    def __init__(
        self,
        elements: Iterable[str],
        open_sets: Iterable[Iterable[str]],
    ) -> None:
        self.universe: FiniteSet = frozenset(elements)
        self.open_sets: frozenset[FiniteSet] = frozenset(
            frozenset(subset) for subset in open_sets
        )

    def validate(self) -> TopologyValidation:
        """Check whether the proposed family is a topology on X."""

        errors: list[str] = []
        union_checks = 0
        intersection_checks = 0

        # Every proposed open set must be a subset of X.
        for subset in self.open_sets:
            if not subset.issubset(self.universe):
                outside = subset - self.universe
                errors.append(
                    f"{self._format_set(subset)} contains elements "
                    f"outside X: {self._format_set(outside)}."
                )

        # First axiom: the empty set and X must belong to the family.
        if frozenset() not in self.open_sets:
            errors.append("The empty set is missing from the topology.")

        if self.universe not in self.open_sets:
            errors.append("The whole set X is missing from the topology.")

        # Second and third axioms:
        # Check closure under pairwise unions and intersections.
        for first, second in combinations(self.open_sets, 2):
            union = first | second
            intersection = first & second

            union_checks += 1
            if union not in self.open_sets:
                errors.append(
                    f"Not closed under unions: "
                    f"{self._format_set(first)} ∪ "
                    f"{self._format_set(second)} = "
                    f"{self._format_set(union)}, which is missing."
                )

            intersection_checks += 1
            if intersection not in self.open_sets:
                errors.append(
                    f"Not closed under intersections: "
                    f"{self._format_set(first)} ∩ "
                    f"{self._format_set(second)} = "
                    f"{self._format_set(intersection)}, which is missing."
                )

        return TopologyValidation(
            is_topology=not errors,
            errors=tuple(errors),
            open_set_count=len(self.open_sets),
            union_checks=union_checks,
            intersection_checks=intersection_checks,
        )

    @staticmethod
    def _format_set(subset: FiniteSet) -> str:
        """Format a finite set consistently for readable diagnostics."""
        if not subset:
            return "∅"

        elements = ", ".join(sorted(subset))
        return "{" + elements + "}"
