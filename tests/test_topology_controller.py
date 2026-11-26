
import unittest

from topolab.services.topology_controller import TopologyController


class TestTopologyController(unittest.TestCase):

    def setUp(self):
        self.controller = TopologyController()

    def test_valid_topology(self):
        result = self.controller.validateTopology(
            "a, b, c",
            "∅\n{a}\n{a,b}\nX",
        )
        self.assertTrue(result["isTopology"])

    def test_invalid_topology(self):
        result = self.controller.validateTopology(
            "a, b, c",
            "∅\n{a}\n{b}\nX",
        )
        self.assertFalse(result["isTopology"])

    def test_invalid_element(self):
        result = self.controller.validateTopology(
            "a, b",
            "∅\n{c}\nX",
        )
        self.assertFalse(result["ok"])

    def test_subset_analysis(self):
        result = self.controller.analyzeSubset(
            "a, b, c",
            "∅\n{a}\n{a,b}\nX",
            "{b}",
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["interior"], "∅")
        self.assertEqual(result["closure"], "{b, c}")
        self.assertEqual(result["boundary"], "{b, c}")

    def test_reject_invalid_topology_for_analysis(self):
        result = self.controller.analyzeSubset(
            "a, b, c",
            "∅\n{a}\n{b}\nX",
            "{a}",
        )
        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
