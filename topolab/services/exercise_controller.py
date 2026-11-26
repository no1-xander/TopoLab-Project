"""Qt-facing exercise and quiz controller."""
from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal, Slot
from topolab.data.exercise_bank import get_exercises


class ExerciseController(QObject):
    """Expose source exercises, proof notes, and deterministic quiz feedback."""

    exercisesChanged = Signal()
    currentChanged = Signal()
    feedbackChanged = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._sheet = "ALL"
        self._exercises = get_exercises()
        self._current_id = self._exercises[0]["id"]
        self._feedback = {}
        self._last_quiz = None

    @Property("QVariantList", notify=exercisesChanged)
    def exercises(self):
        return self._exercises

    @Property("QVariantMap", notify=currentChanged)
    def currentExercise(self):
        return next((e for e in self._exercises if e["id"] == self._current_id), {})

    @Property(str, notify=feedbackChanged)
    def feedback(self):
        return self._feedback.get(self._current_id, "")

    @Slot(str)
    def setSheet(self, sheet: str) -> None:
        if sheet not in {"ALL", "N1", "N2"}:
            return
        self._sheet = sheet
        self._exercises = get_exercises(sheet)
        if self._exercises:
            self._current_id = self._exercises[0]["id"]
        self._feedback.clear()
        self.exercisesChanged.emit()
        self.currentChanged.emit()
        self.feedbackChanged.emit()

    @Slot(str)
    def selectExercise(self, exercise_id: str) -> None:
        if any(e["id"] == exercise_id for e in self._exercises):
            self._current_id = exercise_id
            self.currentChanged.emit()
            self.feedbackChanged.emit()

    @Slot(int, result="QVariantMap")
    def checkAnswer(self, selected_index: int):
        exercise = self.currentExercise
        quiz = exercise.get("quiz")
        if not quiz:
            return {"valid": False, "correct": False, "message": "No quiz item is available."}
        correct = selected_index == quiz["answer"]
        message = ("Correct. " if correct else "Not quite. The correct answer is: "
                   + quiz["options"][quiz["answer"]] + ". ") + quiz["explanation"]
        self._feedback[self._current_id] = message
        self.feedbackChanged.emit()
        return {"valid": True, "correct": correct, "message": message,
                "correctIndex": quiz["answer"]}

    @Slot(result="QVariantMap")
    def quizQuestion(self):
        """Return the selected exercise's objectively keyed multiple-choice item."""
        quiz = self.currentExercise.get("quiz", {})
        return dict(quiz)

    @Slot(result="QVariantList")
    def quizOptions(self):
        return list(self.currentExercise.get("quiz", {}).get("options", []))

    @Slot()
    def clearFeedback(self):
        self._feedback.pop(self._current_id, None)
        self.feedbackChanged.emit()
