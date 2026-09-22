"""Regression tests for synced personal review progress."""
from __future__ import annotations

import unittest

import database


class ReviewProgressTests(unittest.TestCase):
    def test_review_items_and_daily_drills_are_normalized(self):
        progress = database.normalize_progress({
            "reviewItems": [{
                "id": "review-1",
                "source": "She have a reservation.",
                "correction": "She has a reservation.",
                "category": "verb_forms",
                "exercise": "Fix the verb form.",
                "attempts": 3,
                "correct": 2,
            }],
            "review": {
                "dailyCompleted": {"2026-09-02": 4},
                "sessions": 4,
                "attempts": 3,
                "correct": 2,
            },
        })

        self.assertEqual(progress["review"]["dailyCompleted"]["2026-09-02"], 4)
        self.assertEqual(progress["reviewItems"][0]["category"], "verb_forms")
        self.assertEqual(progress["reviewItems"][0]["attempts"], 3)

    def test_merge_keeps_review_attempt_metadata(self):
        existing = database.normalize_progress({
            "reviewItems": [{
                "source": "I am interested on this apartment.",
                "correction": "I am interested in this apartment.",
                "category": "prepositions",
                "attempts": 1,
                "correct": 0,
            }],
            "review": {"dailyCompleted": {"2026-09-02": 1}, "attempts": 1},
        })
        incoming = database.normalize_progress({
            "reviewItems": [{
                "source": "I am interested on this apartment.",
                "correction": "I am interested in this apartment.",
                "category": "prepositions",
                "attempts": 3,
                "correct": 2,
                "lastReviewedDay": "2026-09-02",
            }],
            "review": {"dailyCompleted": {"2026-09-02": 3}, "attempts": 3, "correct": 2},
        })

        merged = database.merge_progress(existing, incoming)
        item = merged["reviewItems"][0]
        self.assertEqual(item["attempts"], 3)
        self.assertEqual(item["correct"], 2)
        self.assertEqual(merged["review"]["dailyCompleted"]["2026-09-02"], 3)

    def test_placement_result_survives_progress_normalization(self):
        progress = database.normalize_progress({
            "profile": {
                "proficiency": "B1",
                "placement": {
                    "level": "B1",
                    "overall": 7.4,
                    "answersScored": 3,
                    "completedAt": "2026-09-22T12:00:00Z",
                    "focus": "Ưu tiên cấu trúc câu trong các buổi luyện đầu tiên.",
                },
            },
        })

        placement = progress["profile"]["placement"]
        self.assertEqual(placement["level"], "B1")
        self.assertEqual(placement["answersScored"], 3)
        self.assertEqual(placement["overall"], 7.4)


if __name__ == "__main__":
    unittest.main()
