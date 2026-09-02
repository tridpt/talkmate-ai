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


if __name__ == "__main__":
    unittest.main()
