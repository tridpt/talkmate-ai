"""English role-play partner with structured, learner-friendly feedback."""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter

import config
import scenarios

SCORE_KEYS = ["relevance", "grammar", "word_choice", "sentence", "naturalness", "clarity", "confidence"]
SCORE_LABELS = {
    "relevance": "Relevance",
    "clarity": "Clarity",
    "grammar": "Grammar",
    "word_choice": "Word choice",
    "sentence": "Sentence",
    "naturalness": "Naturalness",
    "confidence": "Confidence",
}

DIFFICULTY = {
    "de": "A relaxed, patient partner using simple language.",
    "vua": "A natural, encouraging partner with one thoughtful follow-up at a time.",
    "kho": "A quicker, more demanding but always respectful partner who asks specific follow-ups.",
}

# Conversation relevance guard: unrelated answers should be redirected, not graded.
TOPIC_KEYWORDS = {
    "cup": "coffee espresso americano mocha latte cappuccino tea drink beverage water milk cream sugar hot iced order menu receipt take go cup cafe",
    "map": "station train bus airport street road direction left right straight walk minutes corner ticket platform line downtown",
    "home": "neighbor apartment building move moved live food restaurant shop around recommend home neighborhood elevator floor",
    "phone": "call calling reservation booking hotel date change check in checkin available confirm name room cancel nights stay",
    "doctor": "doctor symptom sore throat fever pain sick medicine prescription allergy swallow health cough headache appointment clinic nurse treatment",
    "key": "apartment rent rental utilities deposit lease landlord move available room kitchen pets bathroom bedroom furnished",
    "plate": "restaurant order dish food menu allergy allergic ingredients peanuts sauce drink meal bill waiter server vegetarian vegan spicy",
    "globe": "travel traveler visitor city place visit local food recommend tourist transport arrive country museum beach downtown",
    "briefcase": "interview job role work experience project strength challenge team apply career",
    "spark": "meeting team launch plan idea suggest test timeline users results tradeoff work",
    "handshake": "event work study project designer colleague connect linkedin field introduce",
    "presentation": "present presentation idea problem solution impact proposal team project outline",
}
COMMON_CONVERSATION_WORDS = {
    "yes", "no", "sure", "okay", "ok", "please", "thanks", "thank", "could", "can", "would",
    "i", "we", "you", "he", "she", "they", "me", "my", "your", "our", "the", "a", "an", "it", "is",
    "are", "am", "was", "were", "be", "to", "for", "of", "in", "on", "at", "and", "or", "but",
    "that", "this", "there", "here", "what", "where", "when", "why", "how", "just", "really", "maybe", "also", "more", "less", "all", "any",
    "anything", "else", "fine", "good", "great", "nice", "perfect", "favorite", "delicious", "interesting",
}
BLOCKED_WORDS = {
    "fuck", "fucking", "motherfucker", "shit", "bullshit", "bitch", "bastard", "asshole", "dick", "cunt",
    "dit", "dich", "djt", "dm", "dmm", "du", "lon", "loz", "cac", "cặc", "địt", "đụ", "đm", "đmm",
}
SENTENCE_LINKING_WORDS = {
    "a", "an", "the", "my", "your", "our", "their", "this", "that", "for", "to", "from", "with",
    "about", "on", "in", "at", "since", "because", "if", "when", "and", "or", "but",
}
SENTENCE_STRUCTURE_WORDS = {
    "i", "you", "we", "he", "she", "they", "could", "can", "would", "should", "will", "have", "has", "had",
    "am", "is", "are", "do", "does", "did", "tell", "ask", "confirm", "need", "want", "like", "feel", "suggest",
    "propose", "recommend", "visit", "work", "explain", "change", "book", "order", "get", "please",
}
VALID_SENTENCE_PREFIXES = {
    ("i", "have"), ("i", "am"), ("i", "need"), ("i", "want"), ("i", "like"), ("i", "feel"),
    ("you", "should"), ("you", "can"), ("we", "could"), ("we", "should"), ("please", "confirm"),
    ("could", "you", "tell"), ("could", "you", "ask"),
}
SHORT_VALID_REPLIES = {"to go", "for here", "hot please", "iced please", "yes please", "no thanks", "that's all", "all good"}
UNIVERSAL_SHORT_REPLIES = {"yes", "no", "sure", "okay", "ok", "please", "thanks", "thank", "yes please", "no thanks", "that's all", "all good"}


def _tokens(text: str) -> set[str]:
    """Extract simple English words for the lightweight topic guard."""
    return set(re.findall(r"[a-z]+(?:'[a-z]+)?", (text or "").lower()))


def _ascii_tokens(text: str) -> set[str]:
    """Normalize accents for detecting profanity typed with Vietnamese diacritics."""
    normalized = unicodedata.normalize("NFKD", text or "")
    normalized = normalized.replace("đ", "d").replace("Đ", "D")
    plain = "".join(char for char in normalized if not unicodedata.combining(char))
    return set(re.findall(r"[a-z]+(?:'[a-z]+)?", plain.lower()))


def _has_blocked_language(text: str) -> bool:
    if any(char.isalpha() and not char.isascii() for char in (text or "")):
        return True
    return bool(_ascii_tokens(text) & {word for word in BLOCKED_WORDS if word.isascii()})


def _contains_profanity(text: str) -> bool:
    return bool(_ascii_tokens(text) & {word for word in BLOCKED_WORDS if word.isascii()})


def _topic_terms(scenario: dict) -> set[str]:
    source_text = " ".join(
        [
            TOPIC_KEYWORDS.get(scenario.get("icon", ""), ""),
            scenario.get("title", ""),
            scenario.get("context", ""),
            scenario.get("starter", ""),
            " ".join(scenario.get("vocabulary") or []),
        ]
    )
    # Remove conversational glue words so pronouns in a starter do not count
    # as evidence that an arbitrary sentence belongs to the scene.
    return _tokens(source_text) - COMMON_CONVERSATION_WORDS


def _looks_like_keyword_soup(scenario: dict, user_message: str) -> bool:
    """Catch topic words pasted in a list instead of a usable sentence."""
    words = re.findall(r"[a-z]+(?:[-'][a-z]+)*", (user_message or "").lower())
    if len(words) < 5:
        return False
    topic_terms = _topic_terms(scenario)
    topic_count = sum(1 for word in words if word in topic_terms or word.replace("-", "") in topic_terms)
    link_count = sum(1 for word in words if word in SENTENCE_LINKING_WORDS)
    structure_count = sum(1 for word in words if word in SENTENCE_STRUCTURE_WORDS)
    if topic_count < 4 or link_count > 1 or structure_count + link_count >= 4:
        return False
    for size in (2, 3):
        if tuple(words[:size]) in VALID_SENTENCE_PREFIXES:
            return False
    # A polite imperative such as "Please confirm ..." can be complete even
    # when it is short; otherwise a bare keyword list should not be scored.
    if len(words) == 5 and "please" in words:
        return False
    return True


def _has_repeated_chunks(words: list[str]) -> bool:
    """Detect repeated words or short phrases that indicate accidental spam."""
    if max(Counter(words).values(), default=0) >= 3:
        return True
    for size in (2, 3, 4):
        chunks = [tuple(words[index:index + size]) for index in range(len(words) - size + 1)]
        if any(count >= 2 for count in Counter(chunks).values()):
            return True
    return False


def _is_on_topic(scenario: dict, user_message: str, history: list[dict] | None = None) -> bool:
    return _guard_reason(scenario, user_message, history) is None


def _guard_reason(scenario: dict, user_message: str, history: list[dict] | None = None) -> str | None:
    """Return a stable reason when a reply should not be scored."""
    tokens = _tokens(user_message)
    if not tokens:
        return "incomplete"
    if _has_blocked_language(user_message):
        return "profanity" if _contains_profanity(user_message) else "language"

    topic_terms = _topic_terms(scenario)
    words = re.findall(r"[a-z]+(?:[-'][a-z]+)*", (user_message or "").lower())
    if len(words) >= 4 and _has_repeated_chunks(words):
        return "repeated"

    short_phrase = " ".join(re.findall(r"[a-z]+(?:'[a-z]+)?", user_message.lower()))
    if short_phrase in SHORT_VALID_REPLIES:
        return None if short_phrase in UNIVERSAL_SHORT_REPLIES or scenario.get("icon") == "cup" else "off_topic"
    # A short acknowledgement can naturally fit any scene ("sure", "no thanks").
    if tokens <= COMMON_CONVERSATION_WORDS:
        return None
    # A lone topic keyword ("reservation", "symptoms", "receipt") is not a
    # sentence and should not earn a grammar or conversation score. Keep only
    # a few genuinely useful two-word replies for role-play flow.
    if len(tokens) <= 2:
        return "incomplete"
    if _looks_like_keyword_soup(scenario, user_message):
        return "keyword_soup"
    # A closing move can be valid even when it has no scenario noun (for
    # example, "Thanks, that's all."). Check the active flow goal before
    # applying the broader topic-term guard.
    flow = scenarios.OFFLINE_FLOWS.get(scenario.get("icon"), {})
    goals = flow.get("goals", [])
    if goals:
        progress = 0
        for turn in (history or []):
            if not isinstance(turn, dict) or turn.get("role") != "user":
                continue
            while progress < len(goals) and _goal_matches(goals[progress], turn.get("text", "")):
                progress += 1
        if progress < len(goals) and _goal_matches(goals[progress], user_message):
            return None
    return None if tokens & topic_terms else "off_topic"


def _goal_matches(goal: dict, text: str) -> bool:
    words = _tokens(text)
    terms = set(str(goal.get("terms") or "").lower().split())
    return bool(words & terms)


def _conversation_state(scenario: dict, history: list[dict] | None = None, user_message: str = "") -> dict:
    """Track sequential conversation moves while allowing one message to cover several moves."""
    flow = scenarios.OFFLINE_FLOWS.get(scenario.get("icon"), {})
    goals = flow.get("goals", [])
    prior_messages = [
        turn.get("text", "")
        for turn in (history or [])
        if isinstance(turn, dict) and turn.get("role") == "user"
    ]
    before = 0
    for message in prior_messages:
        while before < len(goals) and _goal_matches(goals[before], message):
            before += 1
    completed = before
    if user_message:
        while completed < len(goals) and _goal_matches(goals[completed], user_message):
            completed += 1
    total = len(goals)
    finished = bool(total and completed >= total)
    if user_message and completed > before:
        reply = goals[completed - 1].get("reply", "")
    elif finished:
        reply = goals[-1].get("reply", "")
    elif goals:
        reply = goals[completed].get("nudge", "")
    else:
        reply = "Keep the conversation moving with one clear sentence."
    return {
        "goals": [
            {"id": goal.get("id", f"goal-{index}"), "label": goal.get("label", "Conversation step"), "complete": index < completed}
            for index, goal in enumerate(goals)
        ],
        "completed": completed,
        "total": total,
        "task_score": round((completed / total) * 10, 1) if total else 0,
        "next_goal": None if finished else (goals[completed].get("label") if completed < total else None),
        "done": finished,
        "reply": reply,
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
Conversation moves to guide naturally: {', '.join(goal['label'] for goal in scenarios.OFFLINE_FLOWS.get(scenario.get('icon'), {}).get('goals', []))}

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
  - Score relevance, grammar, word_choice, sentence, naturalness, clarity, and confidence from 0 to 10.
  - If the learner's message is invalid for this practice, set `off_topic` and `scored` to true/false respectively, set `guard_reason` to one of `off_topic`, `incomplete`, `repeated`, `keyword_soup`, `profanity`, or `language`, leave `improved` empty, and ask them to try again. Do not award a score.
- Set done true after 4-7 learner turns when the scenario has a satisfying close.
- Include `conversation` with completed move ids, a 0-10 `task_score`, the next goal, and `done`.

Return valid JSON only:
{{"reply":"...", "feedback":"...", "improved":"...", "tip":"...", "grammar_note":"...", "word_choice_note":"...", "sentence_pattern":"...", "scores":{{"relevance":0,"grammar":0,"word_choice":0,"sentence":0,"naturalness":0,"clarity":0,"confidence":0}}, "scored":true, "off_topic":false, "guard_reason":null, "conversation":{{"completed":0,"total":4,"task_score":0,"next_goal":"...","done":false}}, "done":false}}"""


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
        # Guard the request before calling the model so an off-topic answer can
        # never receive a score, even when the model is online.
        guard_reason = _guard_reason(scenario, user_message, history)
        if guard_reason:
            return self._off_topic_response(
                scenario, english_only, reason=guard_reason, mode="guard",
                conversation=_conversation_state(scenario, history),
            )
        if self.online:
            try:
                result = self._respond_ai(level, scenario, difficulty, history, user_message, learner, english_only)
                conversation = _conversation_state(scenario, history, user_message)
                return _normalize(
                    {**result, "conversation": conversation, "done": conversation["done"]},
                    mode="ai",
                )
            except Exception as exc:  # pragma: no cover - external service
                print(f"[WARN] Gemini request failed; using offline mode: {exc}")
        return self._respond_offline(scenario, history, user_message, learner, english_only)

    def _off_topic_response(self, scenario, english_only, reason="off_topic", mode="offline", conversation=None):
        language = "English" if english_only else "Vietnamese"
        messages = {
            "off_topic": (
                "That answer does not match this situation yet, so I will not score it.",
                "Mình chưa chấm điểm vì câu trả lời chưa đúng tình huống.",
            ),
            "incomplete": (
                "That is not a complete sentence yet, so I will not score it.",
                "Mình chưa chấm điểm vì câu này chưa phải một câu hoàn chỉnh.",
            ),
            "repeated": (
                "The same word or phrase is repeated too much, so I will not score it.",
                "Mình chưa chấm điểm vì bạn đang lặp lại từ hoặc cụm từ quá nhiều.",
            ),
            "keyword_soup": (
                "These words fit the scene, but they are not arranged as a clear sentence, so I will not score it.",
                "Các từ có liên quan nhưng chưa được sắp xếp thành câu rõ ràng nên mình chưa chấm điểm.",
            ),
            "profanity": (
                "Please keep the practice respectful; I will not score that reply.",
                "Hãy giữ nội dung luyện tập lịch sự; mình chưa chấm điểm câu này.",
            ),
            "language": (
                "Please answer in English for this scene; I will not score this reply.",
                "Hãy trả lời bằng tiếng Anh trong tình huống này; mình chưa chấm điểm câu này.",
            ),
        }
        english_message, vietnamese_message = messages.get(reason, messages["off_topic"])
        if language == "English":
            feedback = english_message
            reply = "Let's stay with this scene. Please try one complete English sentence using the situation details."
            tip = f"Try: \u201c{scenario['starter']}\u201d"
            grammar_note = "We will check grammar after your answer is clear and on topic."
            word_choice_note = "Use words connected to this situation."
        else:
            feedback = vietnamese_message
            reply = "Mình tiếp tục tình huống này nhé. Hãy thử một câu tiếng Anh hoàn chỉnh dựa trên bối cảnh."
            tip = f"Bạn có thể bắt đầu: \u201c{scenario['starter']}\u201d"
            grammar_note = "Khi câu trả lời rõ ràng và đúng chủ đề, mình sẽ kiểm tra ngữ pháp."
            word_choice_note = "Hãy dùng từ liên quan đến tình huống này."
        return _normalize(
            {
                "reply": reply,
                "feedback": feedback,
                "improved": "",
                "tip": tip,
                "grammar_note": grammar_note,
                "word_choice_note": word_choice_note,
                "sentence_pattern": scenario.get("starter", ""),
                "scores": {},
                "scored": False,
                "off_topic": True,
                "guard_reason": reason,
                "conversation": conversation,
                "done": False,
            },
            mode=mode,
        )

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
        guard_reason = _guard_reason(scenario, user_message, history)
        if guard_reason:
            return self._off_topic_response(
                scenario, english_only, reason=guard_reason, mode="offline",
                conversation=_conversation_state(scenario, history),
            )
        conversation = _conversation_state(scenario, history, user_message)
        reply = conversation["reply"]
        if not reply:
            user_turns = sum(turn.get("role") == "user" for turn in history)
            replies = scenario.get("offline_replies", [])
            reply = replies[user_turns % len(replies)] if replies else "Keep the conversation moving with one clear sentence."
        done = conversation["done"]
        scores, feedback, improved, tip, grammar_note, word_choice_note, sentence_pattern = _review_offline(
            user_message, scenario, learner, english_only
        )
        return _normalize(
            {
                "reply": reply,
                "feedback": feedback,
                "improved": improved,
                "tip": tip,
                "grammar_note": grammar_note,
                "word_choice_note": word_choice_note,
                "sentence_pattern": sentence_pattern,
                "scores": scores,
                "done": done,
                "scored": True,
                "off_topic": False,
                "conversation": conversation,
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


def _normalize_conversation(data) -> dict | None:
    if not isinstance(data, dict):
        return None
    raw_goals = data.get("goals") if isinstance(data.get("goals"), list) else []
    goals = []
    for index, goal in enumerate(raw_goals[:8]):
        if not isinstance(goal, dict):
            continue
        goal_id = str(goal.get("id") or f"goal-{index}").strip()[:40]
        label = str(goal.get("label") or "Conversation step").strip()[:100]
        if goal_id and label:
            goals.append({"id": goal_id, "label": label, "complete": bool(goal.get("complete", False))})
    try:
        total = max(0, min(8, int(data.get("total", len(goals)))))
    except (TypeError, ValueError):
        total = len(goals)
    try:
        completed = max(0, min(total, int(data.get("completed", 0))))
    except (TypeError, ValueError):
        completed = sum(goal["complete"] for goal in goals)
    try:
        task_score = round(max(0, min(10, float(data.get("task_score", 0)))), 1)
    except (TypeError, ValueError):
        task_score = round((completed / total) * 10, 1) if total else 0
    return {
        "goals": goals,
        "completed": completed,
        "total": total,
        "task_score": task_score,
        "next_goal": str(data.get("next_goal") or "").strip()[:100] or None,
        "done": bool(data.get("done", False)),
    }


def _normalize(data: dict, mode: str) -> dict:
    raw_scores = data.get("scores") or {}
    scored = bool(data.get("scored", True)) and not bool(data.get("off_topic", False))
    scores = {key: _clamp_score(raw_scores.get(key, 5)) for key in SCORE_KEYS} if scored else {}
    guard_reason = str(data.get("guard_reason") or "").strip() or ("off_topic" if not scored and data.get("off_topic") else None)
    conversation = _normalize_conversation(data.get("conversation"))
    return {
        "reply": str(data.get("reply") or "...").strip(),
        "feedback": str(data.get("feedback") or "").strip(),
        "improved": str(data.get("improved") or "").strip(),
        "tip": str(data.get("tip") or "").strip(),
        "grammar_note": str(data.get("grammar_note") or "").strip(),
        "word_choice_note": str(data.get("word_choice_note") or "").strip(),
        "sentence_pattern": str(data.get("sentence_pattern") or "").strip(),
        "scores": scores,
        "overall": round(sum(scores.values()) / len(scores), 1) if scores else None,
        "scored": scored,
        "off_topic": bool(data.get("off_topic", False)),
        "guard_reason": guard_reason,
        "conversation": conversation,
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


OFFLINE_SUBJECT_WORDS = {"i", "you", "we", "he", "she", "they", "it", "there"}
OFFLINE_VERB_WORDS = {
    "am", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did",
    "can", "could", "will", "would", "should", "must", "need", "want", "like", "love", "feel", "go",
    "get", "order", "ask", "tell", "confirm", "change", "book", "reserve", "recommend", "suggest",
    "propose", "visit", "work", "explain", "make", "take", "know", "think", "call", "live", "move", "drink", "choose",
}


def _offline_sentence_metrics(text: str) -> dict:
    """Estimate basic parts of a sentence without downloading a language model."""
    tokens = re.findall(r"[a-z]+(?:[-'][a-z]+)*", (text or "").lower())
    plain_tokens = {token.replace("-", "") for token in tokens}
    return {
        "words": len(tokens),
        "has_subject": bool(plain_tokens & OFFLINE_SUBJECT_WORDS),
        "has_verb": bool(plain_tokens & OFFLINE_VERB_WORDS),
        "has_linker": bool(plain_tokens & SENTENCE_LINKING_WORDS),
        "has_terminal": bool(re.search(r"[?.!]$", (text or "").strip())),
        "is_question": bool(re.search(r"[?]$", (text or "").strip())),
    }


def _review_offline(message: str, scenario: dict, learner: dict, english_only: bool):
    """Give a focused local correction so the app stays useful without an API key."""
    text = message.strip()
    lower = text.lower()
    metrics = _offline_sentence_metrics(text)
    words = metrics["words"]
    scores = {
        "relevance": 10,
        "grammar": 8,
        "word_choice": 8,
        "sentence": 7,
        "naturalness": 7,
        "clarity": 7,
        "confidence": 7,
    }
    feedback = "Your meaning is clear. Keep the conversation moving." if english_only else "Ý của bạn rõ ràng, cứ tiếp tục giữ nhịp hội thoại nhé."
    improved = ""
    tip = f"Try: “{scenario['starter']}”" if english_only else f"Bạn có thể dùng: “{scenario['starter']}”"
    grammar_note = "Grammar looks okay." if english_only else "Ngữ pháp hiện tại ổn."
    word_choice_note = "Your word choice is understandable." if english_only else "Từ bạn chọn vẫn dễ hiểu."
    sentence_pattern = scenario.get("starter", "")

    fixes = [
        (r"\b(can|could|should|must|will)\s+to\s+([a-z]+)", r"\1 \2", "grammar", "After a modal verb, use the base verb without 'to'." if english_only else "Sau động từ khuyết thiếu dùng động từ nguyên mẫu, không thêm ‘to’.", "Can / Could / Should + base verb ..."),
        (r"\b(he|she|it)\s+have\b", r"\1 has", "grammar", "Use 'has' with he, she, and it." if english_only else "Với he, she, it dùng ‘has’, không dùng ‘have’.", "He / She / It has + noun."),
        (r"\b(i|you|we|they)\s+has\b", r"\1 have", "grammar", "Use 'have' with I, you, we, and they." if english_only else "Với I, you, we, they dùng ‘have’, không dùng ‘has’.", "I / You / We / They have + noun."),
        (r"\ba\s+(hour|honest|honor|heir|herb)\b", r"an \1", "grammar", "Use 'an' before a silent-h word." if english_only else "Dùng ‘an’ trước một số từ có âm h câm.", "an hour / an honest answer."),
        (r"\ban\s+(university|user|usual|european|one|once)\b", r"a \1", "grammar", "Use 'a' before a consonant sound, even when the word starts with a vowel letter." if english_only else "Dùng ‘a’ trước âm phụ âm dù từ bắt đầu bằng nguyên âm.", "a university / a useful idea."),
        (r"\ba\s+([aeiou][a-z]+)\b", r"an \1", "grammar", "Use 'an' before a vowel sound." if english_only else "Dùng ‘an’ trước âm nguyên âm.", "an + vowel sound."),
        (r"\ban\s+([bcdfghjklmnpqrstvwxyz][a-z]+)\b", r"a \1", "grammar", "Use 'a' before a consonant sound." if english_only else "Dùng ‘a’ trước âm phụ âm.", "a + consonant sound."),
        (r"\binterested on\b", "interested in", "grammar", "The correct preposition is 'in' after 'interested'." if english_only else "Sau ‘interested’ dùng giới từ ‘in’.", "be interested in + noun / verb-ing."),
        (r"\bgood in\b", "good at", "grammar", "Use 'good at' for a skill." if english_only else "Nói về kỹ năng dùng ‘good at’.", "be good at + noun / verb-ing."),
        (r"\barrive to\b", "arrive at", "grammar", "Use 'arrive at' for a specific place." if english_only else "Dùng ‘arrive at’ với địa điểm cụ thể.", "arrive at + place."),
        (r"\bmarried with\b", "married to", "grammar", "The usual phrase is 'married to'." if english_only else "Cụm tự nhiên là ‘married to’.", "be married to + person."),
        (r"\blisten\s+(music|the radio|this)", r"listen to \1", "grammar", "Use 'listen to' before the thing you hear." if english_only else "Dùng ‘listen to’ trước thứ bạn nghe.", "listen to + noun."),
        (r"\b(how)\s+much\s+people\b", lambda match: f"{match.group(1)} many people", "grammar", "Use 'many' with countable people." if english_only else "Dùng ‘how many’ với danh từ đếm được như people.", "How many + plural noun ...?"),
        (r"\badvices\b", "advice", "grammar", "'Advice' is uncountable and has no plural -s." if english_only else "‘Advice’ là danh từ không đếm được, không thêm -s.", "some advice / a piece of advice."),
        (r"\bpeoples\b", "people", "grammar", "Use 'people' as the plural of person." if english_only else "Dạng số nhiều của person là ‘people’.", "many people."),
        (r"\bchildrens\b", "children", "grammar", "The plural of 'child' is 'children'." if english_only else "Số nhiều của ‘child’ là ‘children’.", "children + verb."),
        (r"\bcriterias\b", "criteria", "grammar", "The plural of 'criterion' is 'criteria'." if english_only else "Số nhiều của ‘criterion’ là ‘criteria’.", "the criteria are ..."),
        (r"^\s*(what|where|when|why|how)\s+you\s+(are|is|do|does|did|can|could|will|would)\b", lambda match: f"{match.group(1)} {match.group(2)} you", "grammar", "In a direct question, put the helping verb before 'you'." if english_only else "Trong câu hỏi trực tiếp, đưa trợ động từ lên trước ‘you’.", "What / Where / Why + auxiliary + subject ...?"),
        (r"\b(i need|i want|i have)\s+(?!(?:a|an)\s+)(reservation|ticket|room|table|meeting|appointment|interview|hotel|station|doctor|symptom|question|recommendation|project|plan|solution|problem|job|apartment|deposit|lease|dish)\b", lambda match: f"{match.group(1)} {('an' if match.group(2)[0].lower() in 'aeiou' else 'a')} {match.group(2)}", "grammar", "Use an article before this singular countable noun." if english_only else "Cần dùng mạo từ trước danh từ đếm được số ít này.", "I need a / an + singular noun."),
        (r"\bi want\b", "I'd like", "word", "'I want' is grammatically correct, but 'I'd like' is more polite here." if english_only else "‘I want’ đúng ngữ pháp nhưng khá trực tiếp; dùng ‘I’d like’ lịch sự hơn trong tình huống này.", "Use I'd like + noun / to + verb."),
        (r"\bi am agree\b", "I agree", "grammar", "Say 'I agree' - no 'am' is needed." if english_only else "Sau ‘I’ không cần dùng ‘am’ trước ‘agree’.", "I + agree / disagree + with + person."),
        (r"\bi very like\b", "I really like", "word", "Use 'really' before the verb, not 'very'." if english_only else "Dùng ‘really’ trước động từ sẽ tự nhiên hơn ‘very’.", "I really like + noun / verb-ing."),
        (r"\bcan you to\b", "Can you", "grammar", "After 'can', use the base verb without 'to'." if english_only else "Sau ‘can’ dùng động từ nguyên mẫu, không dùng ‘to’.", "Can you + base verb ...?"),
        (r"\bi have (\d+) years old\b", r"I am \1 years old", "grammar", "Use 'be', not 'have', for age." if english_only else "Khi nói tuổi dùng ‘be’, không dùng ‘have’.", "I am + number + years old."),
        (r"\bi am boring\b", "I am bored", "word", "Use 'bored' for your feeling; 'boring' describes something that causes it." if english_only else "Dùng ‘bored’ cho cảm xúc của bạn; ‘boring’ mô tả thứ làm bạn chán.", "I am bored because ... / It is boring."),
        (r"\bi(?:'m| am) interest\b", "I am interested", "grammar", "Use the adjective 'interested' after 'I am'." if english_only else "Sau ‘I am’ dùng tính từ ‘interested’.", "I am interested in + noun / verb-ing."),
        (r"\bi(?:'d| would) like go\b", "I'd like to go", "grammar", "Use 'to' after 'would like'." if english_only else "Sau ‘would like’ cần có ‘to’ trước động từ.", "I'd like to + base verb."),
        (r"\b(he|she|it) don't\b", r"\1 doesn't", "grammar", "Use 'doesn't' with he, she, and it." if english_only else "Với he, she, it dùng ‘doesn’t’, không dùng ‘don’t’.", "He / She / It doesn't + base verb."),
        (r"\bi didn't went\b", "I didn't go", "grammar", "After 'didn't', use the base verb 'go'." if english_only else "Sau ‘didn’t’ dùng động từ nguyên mẫu ‘go’.", "I didn't + base verb."),
        (r"\bpeople is\b", "People are", "grammar", "'People' is plural, so use 'are'." if english_only else "‘People’ là số nhiều nên dùng ‘are’.", "People are + adjective / verb-ing."),
        (r"\bdiscuss about\b", "discuss", "grammar", "'Discuss' already includes the meaning of 'about'." if english_only else "‘Discuss’ đã mang nghĩa ‘thảo luận về’, không cần thêm ‘about’.", "Discuss + topic."),
        (r"\bexplain me\b", "explain it to me", "grammar", "Use 'explain something to someone'." if english_only else "Dùng cấu trúc ‘explain something to someone’.", "Could you explain + it / this + to me?"),
        (r"\bdepend of\b", "depend on", "grammar", "The correct preposition is 'on'." if english_only else "Giới từ đúng sau ‘depend’ là ‘on’.", "It depends on + noun / question word."),
        (r"\bgo to there\b", "go there", "grammar", "Do not use 'to' before 'there'." if english_only else "Không dùng ‘to’ trước ‘there’.", "Go there / come here."),
        (r"\bmore better\b", "better", "grammar", "'Better' is already comparative, so do not add 'more'." if english_only else "‘Better’ đã là so sánh hơn nên không thêm ‘more’.", "This option is better than ..."),
        (r"\binformations\b", "information", "grammar", "'Information' is uncountable, so it has no plural -s." if english_only else "‘Information’ là danh từ không đếm được nên không thêm -s.", "Some information / a piece of information."),
    ]
    for pattern, replacement, focus, note, pattern_tip in fixes:
        if re.search(pattern, lower):
            improved = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            feedback = note
            scores["grammar" if focus == "grammar" else "word_choice"] = 5
            scores["sentence"] = 5
            scores["naturalness"] = 5
            tip = f"Try: “{improved}”" if english_only else f"Thử nói: “{improved}”"
            grammar_note = note if focus == "grammar" else ("Grammar is okay; the wording is the key improvement." if english_only else "Ngữ pháp vẫn ổn; điểm cần cải thiện chính là cách dùng từ.")
            word_choice_note = note if focus == "word" else ("This correction makes the sentence more natural." if english_only else "Sửa như vậy giúp câu tự nhiên hơn.")
            sentence_pattern = pattern_tip
            break
    else:
        if words < 4:
            feedback = "Your reply is a little short, so it is harder to build a real conversation." if english_only else "Câu trả lời hơi ngắn, nên khó tạo phản xạ hội thoại."
            scores["clarity"] = 4
            scores["confidence"] = 5
            scores["sentence"] = 4
            tip = "Add one detail or a question: “Could you tell me more?”" if english_only else "Thêm một chi tiết hoặc một câu hỏi: “Could you tell me more?”"
            sentence_pattern = "Add one detail + one follow-up question."
        elif not metrics["has_verb"]:
            feedback = "I can see the topic, but this needs a verb to become a complete sentence." if english_only else "Mình thấy đúng chủ đề, nhưng câu cần có động từ để hoàn chỉnh."
            scores["grammar"] = 5
            scores["sentence"] = 4
            scores["clarity"] = 5
            grammar_note = "Add a clear verb after the subject." if english_only else "Thêm một động từ rõ ràng sau chủ ngữ."
            sentence_pattern = "Subject + verb + detail."
            tip = "Try: “I would like ...”" if english_only else "Thử nói: “I would like ...”"
        elif not metrics["has_subject"] and not re.match(r"\s*(please\s+)?(?:can|could|would|should|tell|ask|confirm|order|recommend|suggest|propose|explain|change|book)\b", lower):
            feedback = "Your words are related, but add a subject so the sentence is easier to follow." if english_only else "Các từ đúng chủ đề, nhưng nên thêm chủ ngữ để câu dễ hiểu hơn."
            scores["grammar"] = 6
            scores["sentence"] = 5
            scores["clarity"] = 5
            grammar_note = "Use a subject + verb structure." if english_only else "Dùng cấu trúc chủ ngữ + động từ."
            sentence_pattern = "Subject + verb + detail."
        elif not re.search(r"[?.!]$", text):
            feedback = "Your sentence is clear. Let your voice fall at the end so it sounds complete." if english_only else "Câu của bạn dễ hiểu. Khi nói, hãy hạ giọng ở cuối câu để nghe trọn ý hơn."
            scores["sentence"] = 6
        elif "please" in lower or "could" in lower:
            feedback = "Very good - your wording is polite and natural." if english_only else "Rất tốt - bạn dùng cách nói lịch sự và tự nhiên."
            scores["naturalness"] = 8
            scores["confidence"] = 8

    return scores, feedback, improved, tip, grammar_note, word_choice_note, sentence_pattern


def review_sentence_exercise(message: str, exercise: dict, english_only: bool = False) -> dict:
    """Review a free sentence against a Vietnamese context prompt offline."""
    text = (message or "").strip()
    exercise = exercise if isinstance(exercise, dict) else {}
    public_exercise = {
        "id": str(exercise.get("id") or "").strip()[:60],
        "level": str(exercise.get("level") or "A2").strip()[:20],
        "prompt": str(exercise.get("prompt") or "").strip()[:240],
        "situation": str(exercise.get("situation") or "").strip()[:240],
        "focus": str(exercise.get("focus") or "").strip()[:100],
        "hint_en": str(exercise.get("hint_en") or "").strip()[:120],
    }
    if not text:
        result = _normalize(
            {
                "reply": "Write one English sentence for this prompt.",
                "feedback": "Hãy viết một câu tiếng Anh trước khi mình sửa nhé.",
                "scores": {},
                "scored": False,
                "off_topic": True,
                "guard_reason": "incomplete",
                "done": False,
            },
            mode="offline",
        )
        result["exercise"] = public_exercise
        return result
    if _has_blocked_language(text):
        feedback = "Please write your answer in English so I can correct the sentence." if english_only else "Hãy viết câu trả lời bằng tiếng Anh để mình sửa câu nhé."
        result = _normalize(
            {
                "reply": "Try the same idea in English.",
                "feedback": feedback,
                "scores": {},
                "scored": False,
                "off_topic": True,
                "guard_reason": "language",
                "done": False,
            },
            mode="offline",
        )
        result["exercise"] = public_exercise
        return result

    scenario = {
        "title": public_exercise["id"] or "Sentence exercise",
        "context": public_exercise["prompt"],
        "starter": public_exercise["hint_en"] or "Write one clear sentence.",
    }
    scores, feedback, improved, tip, grammar_note, word_choice_note, sentence_pattern = _review_offline(
        text, scenario, {}, english_only
    )
    result = _normalize(
        {
            "reply": "Good attempt. Compare your sentence with the improved version below.",
            "feedback": feedback,
            "improved": improved,
            "tip": tip,
            "grammar_note": grammar_note,
            "word_choice_note": word_choice_note,
            "sentence_pattern": sentence_pattern,
            "scores": scores,
            "scored": True,
            "off_topic": False,
            "guard_reason": None,
            "done": False,
        },
        mode="offline",
    )
    result["exercise"] = public_exercise
    result["saved_to_notebook"] = bool(improved and improved.strip().lower() != text.lower())
    return result
