"""Small SQLite persistence layer for TalkMate accounts and sync data."""
from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import config


MAX_COMPLETED = 100
MAX_ACTIVE_DAYS = 365
MAX_SCORE_EVENTS = 30
MAX_REVIEW_ITEMS = 20
MAX_REVIEW_DAYS = 365
MAX_XP_EVENTS = 500
MAX_CHALLENGE_EVENTS = 100_000


def _limited_strings(value, limit: int, item_limit: int):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if not isinstance(item, str):
            continue
        item = item.strip()[:item_limit]
        if item and item not in result:
            result.append(item)
        if len(result) >= limit:
            break
    return result


def _score(value):
    try:
        return round(max(0, min(10, float(value))), 1)
    except (TypeError, ValueError):
        return None


def _event_list(value, limit: int, amount_key: str, maximum: int):
    if not isinstance(value, list):
        return []
    result = []
    seen = set()
    for event in value:
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("id") or "").strip()[:100]
        try:
            amount = int(event.get(amount_key))
        except (TypeError, ValueError):
            continue
        if not event_id or event_id in seen or amount <= 0:
            continue
        result.append({"id": event_id, amount_key: min(maximum, amount), "at": str(event.get("at") or "")[:40]})
        seen.add(event_id)
        if len(result) >= limit:
            break
    return result


def normalize_progress(payload):
    """Keep synced progress bounded and compatible with older browser data."""
    payload = payload if isinstance(payload, dict) else {}
    completed = _limited_strings(payload.get("completed"), MAX_COMPLETED, 100)
    active_days = _limited_strings(payload.get("activeDays"), MAX_ACTIVE_DAYS, 20)
    raw_scores = payload.get("scores") if isinstance(payload.get("scores"), list) else []
    scores = [score for value in raw_scores if (score := _score(value)) is not None][-MAX_SCORE_EVENTS:]

    score_events = []
    raw_events = payload.get("scoreEvents") if isinstance(payload.get("scoreEvents"), list) else []
    for index, event in enumerate(raw_events):
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("id") or "").strip()[:100]
        score = _score(event.get("score"))
        if not event_id or score is None or any(item["id"] == event_id for item in score_events):
            continue
        score_events.append({"id": event_id, "score": score, "at": str(event.get("at") or "")[:40]})
        if len(score_events) >= MAX_SCORE_EVENTS:
            break
    if not score_events:
        score_events = [
            {"id": f"legacy-{index}-{score}", "score": score, "at": ""}
            for index, score in enumerate(scores)
        ]
    score_events = score_events[-MAX_SCORE_EVENTS:]

    raw_momentum = payload.get("momentum") if isinstance(payload.get("momentum"), dict) else {}
    daily_minutes = {}
    if isinstance(raw_momentum.get("dailyMinutes"), dict):
        for day, minutes in raw_momentum["dailyMinutes"].items():
            if not isinstance(day, str) or not re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", day):
                continue
            try:
                daily_minutes[day] = round(max(0, min(5, float(minutes))), 1)
            except (TypeError, ValueError):
                continue
            if len(daily_minutes) >= MAX_ACTIVE_DAYS:
                break
    xp_events = _event_list(raw_momentum.get("xpEvents"), MAX_XP_EVENTS, "amount", 1_000)
    if not xp_events:
        try:
            legacy_xp = max(0, min(1_000_000, int(raw_momentum.get("xp", 0))))
        except (TypeError, ValueError):
            legacy_xp = 0
        if legacy_xp:
            xp_events = [{"id": "legacy-xp", "amount": legacy_xp, "at": ""}]
    challenge_events = _event_list(raw_momentum.get("challengeEvents"), MAX_CHALLENGE_EVENTS, "amount", 1_000)
    if not challenge_events:
        try:
            legacy_challenges = max(0, min(100_000, int(raw_momentum.get("challenges", 0))))
        except (TypeError, ValueError):
            legacy_challenges = 0
        if legacy_challenges:
            challenge_events = [{"id": "legacy-challenges", "amount": legacy_challenges, "at": ""}]
    momentum = {
        "xp": min(1_000_000, sum(event["amount"] for event in xp_events)),
        "xpEvents": xp_events,
        "badges": _limited_strings(raw_momentum.get("badges"), 50, 60),
        "dailyMinutes": daily_minutes,
        "challenges": min(100_000, sum(event["amount"] for event in challenge_events)),
        "challengeEvents": challenge_events,
    }

    raw_profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
    def counters(name):
        values = raw_profile.get(name) if isinstance(raw_profile.get(name), dict) else {}
        result = {}
        for key, value in values.items():
            if not isinstance(key, str) or not key.strip() or len(result) >= 30:
                continue
            try:
                result[key.strip()[:90]] = max(0, min(10_000, int(value)))
            except (TypeError, ValueError):
                continue
        return result
    profile = {
        "goal": str(raw_profile.get("goal") or "")[:180],
        "proficiency": str(raw_profile.get("proficiency") or "A2")[:10],
        "target": str(raw_profile.get("target") or "travel")[:50],
        "englishOnly": bool(raw_profile.get("englishOnly", False)),
        "errors": counters("errors"),
        "strengths": counters("strengths"),
    }

    review_items = []
    raw_reviews = payload.get("reviewItems") if isinstance(payload.get("reviewItems"), list) else []
    for item in raw_reviews:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source") or "").strip()[:600]
        correction = str(item.get("correction") or "").strip()[:600]
        if not source or not correction:
            continue
        key = (source.lower(), correction.lower())
        if any((entry["source"].lower(), entry["correction"].lower()) == key for entry in review_items):
            continue
        review_items.append({
            "id": str(item.get("id") or f"legacy-review-{len(review_items)}")[:100],
            "source": source,
            "correction": correction,
            "note": str(item.get("note") or "")[:600],
            "tag": str(item.get("tag") or "PERSONAL FIX")[:60],
            "category": str(item.get("category") or "word_choice")[:40],
            "exercise": str(item.get("exercise") or "Rewrite this sentence in natural English.")[:300],
            "level": str(item.get("level") or "A2")[:10],
            "target": str(item.get("target") or "practice")[:50],
            "attempts": max(0, min(10_000, int(item.get("attempts") or 0))) if str(item.get("attempts") or "0").lstrip("-").isdigit() else 0,
            "correct": max(0, min(10_000, int(item.get("correct") or 0))) if str(item.get("correct") or "0").lstrip("-").isdigit() else 0,
            "lastReviewedDay": str(item.get("lastReviewedDay") or "")[:20],
            "createdAt": str(item.get("createdAt") or "")[:40],
        })
        if len(review_items) >= MAX_REVIEW_ITEMS:
            break

    raw_review = payload.get("review") if isinstance(payload.get("review"), dict) else {}
    review_daily = {}
    if isinstance(raw_review.get("dailyCompleted"), dict):
        for day, count in raw_review["dailyCompleted"].items():
            if not isinstance(day, str) or not re.fullmatch(r"\d{4}-\d{1,2}-\d{1,2}", day):
                continue
            try:
                review_daily[day] = max(0, min(5, int(count)))
            except (TypeError, ValueError):
                continue
            if len(review_daily) >= MAX_REVIEW_DAYS:
                break
    def bounded_review_count(name):
        try:
            return max(0, min(1_000_000, int(raw_review.get(name) or 0)))
        except (TypeError, ValueError):
            return 0
    review = {
        "dailyCompleted": review_daily,
        "sessions": bounded_review_count("sessions"),
        "attempts": bounded_review_count("attempts"),
        "correct": bounded_review_count("correct"),
    }

    return {
        "completed": completed,
        "scores": [event["score"] for event in score_events],
        "scoreEvents": score_events,
        "activeDays": active_days,
        "momentum": momentum,
        "profile": profile,
        "profile_updated_at": str(payload.get("profile_updated_at") or "")[:40],
        "reviewItems": review_items,
        "review": review,
    }


def merge_progress(existing, incoming):
    """Merge independent device snapshots without letting an old snapshot erase work."""
    existing = normalize_progress(existing)
    incoming = normalize_progress(incoming)

    def unique(items, limit):
        result = []
        for item in [*items[0], *items[1]]:
            if item not in result:
                result.append(item)
        return result[-limit:]

    merged = {
        "completed": unique((existing["completed"], incoming["completed"]), MAX_COMPLETED),
        "activeDays": unique((existing["activeDays"], incoming["activeDays"]), MAX_ACTIVE_DAYS),
    }
    events = {event["id"]: event for event in existing["scoreEvents"]}
    events.update({event["id"]: event for event in incoming["scoreEvents"]})
    merged_events = sorted(events.values(), key=lambda event: (event["at"], event["id"]))[-MAX_SCORE_EVENTS:]
    merged["scoreEvents"] = merged_events
    merged["scores"] = [event["score"] for event in merged_events]

    base_momentum = existing["momentum"]
    next_momentum = incoming["momentum"]
    daily_minutes = dict(base_momentum["dailyMinutes"])
    for day, minutes in next_momentum["dailyMinutes"].items():
        daily_minutes[day] = max(daily_minutes.get(day, 0), minutes)
    def merged_events(base_events, next_events, amount_key, limit, maximum):
        events = {event["id"]: event for event in base_events}
        for event in next_events:
            previous = events.get(event["id"])
            if not previous or event[amount_key] > previous[amount_key]:
                events[event["id"]] = event
        return sorted(events.values(), key=lambda event: (event["at"], event["id"]))[-limit:]

    xp_events = merged_events(base_momentum["xpEvents"], next_momentum["xpEvents"], "amount", MAX_XP_EVENTS, 1_000_000)
    challenge_events = merged_events(
        base_momentum["challengeEvents"], next_momentum["challengeEvents"], "amount", MAX_CHALLENGE_EVENTS, 100_000
    )
    merged["momentum"] = {
        "xp": min(1_000_000, sum(event["amount"] for event in xp_events)),
        "xpEvents": xp_events,
        "badges": unique((base_momentum["badges"], next_momentum["badges"]), 50),
        "dailyMinutes": dict(list(daily_minutes.items())[-MAX_ACTIVE_DAYS:]),
        "challenges": min(100_000, sum(event["amount"] for event in challenge_events)),
        "challengeEvents": challenge_events,
    }

    profile_from_incoming = bool(
        incoming["profile_updated_at"]
        and (
            not existing["profile_updated_at"]
            or incoming["profile_updated_at"] > existing["profile_updated_at"]
        )
    )
    selected_profile = incoming if profile_from_incoming else existing
    profile = dict(selected_profile["profile"])
    for field in ("errors", "strengths"):
        counters = dict(existing["profile"][field])
        for key, value in incoming["profile"][field].items():
            counters[key] = max(counters.get(key, 0), value)
        profile[field] = counters
    merged["profile"] = profile
    merged["profile_updated_at"] = selected_profile["profile_updated_at"]

    merged_reviews = []
    review_lookup = {}
    for item in [*existing["reviewItems"], *incoming["reviewItems"]]:
        key = (item["source"].lower(), item["correction"].lower())
        previous = review_lookup.get(key)
        if previous is None:
            review_lookup[key] = dict(item)
            merged_reviews.append(review_lookup[key])
            continue
        previous["attempts"] = max(previous["attempts"], item["attempts"])
        previous["correct"] = max(previous["correct"], item["correct"])
        if item.get("lastReviewedDay") > previous.get("lastReviewedDay", ""):
            previous["lastReviewedDay"] = item["lastReviewedDay"]
        for field in ("id", "note", "tag", "category", "exercise", "level", "target", "createdAt"):
            if not previous.get(field) and item.get(field):
                previous[field] = item[field]
    merged["reviewItems"] = merged_reviews[-MAX_REVIEW_ITEMS:]
    base_review = existing["review"]
    incoming_review = incoming["review"]
    review_daily = dict(base_review["dailyCompleted"])
    for day, count in incoming_review["dailyCompleted"].items():
        review_daily[day] = max(review_daily.get(day, 0), count)
    merged["review"] = {
        "dailyCompleted": dict(list(review_daily.items())[-MAX_REVIEW_DAYS:]),
        "sessions": max(base_review["sessions"], incoming_review["sessions"]),
        "attempts": max(base_review["attempts"], incoming_review["attempts"]),
        "correct": max(base_review["correct"], incoming_review["correct"]),
    }
    return merged


@contextmanager
def _connect():
    connection = sqlite3.connect(config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS progress (
                user_id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                client_id TEXT NOT NULL DEFAULT '',
                title TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(sessions)")}
        if "client_id" not in columns:
            connection.execute("ALTER TABLE sessions ADD COLUMN client_id TEXT NOT NULL DEFAULT ''")
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS sessions_user_client_id "
            "ON sessions(user_id, client_id) WHERE client_id <> ''"
        )


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def create_user(email: str, name: str, password_hash: str):
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (email, name, password_hash, now_iso()),
        )
        return cursor.lastrowid


def get_user_by_email(email: str):
    with _connect() as connection:
        row = connection.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def get_user(user_id: int):
    with _connect() as connection:
        row = connection.execute("SELECT id, email, name, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def save_progress(user_id: int, payload: dict):
    serialized = json.dumps(normalize_progress(payload), ensure_ascii=False)
    with _connect() as connection:
        connection.execute(
            "INSERT INTO progress (user_id, payload, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET payload = excluded.payload, updated_at = excluded.updated_at",
            (user_id, serialized, now_iso()),
        )


def get_progress(user_id: int):
    with _connect() as connection:
        row = connection.execute("SELECT payload, updated_at FROM progress WHERE user_id = ?", (user_id,)).fetchone()
        if not row:
            return {"completed": [], "scores": [], "activeDays": [], "updated_at": None}
        try:
            payload = normalize_progress(json.loads(row["payload"]))
        except json.JSONDecodeError:
            payload = normalize_progress({})
        payload["updated_at"] = row["updated_at"]
        return payload


def save_session(user_id: int, title: str, payload: dict, client_id: str = ""):
    client_id = client_id[:80]
    with _connect() as connection:
        if client_id:
            connection.execute(
                "INSERT OR IGNORE INTO sessions (user_id, client_id, title, payload, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, client_id, title[:140], json.dumps(payload, ensure_ascii=False), now_iso()),
            )
        else:
            connection.execute(
                "INSERT INTO sessions (user_id, client_id, title, payload, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, "", title[:140], json.dumps(payload, ensure_ascii=False), now_iso()),
            )


def get_sessions(user_id: int, limit: int = 30):
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, client_id, title, payload, created_at FROM sessions WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, max(1, min(100, int(limit)))),
        ).fetchall()
    result = []
    for row in rows:
        try:
            payload = json.loads(row["payload"])
        except json.JSONDecodeError:
            payload = {}
        result.append({"id": row["id"], "client_id": row["client_id"], "title": row["title"], "created_at": row["created_at"], **payload})
    return result
