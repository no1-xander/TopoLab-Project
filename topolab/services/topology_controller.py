
"""Bridge between the TopoLab mathematical engine and QML."""

from __future__ import annotations

import re

from PySide6.QtCore import QObject, Slot

from topolab.core.finite_spaces import FiniteTopologicalSpace
from itertools import combinations

from topolab.core.operators import (
    interior,
    closure,
    boundary,
    complement,
    is_open,
    is_closed,
    is_clopen,
    closed_sets,
    neighborhoods,
    accumulation_points,
    isolated_points,
    hausdorff_separation,
    is_hausdorff,
)


class TopologyController(QObject):
    """Parse mathematical input and expose topology operations to QML."""

    @staticmethod
    def _parse_elements(text: str) -> frozenset[str]:
        """Parse a universe such as a, b, c or {a,b,c}."""
        source = text.strip()

        if source.startswith("{") and source.endswith("}"):
            source = source[1:-1].strip()

        if not source:
            return frozenset()

        elements = [item.strip() for item in source.split(",")]

        if any(not item for item in elements):
            raise ValueError("Check the elements of X. An element is missing.")

        for item in elements:
            if not re.fullmatch(r"[A-Za-z0-9_]+", item):
                raise ValueError(f"Invalid element: {item}")

        if len(elements) != len(set(elements)):
            raise ValueError("The universe contains duplicate elements.")

        return frozenset(elements)

    @staticmethod
    def _parse_subset(
        text: str,
        universe: frozenset[str],
    ) -> frozenset[str]:
        """Parse a subset such as {a,b}, ∅, or X."""
        source = text.strip()

        if source in ("∅", "{}"):
            return frozenset()

        if source == "X":
            return universe

        if source.startswith("{") and source.endswith("}"):
            source = source[1:-1].strip()

        if not source:
            return frozenset()

        elements = [item.strip() for item in source.split(",")]

        if any(not item for item in elements):
            raise ValueError("Check the subset notation. An element is missing.")

        for item in elements:
            if not re.fullmatch(r"[A-Za-z0-9_]+", item):
                raise ValueError(f"Invalid element in subset: {item}")

        if len(elements) != len(set(elements)):
            raise ValueError("The subset contains duplicate elements.")

        result = frozenset(elements)

        if not result.issubset(universe):
            outside = result - universe
            raise ValueError(
                f"These elements are outside X: {', '.join(sorted(outside))}"
            )

        return result

    @classmethod
    def _parse_topology(
        cls,
        text: str,
        universe: frozenset[str],
    ) -> list[frozenset[str]]:
        """Read one open-set candidate per line."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if not lines:
            raise ValueError("Enter at least one proposed open set.")

        return [cls._parse_subset(line, universe) for line in lines]

    @staticmethod
    def _format_set(subset: frozenset[str]) -> str:
        """Format a set for display."""
        if not subset:
            return "∅"

        return "{" + ", ".join(sorted(subset)) + "}"

    @Slot(str, str, result="QVariantMap")
    def validateTopology(
        self,
        universe_text: str,
        topology_text: str,
    ) -> dict:
        """Validate a proposed topology and return a QML-friendly result."""
        try:
            universe = self._parse_elements(universe_text)
            open_sets = self._parse_topology(topology_text, universe)

            space = FiniteTopologicalSpace(universe, open_sets)
            validation = space.validate()

            return {
                "ok": True,
                "isTopology": validation.is_topology,
                "openSetCount": validation.open_set_count,
                "unionChecks": validation.union_checks,
                "intersectionChecks": validation.intersection_checks,
                "errors": list(validation.errors),
                "message": (
                    "The proposed family is a valid topology."
                    if validation.is_topology
                    else "The proposed family is not a topology."
                ),
            }

        except ValueError as error:
            return {
                "ok": False,
                "isTopology": False,
                "openSetCount": 0,
                "unionChecks": 0,
                "intersectionChecks": 0,
                "errors": [str(error)],
                "message": "Please check your mathematical input.",
            }

    @Slot(str, str, str, result="QVariantMap")
    def analyzeSubset(
        self,
        universe_text: str,
        topology_text: str,
        subset_text: str,
    ) -> dict:
        """Calculate the interior, closure, and boundary of A."""
        try:
            universe = self._parse_elements(universe_text)
            open_sets = self._parse_topology(topology_text, universe)

            space = FiniteTopologicalSpace(universe, open_sets)
            validation = space.validate()

            if not validation.is_topology:
                return {
                    "ok": False,
                    "errors": list(validation.errors),
                    "message": "Validate the topology before analyzing a subset.",
                }

            subset = self._parse_subset(subset_text, universe)

            return {
                "ok": True,
                "subset": self._format_set(subset),

                "interior": self._format_set(
                    interior(space, subset)
                ),
                "closure": self._format_set(
                    closure(space, subset)
                ),
                "boundary": self._format_set(
                    boundary(space, subset)
                ),
                "complement": self._format_set(
                    complement(space, subset)
                ),

                "isOpen": is_open(space, subset),
                "isClosed": is_closed(space, subset),
                "isClopen": is_clopen(space, subset),

                "accumulationPoints": self._format_set(
                    accumulation_points(space, subset)
                ),
                "isolatedPoints": self._format_set(
                    isolated_points(space, subset)
                ),

                "closedSets": [
                    self._format_set(item)
                    for item in sorted(
                        closed_sets(space),
                        key=lambda item: (len(item), tuple(sorted(item)))
                    )
                ],

                "message": "Subset analysis completed.",
                "errors": [],
            }

        except ValueError as error:
            return {
                "ok": False,
                "errors": [str(error)],
                "message": "Please check your mathematical input.",
            }

    @Slot(str, str, str, result="QVariantMap")
    def analyzePoint(
        self,
        universe_text: str,
        topology_text: str,
        point_text: str
    ) -> dict:
        try:
            universe = self._parse_elements(universe_text)
            open_sets = self._parse_topology(topology_text, universe)

            space = FiniteTopologicalSpace(universe, open_sets)
            validation = space.validate()

            if not validation.is_topology:
                raise ValueError(
                    "The proposed family is not a valid topology."
                )

            point_set = self._parse_subset(point_text, universe)

            if len(point_set) != 1:
                raise ValueError(
                    "Enter exactly one point, for example: a"
                )

            point = next(iter(point_set))

            result = neighborhoods(space, point)

            return {
                "ok": True,
                "point": point,
                "neighborhoods": [
                    self._format_set(item)
                    for item in sorted(
                        result,
                        key=lambda item: (len(item), tuple(sorted(item)))
                    )
                ],
                "message": "Neighborhood analysis completed.",
                "errors": [],
            }

        except ValueError as error:
            return {
                "ok": False,
                "neighborhoods": [],
                "errors": [str(error)],
                "message": "Please check your mathematical input.",
            }

    @Slot(str, str, result="QVariantMap")
    def analyzeHausdorff(
        self,
        universe_text: str,
        topology_text: str
    ) -> dict:
        try:
            universe = self._parse_elements(universe_text)
            open_sets = self._parse_topology(topology_text, universe)

            space = FiniteTopologicalSpace(universe, open_sets)
            validation = space.validate()

            if not validation.is_topology:
                raise ValueError(
                    "The proposed family is not a valid topology."
                )

            separations = []
            inseparable_pairs = []

            for first, second in combinations(
                sorted(universe), 2
            ):
                result = hausdorff_separation(
                    space, first, second
                )

                if result is None:
                    inseparable_pairs.append(
                        f"({first}, {second})"
                    )
                else:
                    first_open, second_open = result

                    separations.append({
                        "firstPoint": first,
                        "secondPoint": second,
                        "firstNeighborhood": self._format_set(
                            first_open
                        ),
                        "secondNeighborhood": self._format_set(
                            second_open
                        ),
                    })

            return {
                "ok": True,
                "isHausdorff": is_hausdorff(space),
                "separations": separations,
                "inseparablePairs": inseparable_pairs,
                "message": (
                    "The space is Hausdorff."
                    if is_hausdorff(space)
                    else "The space is not Hausdorff."
                ),
                "errors": [],
            }

        except ValueError as error:
            return {
                "ok": False,
                "isHausdorff": False,
                "separations": [],
                "inseparablePairs": [],
                "errors": [str(error)],
                "message": "Please check your mathematical input.",
            }