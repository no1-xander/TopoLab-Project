"""QML controller for finite set operations in the Set Toolkit."""
from __future__ import annotations
import re
from PySide6.QtCore import QObject, Slot
from topolab.core.sets import (
    are_disjoint, are_equal, cartesian_product, complement, difference,
    intersection, is_subset, power_set, union,
)


class SetController(QObject):
    """Parse finite-set input and expose Chapter 1 operations to QML.

    Accepted input is comma-separated labels (a, b, c) or braced labels.
    Labels contain letters, digits, and underscores; intervals and infinite
    sets are deliberately outside this finite input grammar.
    """
    POWER_SET_LIMIT = 8
    CARTESIAN_PRODUCT_LIMIT = 100
    _OPERATIONS = {
        0: "union", 1: "intersection", 2: "difference",
        3: "complement", 4: "power_set", 5: "cartesian_product",
        6: "subset", 7: "equality", 8: "disjoint",
    }

    @staticmethod
    def _parse_set(text: str, field_name: str) -> frozenset[str]:
        source = text.strip()
        if source in ("", "∅", "{}"):
            return frozenset()
        if source.startswith("{") and source.endswith("}"):
            source = source[1:-1].strip()
        elif source.startswith("{") or source.endswith("}"):
            raise ValueError(
                f"{field_name}: use balanced braces, for example {{a, b}}."
            )
        if not source:
            return frozenset()
        elements = [item.strip() for item in source.split(",")]
        if any(not item for item in elements):
            raise ValueError(f"{field_name}: an element is missing.")
        invalid = [
            item for item in elements
            if re.fullmatch(r"[A-Za-z0-9_]+", item) is None
        ]
        if invalid:
            raise ValueError(
                f"{field_name}: invalid element label {invalid[0]!r}. "
                "Use letters, numbers, or underscores."
            )
        if len(elements) != len(set(elements)):
            raise ValueError(f"{field_name}: duplicate elements are not allowed.")
        return frozenset(elements)

    @staticmethod
    def _format_set(elements) -> str:
        values = sorted(elements)
        return "∅" if not values else "{" + ", ".join(values) + "}"

    @classmethod
    def _format_power_set(cls, family) -> str:
        ordered = sorted(family, key=lambda item: (len(item), tuple(sorted(item))))
        return "{\n  " + ",\n  ".join(
            cls._format_set(item) for item in ordered
        ) + "\n}"

    @staticmethod
    def _format_product(product) -> str:
        ordered = sorted(product)
        if not ordered:
            return "∅"
        return "{\n  " + ",\n  ".join(
            f"({first}, {second})" for first, second in ordered
        ) + "\n}"

    @Slot(int, str, str, str, result="QVariantMap")
    def calculate(self, operation_index: int, first_text: str,
                  second_text: str, universe_text: str) -> dict:
        """Calculate the selected operation and return a QML-friendly map."""
        operation = self._OPERATIONS.get(operation_index)
        if operation is None:
            return {
                "ok": False, "result": "", "formula": "",
                "message": "Select a valid set operation.", "explanation": "",
            }
        try:
            first = self._parse_set(first_text, "Set A")
            if operation == "complement":
                universe = self._parse_set(universe_text, "Universe E")
                value = complement(first, universe)
                result_text = f"E \\ A = {self._format_set(value)}"
                formula = "E \\ A"
                explanation = (
                    "The complement is relative to the stated universe E. "
                    "The controller verifies that A is a subset of E."
                )
            elif operation == "power_set":
                if len(first) > self.POWER_SET_LIMIT:
                    raise ValueError(
                        f"The power set is limited to {self.POWER_SET_LIMIT} "
                        "elements in this interactive view (2^n subsets)."
                    )
                value = power_set(first)
                result_text = f"P(A) = {self._format_power_set(value)}"
                formula = "P(A)"
                explanation = (
                    f"The power set contains {len(value)} subsets, "
                    f"including ∅ and A (2^{len(first)} = {len(value)})."
                )
            else:
                second = self._parse_set(second_text, "Set B")
                if operation == "union":
                    value = union(first, second)
                    formula = "A \\cup B"
                    result_text = f"A ∪ B = {self._format_set(value)}"
                    explanation = "Elements that belong to A or to B (or to both)."
                elif operation == "intersection":
                    value = intersection(first, second)
                    formula = "A \\cap B"
                    result_text = f"A ∩ B = {self._format_set(value)}"
                    explanation = "Elements that belong to both A and B."
                elif operation == "difference":
                    value = difference(first, second)
                    formula = "A \\setminus B"
                    result_text = f"A \\ B = {self._format_set(value)}"
                    explanation = "Elements of A that do not belong to B."
                elif operation == "cartesian_product":
                    if len(first) * len(second) > self.CARTESIAN_PRODUCT_LIMIT:
                        raise ValueError(
                            "The Cartesian product is limited to 100 ordered "
                            "pairs in this interactive view."
                        )
                    value = cartesian_product(first, second)
                    formula = "A \\times B"
                    result_text = f"A × B = {self._format_product(value)}"
                    explanation = (
                        "The first coordinate comes from A and the second "
                        "coordinate comes from B; order matters."
                    )
                elif operation == "subset":
                    value = is_subset(first, second)
                    formula = "A \\subseteq B"
                    result_text = f"A ⊆ B: {value}"
                    explanation = "True exactly when every element of A belongs to B."
                elif operation == "equality":
                    value = are_equal(first, second)
                    formula = "A = B"
                    result_text = f"A = B: {value}"
                    explanation = "Two sets are equal when they have exactly the same elements."
                elif operation == "disjoint":
                    value = are_disjoint(first, second)
                    formula = "A \\cap B = \\varnothing"
                    result_text = f"A and B are disjoint: {value}"
                    explanation = "The sets are disjoint exactly when their intersection is empty."
                else:
                    raise ValueError("This operation is not implemented.")
            return {
                "ok": True, "result": result_text, "formula": formula,
                "message": "Calculation completed.", "explanation": explanation,
            }
        except ValueError as error:
            return {
                "ok": False, "result": "", "formula": "",
                "message": str(error), "explanation": "",
            }
