"""QML controller for finite metric-space calculations."""
from __future__ import annotations

import math
import re

from PySide6.QtCore import QObject, Slot

from topolab.core.metrics import FiniteMetricSpace


class MetricController(QObject):
    """Parse a finite distance table and expose metric operations to QML."""

    @staticmethod
    def _parse_points(text: str) -> frozenset[str]:
        source = text.strip()
        if source.startswith("{") and source.endswith("}"):
            source = source[1:-1].strip()
        if not source:
            raise ValueError("Enter a nonempty underlying set X.")
        values = [item.strip() for item in source.split(",")]
        if any(not item for item in values):
            raise ValueError("An element of X is missing.")
        invalid = [item for item in values
                   if re.fullmatch(r"[A-Za-z0-9_]+", item) is None]
        if invalid:
            raise ValueError(
                f"Invalid point label {invalid[0]!r}; use letters, digits, or underscores."
            )
        if len(values) != len(set(values)):
            raise ValueError("The underlying set contains duplicate points.")
        if len(values) > 10:
            raise ValueError("This interactive finite metric workspace is limited to 10 points.")
        return frozenset(values)

    @staticmethod
    def _parse_distances(text: str, points: frozenset[str]) -> dict:
        distances = {}
        for line_number, line in enumerate(text.splitlines(), start=1):
            source = line.strip()
            if not source:
                continue
            parts = [part.strip() for part in source.split(",")]
            if len(parts) != 3:
                raise ValueError(
                    f"Line {line_number}: use the format point, point, distance."
                )
            first, second, raw_value = parts
            if first not in points or second not in points:
                raise ValueError(
                    f"Line {line_number}: both points must belong to X."
                )
            pair = (first, second)
            if pair in distances:
                raise ValueError(
                    f"Line {line_number}: distance d({first}, {second}) is repeated."
                )
            try:
                value = float(raw_value)
            except ValueError as error:
                raise ValueError(
                    f"Line {line_number}: distance must be a real number."
                ) from error
            if not math.isfinite(value):
                raise ValueError(
                    f"Line {line_number}: distance must be finite."
                )
            distances[pair] = value
        return distances

    @staticmethod
    def _format_set(values) -> str:
        ordered = sorted(values)
        return "∅" if not ordered else "{" + ", ".join(ordered) + "}"

    @classmethod
    def _format_topology(cls, topology) -> list[str]:
        return [
            cls._format_set(item)
            for item in sorted(topology, key=lambda item: (len(item), tuple(sorted(item))))
        ]

    @Slot(str, str, str, str, result="QVariantMap")
    def analyzeMetric(
        self,
        points_text: str,
        distance_table_text: str,
        center_text: str,
        radius_text: str,
    ) -> dict:
        """Validate M1-M3 and calculate the requested balls and topology."""
        try:
            points = self._parse_points(points_text)
            distances = self._parse_distances(distance_table_text, points)
            space = FiniteMetricSpace(points, distances)
            validation = space.validate()

            if not validation.is_metric:
                return {
                    "ok": False,
                    "isMetric": False,
                    "errors": list(validation.errors),
                    "openBall": "",
                    "closedBall": "",
                    "metricTopology": [],
                    "message": "The supplied distance table does not define a metric.",
                    "separationChecks": validation.separation_checks,
                    "symmetryChecks": validation.symmetry_checks,
                    "triangleChecks": validation.triangle_checks,
                }

            center = center_text.strip()
            if center not in points:
                raise ValueError("The selected ball centre must belong to X.")
            try:
                radius = float(radius_text)
            except ValueError as error:
                raise ValueError("Enter a valid positive radius.") from error
            if not math.isfinite(radius) or radius <= 0:
                raise ValueError("The radius must be a positive finite real number.")

            open_ball = space.open_ball(center, radius)
            closed_ball = space.closed_ball(center, radius)
            topology = space.metric_topology()

            return {
                "ok": True,
                "isMetric": True,
                "errors": [],
                "message": "M1, M2, and M3 are satisfied. This is a metric space.",
                "openBall": self._format_set(open_ball),
                "closedBall": self._format_set(closed_ball),
                "metricTopology": self._format_topology(topology),
                "isDiscrete": len(topology) == 2 ** len(points),
                "separationChecks": validation.separation_checks,
                "symmetryChecks": validation.symmetry_checks,
                "triangleChecks": validation.triangle_checks,
                "epsilonNetNote": (
                    "Every finite metric space is totally bounded: for any ε > 0, "
                    "the finite set X itself is an ε-net."
                ),
            }
        except ValueError as error:
            return {
                "ok": False,
                "isMetric": False,
                "errors": [str(error)],
                "message": "Please check the metric input.",
                "openBall": "",
                "closedBall": "",
                "metricTopology": [],
            }
