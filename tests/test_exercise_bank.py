import unittest

from topolab.data.exercise_bank import EXERCISES, get_exercises


class ExerciseBankTests(unittest.TestCase):
    def test_all_fourteen_source_exercises_are_present(self):
        self.assertEqual(len(EXERCISES), 14)
        self.assertEqual(len(get_exercises("N1")), 10)
        self.assertEqual(len(get_exercises("N2")), 4)

    def test_every_exercise_has_parts_solution_and_quiz(self):
        for exercise in EXERCISES:
            with self.subTest(exercise=exercise["id"]):
                self.assertTrue(exercise["parts"])
                self.assertEqual(len(exercise["parts"]), len(exercise["solutions"]))
                self.assertIn("question", exercise["quiz"])
                self.assertEqual(len(exercise["quiz"]["options"]), 4)
                self.assertIn(exercise["quiz"]["answer"], range(4))

    def test_invalid_sheet_is_rejected(self):
        with self.assertRaises(ValueError):
            get_exercises("N3")


if __name__ == "__main__":
    unittest.main()
