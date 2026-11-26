import pytest

from topolab.core.metrics import FiniteMetricSpace


def discrete_space():
    points = {"a", "b", "c"}
    distances = {
        (x, y): (0 if x == y else 1)
        for x in points for y in points
    }
    return FiniteMetricSpace(points, distances)


def test_discrete_metric_is_valid():
    result = discrete_space().validate()
    assert result.is_metric
    assert result.separation_checks == 9
    assert result.symmetry_checks == 3
    assert result.triangle_checks == 27


def test_path_metric_is_valid():
    points = {0, 1, 2}
    distances = {
        (x, y): abs(x - y)
        for x in points for y in points
    }
    assert FiniteMetricSpace(points, distances).validate().is_metric


def test_missing_ordered_pair_is_rejected():
    space = discrete_space()
    distances = dict(space.distances)
    del distances[("a", "b")]
    result = FiniteMetricSpace(space.points, distances).validate()
    assert not result.is_metric
    assert any("incomplete" in error for error in result.errors)


def test_negative_distance_is_rejected():
    space = discrete_space()
    distances = dict(space.distances)
    distances[("a", "b")] = -1
    result = FiniteMetricSpace(space.points, distances).validate()
    assert not result.is_metric
    assert any("nonnegative" in error for error in result.errors)


def test_nonzero_diagonal_is_rejected():
    space = discrete_space()
    distances = dict(space.distances)
    distances[("a", "a")] = 1
    result = FiniteMetricSpace(space.points, distances).validate()
    assert not result.is_metric
    assert any("M1 fails" in error for error in result.errors)


def test_zero_distance_between_distinct_points_is_rejected():
    space = discrete_space()
    distances = dict(space.distances)
    distances[("a", "b")] = 0
    distances[("b", "a")] = 0
    result = FiniteMetricSpace(space.points, distances).validate()
    assert not result.is_metric
    assert any("M1 fails" in error for error in result.errors)


def test_asymmetry_is_rejected():
    space = discrete_space()
    distances = dict(space.distances)
    distances[("a", "b")] = 2
    result = FiniteMetricSpace(space.points, distances).validate()
    assert not result.is_metric
    assert any("M2 fails" in error for error in result.errors)


def test_triangle_inequality_is_checked():
    points = {"a", "b", "c"}
    distances = {
        ("a", "a"): 0, ("b", "b"): 0, ("c", "c"): 0,
        ("a", "b"): 1, ("b", "a"): 1,
        ("b", "c"): 1, ("c", "b"): 1,
        ("a", "c"): 3, ("c", "a"): 3,
    }
    result = FiniteMetricSpace(points, distances).validate()
    assert not result.is_metric
    assert any("M3 fails" in error for error in result.errors)


def test_open_ball_uses_strict_inequality():
    space = discrete_space()
    assert space.open_ball("a", 1) == {"a"}


def test_closed_ball_includes_boundary_points():
    space = discrete_space()
    assert space.closed_ball("a", 1) == {"a", "b", "c"}


def test_metric_topology_of_finite_metric_space_is_discrete():
    topology = discrete_space().metric_topology()
    assert len(topology) == 8
    assert frozenset({"a"}) in topology


def test_finite_metric_space_has_epsilon_net():
    space = discrete_space()
    net = space.epsilon_net(0.5)
    assert space.is_totally_bounded_at(0.5)
    assert net == {"a", "b", "c"}


def test_invalid_center_is_rejected():
    with pytest.raises(ValueError, match="centre"):
        discrete_space().open_ball("z", 1)


def test_nonpositive_radius_is_rejected():
    with pytest.raises(ValueError, match="positive"):
        discrete_space().open_ball("a", 0)
