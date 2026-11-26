"""Qt-facing exercise, per-part quiz, persistence, and finite-example controller."""
from pathlib import Path
from PySide6.QtCore import QObject, Property, Signal, Slot
from topolab.core.example_validation import check_finite_topology_example
from topolab.data.exercise_bank import get_exercises
from topolab.data.quiz_bank import get_quiz
from topolab.services.draft_store import DraftStore


class ExerciseController(QObject):
    exercisesChanged = Signal()
    currentChanged = Signal()
    feedbackChanged = Signal()
    progressChanged = Signal()

    def __init__(self, progress_file=None):
        super().__init__()
        self._all = get_exercises()
        self._exercises = get_exercises()
        self._sheet = "ALL"
        self._current_id = self._exercises[0]["id"]
        self._part = 0
        self._feedback = ""
        path = progress_file or Path.home() / ".topolab" / "progress.json"
        self._store = DraftStore(path)

    @Property("QVariantList", notify=exercisesChanged)
    def exercises(self):
        return self._exercises

    @Property("QVariantMap", notify=currentChanged)
    def currentExercise(self):
        return next((item for item in self._exercises
                     if item["id"] == self._current_id), {})

    @Property(int, notify=currentChanged)
    def currentPartIndex(self):
        return self._part

    @Property("QVariantMap", notify=currentChanged)
    def currentQuiz(self):
        try:
            return get_quiz(self._current_id, self._part)
        except ValueError:
            return {}

    @Property(str, notify=feedbackChanged)
    def feedback(self):
        return self._feedback

    @Property("QVariantMap", notify=progressChanged)
    def progress(self):
        return self._store.get_stats(self._current_id, self._part)

    @Slot(str)
    def setSheet(self, sheet):
        if sheet not in {"ALL", "N1", "N2"}:
            return
        self._sheet = sheet
        self._exercises = get_exercises(sheet)
        self._current_id = self._exercises[0]["id"]
        self._part = 0
        self._feedback = ""
        self.exercisesChanged.emit()
        self.currentChanged.emit()
        self.feedbackChanged.emit()
        self.progressChanged.emit()

    @Slot(str)
    def selectExercise(self, exercise_id):
        if any(item["id"] == exercise_id for item in self._exercises):
            self._current_id, self._part, self._feedback = exercise_id, 0, ""
            self.currentChanged.emit()
            self.feedbackChanged.emit()
            self.progressChanged.emit()

    @Slot(int)
    def setCurrentPart(self, part_index):
        if 0 <= part_index < len(self.currentExercise.get("parts", [])):
            self._part, self._feedback = part_index, ""
            self.currentChanged.emit()
            self.feedbackChanged.emit()
            self.progressChanged.emit()

    @Slot(str, int, result=str)
    def draftFor(self, exercise_id, part_index):
        if not any(item["id"] == exercise_id for item in self._all):
            return ""
        try:
            return self._store.get_draft(exercise_id, part_index)
        except ValueError:
            return ""

    @Slot(str, int, str, result=bool)
    def saveDraft(self, exercise_id, part_index, draft):
        exercise = next((item for item in self._all
                         if item["id"] == exercise_id), None)
        if exercise is None or not 0 <= part_index < len(exercise["parts"]):
            return False
        self._store.save_draft(exercise_id, part_index, draft)
        return True

    @Slot(int, result="QVariantMap")
    def checkAnswer(self, selected_index):
        quiz = self.currentQuiz
        if not quiz:
            return {"valid": False, "correct": False,
                    "message": "No quiz question is available."}
        correct = selected_index == quiz["answer"]
        stats = self._store.record_attempt(self._current_id, self._part, correct)
        prefix = "Correct. " if correct else (
            "Not quite. The correct answer is: " + quiz["options"][quiz["answer"]] + ". "
        )
        self._feedback = prefix + quiz["explanation"]
        self.feedbackChanged.emit()
        self.progressChanged.emit()
        return {"valid": True, "correct": correct, "message": self._feedback,
                "correctIndex": quiz["answer"], "attempts": stats["attempts"],
                "correctAttempts": stats["correct"]}

    @Slot()
    def clearFeedback(self):
        self._feedback = ""
        self.feedbackChanged.emit()

    @Slot(str, str, str, result="QVariantMap")
    def checkFiniteExample(self, universe, topology, subset):
        return check_finite_topology_example(universe, topology, subset)
