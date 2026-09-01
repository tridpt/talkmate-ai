"""English role-play partner with structured, learner-friendly feedback."""
from __future__ import annotations

import json
import re

import config
import scenarios

SCORE_KEYS = ["clarity", "grammar", "naturalness", "confidence"]
SCORE_LABELS = {
    "clarity": "Clarity",
    "grammar": "Grammar",
    "naturalness": "Naturalness",
    "confidence": "Confidence",
}

DIFFICULTY = {
    "de": "A relaxed, patient partner using simple language.",
    "vua": "A natural, encouraging partner with one thoughtful follow-up at a time.",
    "kho": "A quicker, more demanding but always respectful partner who asks specific follow-ups.",
}

# These phrases are common points of friction for Vietnamese English learners.
PRONUNCIATION_PATTERNS = [
    (r"\bi'd\b", "I'd", "Finish the /d/ cleanly before the next word."),
    (r"\bwould you\b", "would you", "Link the final /d/ into /ju:/."),
    (r"\bcould you\b", "could you", "Keep the vowel in 'could' short: /kʊd/."),
    (r"\bcoffee\b", "coffee", "Stress the first syllable: /ˈkɔː.fi/."),
    (r"\bplease\b", "please", "Hold the long vowel /i:/ a little longer."),
    (r"\bthank you\b", "thank you", "Let the tongue touch lightly for /th/, not /t/."),
    (r"\bthree\b", "three", "Start with a soft /th/ and keep /i:/ long."),
    (r"\bthought\b", "thought", "Use a soft /th/ and round the vowel /ɔː/."),
    (r"\binterview\b", "interview", "Stress the first syllable: /ˈɪn.tə.vjuː/."),
    (r"\bcomfortable\b", "comfortable", "Say it in three beats: /ˈkʌmf.tə.bəl/."),
]


def _system_prompt(level: dict, scenario: dict, difficulty: str, learner: dict, english_only: bool) -> str:
    preferred_goal = learner.get("goal") or "Speak naturally and confidently in English."
    recurring_errors = ", ".join(learner.get("recurring_errors") or []) or "No reliable pattern yet."
    strengths = ", ".join(learner.get("strengths") or []) or "Still getting to know the learner."
    feedback_language = "English" if english_only else "Vietnamese"
    return f"""You are TalkMate, an expert English-speaking role-play partner and a kind micro-coach for a Vietnamese learner.

The learner is practicing this real-life scenario:
Title: {scenario['title']}
Context: {scenario['context']}
Your character: {scenario['persona']}
Learning goal: {level['goal']}
Challenge: {DIFFICULTY.get(difficulty, DIFFICULTY['vua'])}

Learner profile (use it quietly and constructively):
- Current level: {learner.get('proficiency') or 'A2'}
- Preferred situations: {learner.get('target') or 'travel and everyday life'}
- Personal goal: {preferred_goal}
- Recurring patterns to help with: {recurring_errors}
- Strengths to reinforce: {strengths}

After each learner message, respond in English as the character and give concise feedback in {feedback_language}.
Keep the role-play reply natural, 1-2 short sentences, and continue the scenario. Do not translate the whole conversation.

Role-play rules:
- React to the learner's exact meaning, tone, details, and questions rather than following a fixed script.
- Let the conversation change direction naturally when the learner introduces a sensible new detail.
- Use the learner profile to select only one high-value improvement at a time; do not mention that a profile exists.

Feedback rules:
- Praise what is understandable first. Correct only the one most important grammar, word choice, or politeness issue.
- `improved` must be a natural English rewrite of the learner's exact meaning, or an empty string if it is already excellent.
- `feedback` and `tip` must be short {feedback_language} sentences. `tip` teaches one reusable English phrase.
- Score clarity, grammar, naturalness, confidence from 0 to 10.
- Set done true after 4-7 learner turns when the scenario has a satisfying close.

Return valid JSON only:
{{"reply":"...", "feedback":"...", "improved":"...", "tip":"...", "scores":{{"clarity":0,"grammar":0,"naturalness":0,"confidence":0}}, "done":false}}"""


def _build_contents(history: list[dict], user_message: str):
    contents = []
    for turn in history:
        role = "user" if turn.get("role") == "user" else "model"
        text = turn.get("text", "")
        if text:
            contents.append({"role": role, "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})
    return contents


class Coach:
    """Use Gemini when configured; fall back to a useful offline practice mode."""

    def __init__(self):
        self.client = None
        if config.ai_enabled():
            try:
                from google import genai

                self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            except Exception as exc:  # pragma: no cover - depends on local setup
                print(f"[WARN] Gemini unavailable; using offline mode: {exc}")

    @property
    def online(self) -> bool:
        return self.client is not None

    def respond(self, level_id, scenario_index, difficulty, history, user_message, learner=None, english_only=False):
        level = scenarios.get_level(level_id)
        scenario = scenarios.get_scenario(level_id, scenario_index)
        if not level or not scenario:
            return {"error": "Invalid level or scenario."}
        learner = _normalize_learner(learner)
        if self.online:
            try:
                return self._respond_ai(level, scenario, difficulty, history, user_message, learner, english_only)
            except Exception as exc:  # pragma: no cover - external service
                print(f"[WARN] Gemini request failed; using offline mode: {exc}")
        return self._respond_offline(scenario, history, user_message, learner, english_only)

    def _respond_ai(self, level, scenario, difficulty, history, user_message, learner, english_only):
        from google.genai import types

        response = self.client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=_build_contents(history, user_message),
            config=types.GenerateContentConfig(
                system_instruction=_system_prompt(level, scenario, difficulty, learner, english_only),
                response_mime_type="application/json",
                temperature=0.8,
            ),
        )
        return _normalize(_parse_json(getattr(response, "text", "") or ""), mode="ai")

    def _respond_offline(self, scenario, history, user_message, learner, english_only):
        user_turns = sum(turn.get("role") == "user" for turn in history)
        replies = scenario.get("offline_replies", [])
        done = user_turns >= len(replies)
        reply = "That was lovely talking with you. Have a great day!" if done else replies[user_turns % len(replies)]
        scores, feedback, improved, tip = _review_offline(user_message, scenario, learner, english_only)
        return _normalize(
            {
                "reply": reply,
                "feedback": feedback,
                "improved": improved,
                "tip": tip,
                "scores": scores,
                "done": done,
            },
            mode="offline",
        )


def _parse_json(text: str) -> dict:
    try:
        return json.loads(text.strip())
    except (json.JSONDecodeError, AttributeError):
        match = re.search(r"\{.*\}", text or "", re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {}


def _clamp_score(value) -> int:
    try:
        return max(0, min(10, int(round(float(value)))))
    except (TypeError, ValueError):
        return 5


def _normalize(data: dict, mode: str) -> dict:
    raw_scores = data.get("scores") or {}
    scores = {key: _clamp_score(raw_scores.get(key, 5)) for key in SCORE_KEYS}
    return {
        "reply": str(data.get("reply") or "...").strip(),
        "feedback": str(data.get("feedback") or "").strip(),
        "improved": str(data.get("improved") or "").strip(),
        "tip": str(data.get("tip") or "").strip(),
        "scores": scores,
        "overall": round(sum(scores.values()) / len(scores), 1),
        "done": bool(data.get("done", False)),
        "mode": mode,
    }


def _normalize_learner(learner) -> dict:
    """Keep the client-held learning memory compact before it reaches the model."""
    learner = learner if isinstance(learner, dict) else {}

    def clean_list(value):
        if not isinstance(value, list):
            return []
        return [str(item).strip()[:90] for item in value if str(item).strip()][:5]

    return {
        "goal": str(learner.get("goal") or "").strip()[:180],
        "proficiency": str(learner.get("proficiency") or "A2").strip()[:10],
        "target": str(learner.get("target") or "").strip()[:50],
        "recurring_errors": clean_list(learner.get("recurring_errors")),
        "strengths": clean_list(learner.get("strengths")),
    }


def pronunciation_check(transcript: str, confidence: float | None = None) -> dict:
    """Estimate speech clarity from browser speech recognition output.

    This is intentionally transparent: it is a clarity estimate, not a clinical
    pronunciation grade, and it tells the learner exactly what to rehearse.
    """
    text = (transcript or "").strip()
    if not text:
        return {
            "score": 0,
            "label": "No speech detected",
            "heard": "",
            "unclear_words": [],
            "tip": "Try speaking a little closer to the microphone.",
        }
    lower = text.lower()
    words = re.findall(r"[A-Za-z']+", text)
    unclear = []
    seen = set()
    for pattern, word, tip in PRONUNCIATION_PATTERNS:
        if re.search(pattern, lower) and word.lower() not in seen:
            unclear.append({"word": word, "tip": tip})
            seen.add(word.lower())
    # Recognition confidence is 0..1 in browsers that expose it; otherwise use
    # a neutral baseline and let the word-level cues carry the explanation.
    base = 92 if confidence is None else round(max(0, min(1, confidence)) * 100)
    score = max(45, min(98, base - len(unclear) * 7))
    if score >= 88:
        label = "Very clear"
    elif score >= 72:
        label = "Mostly clear"
    else:
        label = "Needs a little practice"
    return {
        "score": score,
        "label": label,
        "heard": text,
        "unclear_words": unclear[:4],
        "tip": "Repeat the highlighted words slowly, then say the whole sentence at normal speed." if unclear else "Great clarity. Try connecting the words a little more smoothly.",
    }


def _review_offline(message: str, scenario: dict, learner: dict, english_only: bool):
    """Give a focused local correction so the app stays useful without an API key."""
    text = message.strip()
    lower = text.lower()
    words = len(re.findall(r"\b[\w']+\b", text))
    scores = {"clarity": 6, "grammar": 7, "naturalness": 6, "confidence": 7}
    feedback = "Your meaning is clear. Keep the conversation moving." if english_only else "Ý của bạn rõ ràng, cứ tiếp tục giữ nhịp hội thoại nhé."
    improved = ""
    tip = f"Try: “{scenario['starter']}”" if english_only else f"Bạn có thể dùng: “{scenario['starter']}”"

    fixes = [
        (r"\bi want\b", "I'd like", "'I want' is correct, but 'I'd like' sounds more polite here." if english_only else "‘I want’ đúng nhưng khá trực tiếp khi gọi món hoặc nhờ vả."),
        (r"\bi am agree\b", "I agree", "Say 'I agree' - no 'am' is needed." if english_only else "Sau ‘I’ không cần dùng ‘am’ trước ‘agree’."),
        (r"\bhow much is it\b", "How much is it?", "End this question with rising intonation." if english_only else "Câu hỏi nghe tự nhiên hơn khi thêm dấu hỏi và ngữ điệu lên ở cuối câu."),
        (r"\bi very like\b", "I really like", "Use 'really' before the verb, not 'very'." if english_only else "Dùng ‘really’ trước động từ sẽ tự nhiên hơn ‘very’."),
        (r"\bcan you to\b", "Can you", "After 'can', use the base verb without 'to'." if english_only else "Sau ‘can’ dùng động từ nguyên mẫu, không dùng ‘to’."),
    ]
    for pattern, replacement, note in fixes:
        if re.search(pattern, lower):
            improved = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            feedback = note
            scores["grammar"] = 5
            scores["naturalness"] = 5
            tip = f"Try: “{improved}”" if english_only else f"Thử nói: “{improved}”"
            break
    else:
        if words < 4:
            feedback = "Your reply is a little short, so it is harder to build a real conversation." if english_only else "Câu trả lời hơi ngắn, nên khó tạo phản xạ hội thoại."
            scores["clarity"] = 4
            scores["confidence"] = 5
            tip = "Add one detail or a question: “Could you tell me more?”" if english_only else "Thêm một chi tiết hoặc một câu hỏi: “Could you tell me more?”"
        elif not re.search(r"[?.!]$", text):
            feedback = "Your sentence is clear. Let your voice fall at the end so it sounds complete." if english_only else "Câu của bạn dễ hiểu. Khi nói, hãy hạ giọng ở cuối câu để nghe trọn ý hơn."
        elif "please" in lower or "could" in lower:
            feedback = "Very good - your wording is polite and natural." if english_only else "Rất tốt - bạn dùng cách nói lịch sự và tự nhiên."
            scores["naturalness"] = 8
            scores["confidence"] = 8

    return scores, feedback, improved, tip
