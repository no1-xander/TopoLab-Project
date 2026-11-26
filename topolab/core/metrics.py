"""Finite metric spaces and their induced metric topologies.

This module is intentionally finite and explicit: every ordered pair must have
a supplied distance. It does not attempt to represent arbitrary or infinite
metric spaces.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import isclose, isfinite
from numbers import Real
from typing import Hashable, Mapping, TypeVar

T = TypeVar("T", bound=Hashable)
DistanceTable = Mapping[tuple[T, T], Real]
FiniteSet = frozenset[T]


@dataclass(frozen=True)
class MetricValidation:
    """Detailed result of checking the three metric axioms."""

    is_metric: bool
    errors: tuple[str, ...]
    separation_checks: int
    symmetry_checks: int
    triangle_checks: int


class FiniteMetricSpace:
    """A finite set equipped with an explicitly supplied distance table."""

    def __init__(self, points, distances: DistanceTable[T]) -> None:
        self.points: FiniteSet[T] = frozenset(points)
        self.distances: dict[tuple[T, T], Real] = dict(distances)

    def validate(self) -> MetricValidation:
        """Check M1 (separation), M2 (symmetry), and M3 (triangle inequality)."""
        errors: list[str] = []
        separation_checks = symmetry_checks = triangle_checks = 0
        expected = {(x, y) for x in self.points for y in self.points}
        actual = set(self.distances)

        missing = expected - actual
        extra = actual - expected
        if missing:
            preview = ", ".join(
                f"({x}, {y})" for x, y in sorted(missing, key=repr)[:8]
            )
            errors.append(f"Distance table is incomplete; missing pairs: {preview}.")
        if extra:
            preview = ", ".join(repr(pair) for pair in sorted(extra, key=repr)[:8])
            errors.append(f"Distance table contains pairs outside X: {preview}.")

        invalid_values = []
        for pair, value in self.distances.items():
            if (
                not isinstance(value, Real)
                or isinstance(value, bool)
                or not isfinite(float(value))
                or value < 0
            ):
                invalid_values.append(pair)
        if invalid_values:
            errors.append(
                "Every distance must be a finite, nonnegative real number; "
                f"invalid entries: {', '.join(map(repr, invalid_values[:8]))}."
            )

        if missing or extra or invalid_values:
            return MetricValidation(
                False, tuple(errors), separation_checks,
                symmetry_checks, triangle_checks
            )

        points = tuple(self.points)
        for x in points:
            for y in points:
                separation_checks += 1
                value = self.distances[(x, y)]
                if (value == 0) != (x == y):
                    errors.append(
                        f"M1 fails for ({x}, {y}): d({x}, {y}) = {value}."
                    )

        for x, y in combinations(points, 2):
            symmetry_checks += 1
            first = self.distances[(x, y)]
            reverse = self.distances[(y, x)]
            if first != reverse:
                errors.append(
                    f"M2 fails for ({x}, {y}): d({x}, {y}) = {first} "
                    f"but d({y}, {x}) = {reverse}."
                )

        for x in points:
            for y in points:
                for z in points:
                    triangle_checks += 1
                    direct = float(self.distances[(x, z)])
                    via = float(self.distances[(x, y)]) + float(self.distances[(y, z)])
                    if direct > via and not isclose(
                        direct, via, rel_tol=1e-12, abs_tol=1e-12
                    ):
                        errors.append(
                            f"M3 fails for ({x}, {y}, {z}): "
                            f"d({x}, {z}) = {direct} > "
                            f"d({x}, {y}) + d({y}, {z}) = {via}."
                        )

        return MetricValidation(
            not errors, tuple(errors),
            separation_checks, symmetry_checks, triangle_checks
        )

    def _require_metric(self) -> None:
        validation = self.validate()
        if not validation.is_metric:
            raise ValueError(
                "The distance table does not define a metric: "
                + " ".join(validation.errors)
            )

    def distance(self, first: T, second: T) -> Real:
        """Return d(first, second) after validating the metric."""
        self._require_metric()
        if first not in self.points or second not in self.points:
            raise ValueError("Both points must belong to X.")
        return self.distances[(first, second)]

    def open_ball(self, center: T, radius: Real) -> FiniteSet[T]:
        """Return B_d(center, radius) = {y : d(center, y) < radius}."""
        self._require_metric()
        if center not in self.points:
            raise ValueError("The ball centre must belong to X.")
        if not isinstance(radius, Real) or isinstance(radius, bool):
            raise ValueError("The radius must be a positive real number.")
        if not isfinite(float(radius)) or radius <= 0:
            raise ValueError("The radius must be a positive finite real number.")
        return frozenset(
            point for point in self.points
            if self.distances[(center, point)] < radius
        )

    def closed_ball(self, center: T, radius: Real) -> FiniteSet[T]:
        """Return the closed ball {y : d(center, y) <= radius}."""
        self._require_metric()
        if center not in self.points:
            raise ValueError("The ball centre must belong to X.")
        if not isinstance(radius, Real) or isinstance(radius, bool):
            raise ValueError("The radius must be a positive real number.")
        if not isfinite(float(radius)) or radius <= 0:
            raise ValueError("The radius must be a positive finite real number.")
        return frozenset(
            point for point in self.points
            if self.distances[(center, point)] <= radius
        )

    def metric_topology(self) -> frozenset[FiniteSet[T]]:
        """Return the topology induced on this finite metric space.

        Every finite metric space is discrete: for each point, a sufficiently
        small positive ball contains only that point. Therefore every subset
        is open and the induced topology is P(X).
        """
        self._require_metric()
        points = tuple(self.points)
        return frozenset(
            frozenset(subset)
            for size in range(len(points) + 1)
            for subset in combinations(points, size)
        )

    def epsilon_net(self, epsilon: Real) -> FiniteSet[T]:
        """Construct a finite epsilon-net using open balls of radius epsilon."""
        self._require_metric()
        if not isinstance(epsilon, Real) or isinstance(epsilon, bool):
            raise ValueError("Epsilon must be a positive real number.")
        if not isfinite(float(epsilon)) or epsilon <= 0:
            raise ValueError("Epsilon must be a positive finite real number.")

        uncovered = set(self.points)
        centers: list[T] = []
        while uncovered:
            center = next(iter(uncovered))
            centers.append(center)
            covered = {
                point for point in uncovered
                if self.distances[(center, point)] < epsilon
            }
            uncovered.difference_update(covered)
        return frozenset(centers)

    def is_totally_bounded_at(self, epsilon: Real) -> bool:
        """Check whether the constructed finite epsilon-net covers X."""
        centers = self.epsilon_net(epsilon)
        covered = frozenset().union(
            *(self.open_ball(center, epsilon) for center in centers)
        ) if centers else frozenset()
        return covered == self.points
