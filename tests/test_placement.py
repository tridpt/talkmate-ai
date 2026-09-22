"""Regression tests for TalkMate's short starting-level check."""
from __future__ import annotations

import unittest

import app as server
from coach import evaluate_placement, placement_questions


VALID_ANSWERS = [
    "My name is Linh and I work in design. I enjoy meeting new people.",
    "I would like an iced latte with oat milk to go, please.",
    "I think we should test a smaller launch because it will help us learn from users.",
]


class PlacementCoachTests(unittest.TestCase):
    def test_questions_expose_only_browser_metadata(self):
        questions = placement_questions()

        self.assertEqual(len(questions), 3)
        self.assertTrue(all("topic_terms" not in question for question in questions))
        self.assertTrue(all(question["prompt"] and question["hint_en"] for question in questions))

    def test_relevant_answers_produce_a_practical_starting_level(self):
        result = evaluate_placement(VALID_ANSWERS)

        self.assertEqual(result["answers_scored"], 3)
        self.assertEqual(result["total_questions"], 3)
        self.assertGreaterEqual(result["overall"], 6)
        self.assertIn(result["recommendation"]["level"], {"B1", "B2"})
        self.assertTrue(result["recommendation"]["focus"])

    def test_unrelated_answers_start_at_a1_without_earning_scores(self):
        result = evaluate_placement(["hello", "hello", "hello"])

        self.assertEqual(result["answers_scored"], 0)
        self.assertEqual(result["recommendation"]["level"], "A1")
        self.assertTrue(all(not item["scored"] for item in result["results"]))


class PlacementApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.app.test_client()

    def test_get_returns_three_questions(self):
        response = self.client.get("/api/placement")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["questions"]), 3)

    def test_post_requires_every_answer(self):
        response = self.client.post("/api/placement", json={"answers": VALID_ANSWERS[:2]})

        self.assertEqual(response.status_code, 400)

    def test_post_scores_the_completed_check(self):
        response = self.client.post("/api/placement", json={"answers": VALID_ANSWERS})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["answers_scored"], 3)
        self.assertIn(data["recommendation"]["level"], {"B1", "B2"})


if __name__ == "__main__":
    unittest.main()
