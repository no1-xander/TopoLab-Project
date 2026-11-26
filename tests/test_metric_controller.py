from topolab.services.metric_controller import MetricController


POINTS = "a, b, c"
DISCRETE_TABLE = """a, a, 0
a, b, 1
a, c, 1
b, a, 1
b, b, 0
b, c, 1
c, a, 1
c, b, 1
c, c, 0"""


def test_controller_validates_metric_and_calculates_balls():
    result = MetricController().analyzeMetric(
        POINTS, DISCRETE_TABLE, "a", "1"
    )
    assert result["ok"] is True
    assert result["isMetric"] is True
    assert result["openBall"] == "{a}"
    assert result["closedBall"] == "{a, b, c}"
    assert result["isDiscrete"] is True


def test_controller_rejects_incomplete_table():
    result = MetricController().analyzeMetric(
        POINTS, "a, a, 0", "a", "1"
    )
    assert result["ok"] is False
    assert any("incomplete" in error for error in result["errors"])


def test_controller_rejects_non_metric_table():
    invalid = DISCRETE_TABLE.replace("a, c, 1", "a, c, 3").replace(
        "c, a, 1", "c, a, 3"
    )
    result = MetricController().analyzeMetric(POINTS, invalid, "a", "2")
    assert result["ok"] is False
    assert any("M3 fails" in error for error in result["errors"])


def test_controller_rejects_unknown_center():
    result = MetricController().analyzeMetric(
        POINTS, DISCRETE_TABLE, "z", "1"
    )
    assert result["ok"] is False
    assert "centre" in result["errors"][0]


def test_controller_rejects_nonpositive_radius():
    result = MetricController().analyzeMetric(
        POINTS, DISCRETE_TABLE, "a", "0"
    )
    assert result["ok"] is False
    assert "positive" in result["errors"][0]


def test_controller_rejects_bad_distance_row():
    result = MetricController().analyzeMetric(
        POINTS, "a,b", "a", "1"
    )
    assert result["ok"] is False
    assert "format" in result["errors"][0]
