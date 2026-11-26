import tempfile
import unittest
from pathlib import Path
from topolab.services.draft_store import DraftStore

class DraftStoreTests(unittest.TestCase):
    def test_draft_persists_across_instances(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "progress.json"
            DraftStore(p).save_draft("n1-e1", 0, "Proof draft")
            self.assertEqual(DraftStore(p).get_draft("n1-e1", 0), "Proof draft")

    def test_quiz_statistics_persist(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "progress.json"
            store = DraftStore(p)
            store.record_attempt("n1-e1", 2, False)
            stats = store.record_attempt("n1-e1", 2, True)
            self.assertEqual(stats, {"attempts": 2, "correct": 1})
            self.assertEqual(DraftStore(p).get_stats("n1-e1", 2), stats)

    def test_empty_draft_persists(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "progress.json"
            store = DraftStore(p)
            store.save_draft("n1-e1", 0, "text")
            store.save_draft("n1-e1", 0, "")
            self.assertEqual(DraftStore(p).get_draft("n1-e1", 0), "")

    def test_invalid_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store = DraftStore(Path(d) / "p.json")
            with self.assertRaises(ValueError):
                store.save_draft("", 0, "x")

if __name__ == "__main__":
    unittest.main()
