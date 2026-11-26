
"""Tests for the BasisController."""

import pytest

from topolab.services.basis_controller import BasisController


@pytest.fixture
def controller():
    return BasisController()


# ---------------------------------------------------------
# Basis analysis
# ---------------------------------------------------------

def test_valid_basis_generates_topology(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        "{1, 2}\n{2, 3}\n{2}"
    )

    assert result["ok"] is True
    assert result["isBasis"] is True
    assert result["generatedTopology"] == [
        "∅",
        "{2}",
        "{1, 2}",
        "{2, 3}",
        "{1, 2, 3}",
    ]


def test_invalid_basis_does_not_generate_topology(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        "{1, 2}\n{2, 3}"
    )

    assert result["ok"] is True
    assert result["isBasis"] is False
    assert result["generatedTopology"] == []


def test_basis_with_missing_element_is_invalid(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        "{1, 2}"
    )

    assert result["ok"] is True
    assert result["isBasis"] is False


# ---------------------------------------------------------
# Subbasis analysis
# ---------------------------------------------------------

def test_subbasis_generates_finite_intersections(controller):
    result = controller.analyzeSubbasis(
        "1, 2, 3",
        "{1, 2}\n{2, 3}"
    )

    assert result["ok"] is True
    assert result["finiteIntersections"] == [
        "{2}",
        "{1, 2}",
        "{2, 3}",
        "{1, 2, 3}",
    ]


def test_subbasis_generates_correct_topology(controller):
    result = controller.analyzeSubbasis(
        "1, 2, 3",
        "{1, 2}\n{2, 3}"
    )

    assert result["ok"] is True
    assert result["generatedTopology"] == [
        "∅",
        "{2}",
        "{1, 2}",
        "{2, 3}",
        "{1, 2, 3}",
    ]


def test_single_element_subbasis(controller):
    result = controller.analyzeSubbasis(
        "a, b",
        "{a}"
    )

    assert result["ok"] is True
    assert result["finiteIntersections"] == [
        "{a}",
        "{a, b}",
    ]
    assert result["generatedTopology"] == [
        "∅",
        "{a}",
        "{a, b}",
    ]


# ---------------------------------------------------------
# Input validation
# ---------------------------------------------------------

def test_rejects_empty_universe(controller):
    result = controller.analyzeBasis(
        "",
        "{1}"
    )

    assert result["ok"] is False
    assert result["errors"]


def test_rejects_elements_outside_universe(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        "{1, 4}"
    )

    assert result["ok"] is False
    assert "does not belong to X" in result["message"]


def test_rejects_duplicate_universe_elements(controller):
    result = controller.analyzeBasis(
        "1, 2, 2",
        "{1, 2}"
    )

    assert result["ok"] is False
    assert "duplicate" in result["message"].lower()


def test_rejects_duplicate_elements_inside_subset(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        "{1, 1, 2}"
    )

    assert result["ok"] is False
    assert "duplicate" in result["message"].lower()


def test_rejects_empty_family(controller):
    result = controller.analyzeBasis(
        "1, 2, 3",
        ""
    )

    assert result["ok"] is False
    assert result["errors"]


def test_rejects_duplicate_subsets(controller):
    result = controller.analyzeSubbasis(
        "1, 2",
        "{1}\n{1}"
    )

    assert result["ok"] is False
    assert "duplicate" in result["message"].lower()
