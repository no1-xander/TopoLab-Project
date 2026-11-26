
"""Controller for basis and subbasis analysis."""

import re

from PySide6.QtCore import QObject, Slot

from topolab.core.bases import (
    is_basis,
    generate_topology,
    finite_intersections,
    generate_topology_from_subbasis,
)


class BasisController(QObject):
    """Expose basis and subbasis operations to the QML interface."""

    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def _parse_elements(text: str) -> frozenset[str]:
        """Parse the underlying set X."""
        cleaned = text.strip()

        if cleaned.startswith("{") and cleaned.endswith("}"):
            cleaned = cleaned[1:-1].strip()

        if not cleaned:
            raise ValueError("The underlying set X cannot be empty.")

        elements = [item.strip() for item in cleaned.split(",")]

        if any(not item for item in elements):
            raise ValueError("Empty elements are not allowed.")

        if any(not re.fullmatch(r"[A-Za-z0-9_]+", item) for item in elements):
            raise ValueError(
                "Elements must contain only letters, numbers, or underscores."
            )

        if len(elements) != len(set(elements)):
            raise ValueError("The underlying set contains duplicate elements.")

        return frozenset(elements)

    @staticmethod
    def _parse_family(text: str, universe: frozenset[str]):
        """Parse a family of subsets, one subset per line."""
        family = []

        for line_number, line in enumerate(text.splitlines(), start=1):
            cleaned = line.strip()

            if not cleaned:
                continue

            if cleaned in ("∅", "{}"):
                subset = frozenset()
            elif cleaned == "X":
                subset = universe
            else:
                if cleaned.startswith("{") and cleaned.endswith("}"):
                    cleaned = cleaned[1:-1].strip()

                if not cleaned:
                    subset = frozenset()
                else:
                    elements = [item.strip() for item in cleaned.split(",")]

                    if any(not item for item in elements):
                        raise ValueError(
                            f"Line {line_number}: empty elements are not allowed."
                        )

                    if len(elements) != len(set(elements)):
                        raise ValueError(
                            f"Line {line_number}: duplicate elements were found."
                        )

                    subset = frozenset(elements)

            outside = subset - universe
            if outside:
                raise ValueError(
                    f"Line {line_number}: {', '.join(sorted(outside))} "
                    "does not belong to X."
                )

            family.append(subset)

        if not family:
            raise ValueError("Enter at least one subset.")

        if len(family) != len(set(family)):
            raise ValueError("The family contains duplicate subsets.")

        return frozenset(family)

    @staticmethod
    def _format_set(subset):
        if not subset:
            return "∅"
        return "{" + ", ".join(sorted(subset)) + "}"

    @classmethod
    def _format_family(cls, family):
        ordered = sorted(
            family,
            key=lambda subset: (len(subset), tuple(sorted(subset)))
        )
        return [cls._format_set(subset) for subset in ordered]

    @Slot(str, str, result="QVariant")
    def analyzeBasis(self, universe_text, family_text):
        """Check a basis and generate its topology."""
        try:
            universe = self._parse_elements(universe_text)
            family = self._parse_family(family_text, universe)

            valid = is_basis(universe, family)

            result = {
                "ok": True,
                "isBasis": valid,
                "family": self._format_family(family),
                "message": "",
                "generatedTopology": [],
                "errors": [],
            }

            if valid:
                topology = generate_topology(universe, family)
                result["generatedTopology"] = self._format_family(topology)
                result["message"] = (
                    "The family is a basis. Its generated topology "
                    "has been calculated."
                )
            else:
                result["message"] = (
                    "The family is not a basis. Check the covering "
                    "and intersection conditions."
                )

            return result

        except ValueError as error:
            return {
                "ok": False,
                "isBasis": False,
                "family": [],
                "message": str(error),
                "generatedTopology": [],
                "errors": [str(error)],
            }

    @Slot(str, str, result="QVariant")
    def analyzeSubbasis(self, universe_text, family_text):
        """Generate the topology induced by a subbasis."""
        try:
            universe = self._parse_elements(universe_text)
            family = self._parse_family(family_text, universe)

            intersections = finite_intersections(universe, family)
            topology = generate_topology_from_subbasis(universe, family)

            return {
                "ok": True,
                "finiteIntersections": self._format_family(intersections),
                "generatedTopology": self._format_family(topology),
                "message": (
                    "The finite intersections and generated topology "
                    "have been calculated successfully."
                ),
                "errors": [],
            }

        except ValueError as error:
            return {
                "ok": False,
                "finiteIntersections": [],
                "generatedTopology": [],
                "message": str(error),
                "errors": [str(error)],
            }
