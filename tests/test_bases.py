
import pytest

from topolab.core.bases import (
    is_basis,
    generate_topology,
    finite_intersections,
    generate_topology_from_subbasis,
)


def test_valid_basis():
    X = frozenset({"1", "2", "3"})
    B = [
        {"1", "2"},
        {"2", "3"},
        {"2"},
    ]

    assert is_basis(X, B)


def test_invalid_basis_does_not_cover_universe():
    X = frozenset({"1", "2", "3"})
    B = [{"1"}, {"2"}]

    assert not is_basis(X, B)


def test_invalid_basis_intersection_condition():
    X = frozenset({"1", "2", "3"})
    B = [
        {"1", "2"},
        {"2", "3"},
    ]

    assert not is_basis(X, B)


def test_generate_topology():
    X = frozenset({"1", "2", "3"})
    B = [
        {"1", "2"},
        {"2", "3"},
        {"2"},
    ]

    expected = {
        frozenset(),
        frozenset({"2"}),
        frozenset({"1", "2"}),
        frozenset({"2", "3"}),
        X,
    }

    assert generate_topology(X, B) == expected


def test_finite_intersections():
    X = frozenset({"1", "2", "3"})
    S = [
        {"1", "2"},
        {"2", "3"},
    ]

    expected = {
        X,
        frozenset({"1", "2"}),
        frozenset({"2", "3"}),
        frozenset({"2"}),
    }

    assert finite_intersections(X, S) == expected


def test_generate_topology_from_subbasis():
    X = frozenset({"1", "2", "3"})
    S = [
        {"1", "2"},
        {"2", "3"},
    ]

    expected = {
        frozenset(),
        frozenset({"2"}),
        frozenset({"1", "2"}),
        frozenset({"2", "3"}),
        X,
    }

    assert generate_topology_from_subbasis(X, S) == expected


def test_invalid_basis_raises_error():
    X = frozenset({"1", "2", "3"})
    B = [{"1"}, {"2"}]

    with pytest.raises(ValueError):
        generate_topology(X, B)


def test_invalid_family_element_raises_error():
    X = frozenset({"1", "2"})
    B = [{"1", "3"}]

    with pytest.raises(ValueError):
        is_basis(X, B)
