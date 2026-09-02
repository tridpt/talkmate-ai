"""Regression tests for TalkMate's scoring and reply-quality guard."""
from __future__ import annotations

import unittest

import app as server
from coach import Coach


class CoachScoringGuardTests(unittest.TestCase):
    """Keep invalid replies from silently earning a conversation score."""

    def setUp(self):
        self.coach = Coach()
        # Tests must be deterministic and never call an external model.
        self.coach.client = None

    def reply(self, level, index, message):
        return self.coach.respond(level, index, "vua", [], message, {}, True)

    def test_valid_sentence_for_every_scene_is_scored(self):
        cases = [
            ("everyday", 0, "I'd like an iced latte to go, please."),
            ("everyday", 1, "Could you tell me where the train station is?"),
            ("everyday", 2, "I just moved into the building."),
            ("everyday", 3, "Could you confirm my reservation date, please?"),
            ("everyday", 4, "I have had a sore throat since yesterday."),
            ("everyday", 5, "Could I ask about the monthly rent and utilities?"),
            ("everyday", 6, "Could you make this dish without peanuts, please?"),
            ("everyday", 7, "You should visit the local museum downtown."),
            ("work", 0, "I have experience leading product projects."),
            ("work", 1, "I suggest we test a smaller launch plan."),
            ("work", 2, "I work in design and would like to connect."),
            ("work", 3, "I propose a simpler solution to this problem."),
        ]
        for level, index, message in cases:
            with self.subTest(level=level, index=index, message=message):
                data = self.reply(level, index, message)
                self.assertTrue(data["scored"])
                self.assertFalse(data["off_topic"])
                self.assertIsNone(data["guard_reason"])
                self.assertEqual(set(data["scores"]), {"relevance", "clarity", "grammar", "word_choice", "sentence", "naturalness", "confidence"})

    def test_relevant_grammar_error_is_scored_for_correction(self):
        data = self.reply("everyday", 0, "I want a coffee, please.")

        self.assertTrue(data["scored"])
        self.assertFalse(data["off_topic"])
        self.assertIn("I'd like", data["improved"])
        self.assertEqual(data["scores"]["relevance"], 10)

    def test_rubric_changes_for_politeness(self):
        direct = self.reply("everyday", 0, "I need coffee now.")
        polite = self.reply("everyday", 0, "Could I have an iced latte to go, please?")

        self.assertLess(direct["scores"]["naturalness"], polite["scores"]["naturalness"])
        self.assertEqual(direct["scores"]["relevance"], polite["scores"]["relevance"])

    def test_common_grammar_patterns_get_deterministic_rewrites(self):
        cases = [
            ("everyday", 3, "I need reservation, please.", "I need a reservation, please."),
            ("everyday", 4, "I need appointment with the doctor.", "I need an appointment with the doctor."),
            ("everyday", 3, "She have a reservation.", "She has a reservation."),
            ("everyday", 5, "I am interested on this apartment.", "I am interested in this apartment."),
            ("everyday", 0, "I can to order coffee.", "I can order coffee."),
            ("everyday", 0, "I want a iced latte, please.", "I want an iced latte, please."),
            ("everyday", 5, "What you are looking for in this apartment?", "What are you looking for in this apartment?"),
            ("work", 1, "How much people are attending the meeting?", "How many people are attending the meeting?"),
            ("work", 1, "I discuss about the launch plan.", "I discuss the launch plan."),
            ("work", 3, "I need advices about the project.", "I need advice about the project."),
        ]
        for level, index, message, expected in cases:
            with self.subTest(message=message):
                data = self.reply(level, index, message)
                self.assertTrue(data["scored"])
                self.assertEqual(data["improved"], expected)
                self.assertEqual(data["scores"]["grammar"], 5)

    def test_correct_articles_are_not_flagged_again(self):
        data = self.reply("everyday", 3, "I need a reservation, please.")

        self.assertTrue(data["scored"])
        self.assertEqual(data["improved"], "")
        self.assertGreaterEqual(data["scores"]["grammar"], 8)

    def test_invalid_replies_receive_no_score(self):
        vietnamese_profanity = chr(273) + chr(7883) + "t symptoms"
        cases = [
            ("everyday", 0, "I love quantum physics", "off_topic"),
            ("everyday", 4, vietnamese_profanity, "profanity"),
            ("everyday", 3, "could you confirm check-in date available reservation", "keyword_soup"),
            ("everyday", 0, "receipt still or sparkling still or sparkling for here for here", "repeated"),
            ("everyday", 0, "to go to go to go to go to go", "repeated"),
            ("everyday", 3, "reservation", "incomplete"),
            ("everyday", 3, "to go", "off_topic"),
        ]
        for level, index, message, reason in cases:
            with self.subTest(level=level, index=index, message=message):
                data = self.reply(level, index, message)
                self.assertFalse(data["scored"])
                self.assertTrue(data["off_topic"])
                self.assertIsNone(data["overall"])
                self.assertEqual(data["scores"], {})
                self.assertEqual(data["guard_reason"], reason)
                self.assertFalse(data["done"])

    def test_short_contextual_replies_are_allowed_only_when_relevant(self):
        self.assertTrue(self.reply("everyday", 0, "to go")["scored"])
        self.assertTrue(self.reply("everyday", 0, "for here")["scored"])
        self.assertFalse(self.reply("everyday", 3, "to go")["scored"])


class ReplyApiScoringTests(unittest.TestCase):
    """Verify the browser-facing endpoint preserves the scoring contract."""

    @classmethod
    def setUpClass(cls):
        cls.original_client = server.coach.client
        server.coach.client = None
        cls.client = server.app.test_client()

    @classmethod
    def tearDownClass(cls):
        server.coach.client = cls.original_client

    def test_api_returns_no_score_for_keyword_spam(self):
        response = self.client.post(
            "/api/reply",
            json={
                "level": "everyday",
                "scenario_index": 0,
                "message": "to go to go to go to go to go",
                "history": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data["scored"])
        self.assertTrue(data["off_topic"])
        self.assertEqual(data["guard_reason"], "repeated")
        self.assertIsNone(data["overall"])
        self.assertEqual(data["scores"], {})

    def test_api_scores_a_complete_relevant_sentence(self):
        response = self.client.post(
            "/api/reply",
            json={
                "level": "everyday",
                "scenario_index": 3,
                "message": "Could you confirm my reservation date, please?",
                "history": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["scored"])
        self.assertFalse(data["off_topic"])
        self.assertIsNone(data["guard_reason"])
        self.assertIsInstance(data["overall"], float)
        self.assertEqual(len(data["scores"]), 7)


if __name__ == "__main__":
    unittest.main()
