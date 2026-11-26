
import pytest

from topolab.core.finite_spaces import FiniteTopologicalSpace
from topolab.core.operators import (
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


@pytest.fixture
def example_space():
    """A finite topological space from our course examples."""
    X = {"a", "b", "c"}
    tau = [
        set(),
        {"a"},
        {"a", "b"},
        X,
    ]
    return FiniteTopologicalSpace(X, tau)


def test_complement(example_space):
    assert complement(example_space, frozenset({"a"})) == frozenset({"b", "c"})


def test_open_and_closed_classification(example_space):
    assert is_open(example_space, frozenset({"a"}))
    assert not is_closed(example_space, frozenset({"a"}))

    assert is_closed(example_space, frozenset({"b", "c"}))
    assert not is_open(example_space, frozenset({"b", "c"}))


def test_clopen_sets(example_space):
    assert is_clopen(example_space, frozenset())
    assert is_clopen(example_space, frozenset({"a", "b", "c"}))
    assert not is_clopen(example_space, frozenset({"a"}))


def test_closed_sets(example_space):
    expected = {
        frozenset(),
        frozenset({"c"}),
        frozenset({"b", "c"}),
        frozenset({"a", "b", "c"}),
    }
    assert closed_sets(example_space) == expected


def test_neighborhoods(example_space):
    expected = {
        frozenset({"a", "b"}),
        frozenset({"a", "b", "c"}),
    }
    assert neighborhoods(example_space, "b") == expected


def test_accumulation_points(example_space):
    assert accumulation_points(
        example_space, frozenset({"b"})
    ) == frozenset({"c"})


def test_isolated_points(example_space):
    assert isolated_points(
        example_space, frozenset({"b", "c"})
    ) == frozenset({"b"})


def test_discrete_space_is_hausdorff():
    X = {"a", "b", "c"}
    tau = [
        frozenset(subset)
        for subset in [
            set(),
            {"a"}, {"b"}, {"c"},
            {"a", "b"}, {"a", "c"}, {"b", "c"},
            X,
        ]
    ]
    space = FiniteTopologicalSpace(X, tau)

    assert is_hausdorff(space)


def test_indiscrete_space_is_not_hausdorff():
    X = {"a", "b"}
    tau = [set(), X]
    space = FiniteTopologicalSpace(X, tau)

    assert not is_hausdorff(space)


def test_hausdorff_separation_in_discrete_space():
    X = {"a", "b"}
    tau = [set(), {"a"}, {"b"}, X]
    space = FiniteTopologicalSpace(X, tau)

    result = hausdorff_separation(space, "a", "b")

    assert result is not None
    first, second = result
    assert "a" in first
    assert "b" in second
    assert first.isdisjoint(second)


def test_invalid_point_raises_error(example_space):
    with pytest.raises(ValueError):
        neighborhoods(example_space, "z")

    with pytest.raises(ValueError):
        accumulation_points(example_space, frozenset({"z"}))
