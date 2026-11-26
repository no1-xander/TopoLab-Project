"""Atomic local persistence for proof drafts and quiz statistics."""
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


class DraftStore:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = {"drafts": {}, "quiz_stats": {}}
        if self.file_path.exists():
            try:
                loaded = json.loads(self.file_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError(f"Cannot read saved progress: {error}") from error
            if not isinstance(loaded, dict):
                raise ValueError("Saved progress has an invalid format.")
            for key in self.data:
                value = loaded.get(key, {})
                if not isinstance(value, dict):
                    raise ValueError("Saved progress has an invalid format.")
                self.data[key] = value

    @staticmethod
    def key(exercise_id, part_index):
        if not exercise_id or part_index < 0:
            raise ValueError("Invalid exercise ID or part index.")
        return f"{exercise_id}:{part_index}"

    def get_draft(self, exercise_id, part_index):
        return str(self.data["drafts"].get(self.key(exercise_id, part_index), ""))

    def save_draft(self, exercise_id, part_index, text):
        self.data["drafts"][self.key(exercise_id, part_index)] = str(text)
        self._write()

    def get_stats(self, exercise_id, part_index):
        value = self.data["quiz_stats"].get(self.key(exercise_id, part_index), {})
        return {"attempts": int(value.get("attempts", 0)),
                "correct": int(value.get("correct", 0))}

    def record_attempt(self, exercise_id, part_index, correct):
        key = self.key(exercise_id, part_index)
        stats = self.get_stats(exercise_id, part_index)
        stats["attempts"] += 1
        stats["correct"] += int(bool(correct))
        self.data["quiz_stats"][key] = stats
        self._write()
        return stats

    def _write(self):
        temp = None
        try:
            with NamedTemporaryFile("w", encoding="utf-8", dir=self.file_path.parent,
                    prefix=self.file_path.name + ".", suffix=".tmp", delete=False) as stream:
                temp = Path(stream.name)
                json.dump(self.data, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, self.file_path)
        finally:
            if temp and temp.exists():
                temp.unlink()
