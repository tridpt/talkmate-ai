from __future__ import annotations

import unittest

import app as server
import scenarios


class SentenceLibraryTests(unittest.TestCase):
    def test_library_covers_core_communication_goals(self):
        categories = scenarios.sentence_library()

        self.assertGreaterEqual(len(categories), 5)
        self.assertEqual(
            {category["id"] for category in categories},
            {
                "polite-questions",
                "polite-refusals",
                "clarification",
                "opinions",
                "agreement-disagreement",
            },
        )
        for category in categories:
            self.assertTrue(category["label"])
            self.assertTrue(category["description"])
            self.assertGreaterEqual(len(category["items"]), 2)
            for item in category["items"]:
                self.assertTrue(item["title"])
                self.assertTrue(item["structure"])
                self.assertTrue(item["when"])
                self.assertGreaterEqual(len(item["examples"]), 2)

    def test_library_endpoint_returns_offline_content(self):
        response = server.app.test_client().get("/api/sentence-library")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("categories", payload)
        self.assertEqual(len(payload["categories"]), 5)
        self.assertIn("Could you tell me where the station is?", str(payload))

    def test_context_exercise_returns_correction_for_notebook(self):
        response = server.app.test_client().post(
            "/api/sentence-exercise",
            json={
                "exercise_id": "move-reservation",
                "message": "I want reservation",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["scored"])
        self.assertEqual(payload["improved"], "I want a reservation")
        self.assertTrue(payload["saved_to_notebook"])
        self.assertEqual(payload["exercise"]["id"], "move-reservation")

    def test_context_exercise_does_not_score_vietnamese_text(self):
        response = server.app.test_client().post(
            "/api/sentence-exercise",
            json={
                "exercise_id": "directions",
                "message": "Tôi muốn hỏi đường đến ga tàu",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertFalse(payload["scored"])
        self.assertEqual(payload["guard_reason"], "language")

    def test_context_exercise_rejects_unrelated_english_sentence(self):
        response = server.app.test_client().post(
            "/api/sentence-exercise",
            json={
                "exercise_id": "directions",
                "message": "I watched a movie last night.",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertFalse(payload["scored"])
        self.assertEqual(payload["guard_reason"], "off_topic")
        self.assertIsNone(payload["overall"])

    def test_context_exercise_accepts_different_relevant_wording(self):
        response = server.app.test_client().post(
            "/api/sentence-exercise",
            json={
                "exercise_id": "directions",
                "message": "Would you mind telling me how to walk to the train station?",
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["scored"])
        self.assertFalse(payload["off_topic"])


if __name__ == "__main__":
    unittest.main()
