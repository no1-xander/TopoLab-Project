
from topolab.services.topology_controller import TopologyController


def test_subset_classification():
    controller = TopologyController()

    result = controller.analyzeSubset(
        "a, b, c",
        "∅\n{a}\n{a,b}\nX",
        "{b}"
    )

    assert result["ok"] is True
    assert result["isOpen"] is False
    assert result["isClosed"] is False
    assert result["isClopen"] is False
    assert result["complement"] == "{a, c}"
    assert result["accumulationPoints"] == "{c}"
    assert result["isolatedPoints"] == "{b}"


def test_neighborhood_analysis():
    controller = TopologyController()

    result = controller.analyzePoint(
        "a, b, c",
        "∅\n{a}\n{a,b}\nX",
        "b"
    )

    assert result["ok"] is True
    assert result["point"] == "b"
    assert set(result["neighborhoods"]) == {
        "{a, b}",
        "{a, b, c}",
    }


def test_discrete_space_is_hausdorff():
    controller = TopologyController()

    result = controller.analyzeHausdorff(
        "a, b",
        "∅\n{a}\n{b}\nX"
    )

    assert result["ok"] is True
    assert result["isHausdorff"] is True
    assert result["inseparablePairs"] == []


def test_indiscrete_space_is_not_hausdorff():
    controller = TopologyController()

    result = controller.analyzeHausdorff(
        "a, b",
        "∅\nX"
    )

    assert result["ok"] is True
    assert result["isHausdorff"] is False
    assert result["inseparablePairs"] == ["(a, b)"]


def test_invalid_point():
    controller = TopologyController()

    result = controller.analyzePoint(
        "a, b, c",
        "∅\n{a}\n{a,b}\nX",
        "a, b"
    )

    assert result["ok"] is False
