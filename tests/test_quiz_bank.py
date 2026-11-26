import unittest
from topolab.data.exercise_bank import EXERCISES
from topolab.data.quiz_bank import QUIZZES, get_quiz

class QuizBankTests(unittest.TestCase):
    def test_one_quiz_per_subquestion(self):
        self.assertEqual({k: len(v) for k,v in QUIZZES.items()},
                         {e["id"]: len(e["parts"]) for e in EXERCISES})
        self.assertEqual(sum(map(len, QUIZZES.values())), 40)

    def test_every_quiz_has_four_options_and_explanation(self):
        for key, items in QUIZZES.items():
            for i, item in enumerate(items):
                with self.subTest(exercise=key, part=i):
                    question = get_quiz(key, i)
                    self.assertEqual(len(question["options"]), 4)
                    self.assertIn(question["answer"], range(4))
                    self.assertTrue(question["explanation"])

    def test_missing_quiz_is_rejected(self):
        with self.assertRaises(ValueError):
            get_quiz("n1-e1", 99)

if __name__ == "__main__":
    unittest.main()
