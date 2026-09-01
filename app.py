"""TalkMate Flask API server.

Server không lưu trạng thái phiên: client gửi kèm lịch sử hội thoại mỗi lượt,
nên có thể chạy nhiều tiến trình mà không cần chia sẻ session.
"""
from __future__ import annotations

import random
import secrets
import sqlite3
import sys
from collections import defaultdict, deque
from functools import wraps
from time import monotonic

from flask import Flask, jsonify, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

import config
import database
import scenarios
from coach import Coach, SCORE_LABELS, pronunciation_check

# Sửa encoding console trên Windows để in được tiếng Việt.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

app = Flask(__name__, static_folder="frontend", static_url_path="")
app.secret_key = config.SECRET_KEY
app.config.update(
    MAX_CONTENT_LENGTH=config.MAX_REQUEST_BYTES,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=config.SESSION_COOKIE_SECURE,
)
coach = Coach()
database.init_db()

MAX_HISTORY = 40  # chặn payload quá lớn
MAX_MESSAGE_LENGTH = 600
MAX_TURN_LENGTH = 1_200
MAX_SESSION_TITLE_LENGTH = 140
MAX_TRANSCRIPT_TURNS = 40
_auth_attempts = defaultdict(deque)


def request_data():
    """Return a JSON object, never a list or scalar that would raise a 500."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def text_value(value, limit=MAX_MESSAGE_LENGTH):
    return value.strip()[:limit] if isinstance(value, str) else ""


def csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def begin_user_session(user_id: int):
    session.clear()
    session["user_id"] = user_id
    csrf_token()


def public_user(user):
    if not user:
        return None
    return {key: user[key] for key in ("id", "email", "name", "created_at") if key in user}


def auth_response(user, status=200):
    return jsonify({"user": public_user(user), "csrf_token": csrf_token()}), status


def _recent_auth_attempts(address):
    """Return failed attempts still inside the rate-limit window."""
    now = monotonic()
    attempts = _auth_attempts[address]
    while attempts and now - attempts[0] >= config.AUTH_RATE_WINDOW_SECONDS:
        attempts.popleft()
    return attempts


def rate_limited():
    """Apply a small in-memory brake to repeated password guesses."""
    address = request.remote_addr or "unknown"
    return len(_recent_auth_attempts(address)) >= config.AUTH_RATE_LIMIT


def record_auth_failure():
    _recent_auth_attempts(request.remote_addr or "unknown").append(monotonic())


def clear_auth_failures():
    _auth_attempts.pop(request.remote_addr or "unknown", None)


def current_user():
    user_id = session.get("user_id")
    return database.get_user(user_id) if user_id else None


def login_required(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        if not current_user():
            return jsonify({"error": "Please sign in to sync your progress."}), 401
        return handler(*args, **kwargs)

    return wrapped


def csrf_required(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        expected = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token", "")
        if not expected or not secrets.compare_digest(expected, supplied):
            return jsonify({"error": "Your session expired. Refresh and try again."}), 403
        return handler(*args, **kwargs)

    return wrapped


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request is too large."}), 413


@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "ai": coach.online,
        "model": config.GEMINI_MODEL if coach.online else None,
    })


@app.route("/api/levels")
def api_levels():
    return jsonify({
        "levels": scenarios.level_list(),
        "score_labels": SCORE_LABELS,
        "ai": coach.online,
    })


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request_data()
    if data is None:
        return jsonify({"error": "JSON object expected."}), 400
    level_id = text_value(data.get("level"), 40)
    level = scenarios.get_level(level_id)
    if not level:
        return jsonify({"error": "Cấp độ không hợp lệ."}), 400

    # Cho phép chọn tình huống cụ thể, mặc định chọn ngẫu nhiên.
    idx = data.get("scenario_index")
    if idx is None:
        idx = random.randrange(len(level["scenarios"]))
    else:
        try:
            idx = int(idx) % len(level["scenarios"])
        except (TypeError, ValueError):
            idx = 0

    scenario = scenarios.get_scenario(level_id, idx)
    return jsonify({
        "level": {
            "id": level["id"],
            "name": level["name"],
            "goal": level["goal"],
            "color": level["color"],
        },
        "scenario_index": idx,
        "scenario": {
            "title": scenario["title"],
            "context": scenario["context"],
            "persona": scenario["persona"],
            "icon": scenario["icon"],
            "duration": scenario["duration"],
            "starter": scenario["starter"],
            "vocabulary": scenario["vocabulary"],
        },
        "opening": scenario["opening"],
    })


@app.route("/api/reply", methods=["POST"])
def api_reply():
    data = request_data()
    if data is None:
        return jsonify({"error": "JSON object expected."}), 400
    level_id = text_value(data.get("level"), 40)
    message = text_value(data.get("message"))
    difficulty = text_value(data.get("difficulty"), 20) or "vua"
    learner = data.get("learner") if isinstance(data.get("learner"), dict) else {}
    english_only = bool(data.get("english_only", False))

    if not message:
        return jsonify({"error": "Bạn chưa nhập câu trả lời."}), 400

    try:
        scenario_index = int(data.get("scenario_index", 0))
    except (TypeError, ValueError):
        scenario_index = 0

    history = data.get("history") or []
    if not isinstance(history, list):
        history = []
    # Chỉ giữ các lượt hợp lệ và giới hạn độ dài.
    history = [
        {"role": t.get("role"), "text": text_value(t.get("text"), MAX_TURN_LENGTH)}
        for t in history
        if isinstance(t, dict) and t.get("role") in ("user", "partner") and text_value(t.get("text"), MAX_TURN_LENGTH)
    ][-MAX_HISTORY:]

    result = coach.respond(
        level_id, scenario_index, difficulty, history, message, learner, english_only
    )
    status = 400 if result.get("error") else 200
    return jsonify(result), status


@app.route("/api/pronunciation", methods=["POST"])
def api_pronunciation():
    data = request_data()
    if data is None:
        return jsonify({"error": "JSON object expected."}), 400
    transcript = text_value(data.get("transcript"), MAX_TURN_LENGTH)
    confidence = data.get("confidence")
    try:
        confidence = float(confidence) if confidence is not None else None
    except (TypeError, ValueError):
        confidence = None
    return jsonify(pronunciation_check(transcript, confidence))


@app.route("/api/auth/me")
def auth_me():
    user = current_user()
    return jsonify({"authenticated": bool(user), "user": public_user(user), "csrf_token": csrf_token()})


@app.route("/api/auth/register", methods=["POST"])
@csrf_required
def auth_register():
    if rate_limited():
        return jsonify({"error": "Too many attempts. Please wait a minute and try again."}), 429
    data = request_data()
    if data is None:
        return jsonify({"error": "JSON object expected."}), 400
    email = text_value(data.get("email"), 254).lower()
    name = text_value(data.get("name"), 80)
    password = data.get("password") if isinstance(data.get("password"), str) else ""
    if not email or "@" not in email or len(name) < 2 or len(password) < 6:
        record_auth_failure()
        return jsonify({"error": "Enter a valid name, email, and password (6+ characters)."}), 400
    if database.get_user_by_email(email):
        record_auth_failure()
        return jsonify({"error": "An account with this email already exists."}), 409
    try:
        user_id = database.create_user(email, name, generate_password_hash(password))
    except sqlite3.IntegrityError:
        record_auth_failure()
        return jsonify({"error": "An account with this email already exists."}), 409
    clear_auth_failures()
    begin_user_session(user_id)
    database.save_progress(user_id, {"completed": [], "scores": [], "activeDays": []})
    return auth_response(database.get_user(user_id))


@app.route("/api/auth/login", methods=["POST"])
@csrf_required
def auth_login():
    if rate_limited():
        return jsonify({"error": "Too many attempts. Please wait a minute and try again."}), 429
    data = request_data()
    if data is None:
        return jsonify({"error": "JSON object expected."}), 400
    email = text_value(data.get("email"), 254).lower()
    password = data.get("password") if isinstance(data.get("password"), str) else ""
    user = database.get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        record_auth_failure()
        return jsonify({"error": "Email or password is incorrect."}), 401
    clear_auth_failures()
    begin_user_session(user["id"])
    return auth_response(database.get_user(user["id"]))


@app.route("/api/auth/logout", methods=["POST"])
@csrf_required
def auth_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/sync", methods=["GET", "POST"])
@login_required
def sync_progress():
    user = current_user()
    if request.method == "POST":
        expected = session.get("csrf_token")
        supplied = request.headers.get("X-CSRF-Token", "")
        if not expected or not secrets.compare_digest(expected, supplied):
            return jsonify({"error": "Your session expired. Refresh and try again."}), 403
        data = request_data()
        if data is None or not isinstance(data.get("progress"), dict):
            return jsonify({"error": "A progress object is required."}), 400
        merged = database.merge_progress(database.get_progress(user["id"]), data["progress"])
        database.save_progress(user["id"], merged)
        return jsonify({"ok": True, "progress": database.get_progress(user["id"]), "csrf_token": csrf_token()})
    return jsonify({"progress": database.get_progress(user["id"]), "sessions": database.get_sessions(user["id"])})


@app.route("/api/sessions", methods=["POST"])
@login_required
@csrf_required
def sync_session():
    data = request_data()
    if data is None or not isinstance(data.get("session"), dict):
        return jsonify({"error": "A session object is required."}), 400
    title = text_value(data.get("title"), MAX_SESSION_TITLE_LENGTH) or "TalkMate session"
    client_id = text_value(data.get("client_id"), 80)
    session_payload = data["session"]
    transcript = session_payload.get("transcript") if isinstance(session_payload.get("transcript"), list) else []
    safe_transcript = [
        {"role": turn.get("role"), "text": text_value(turn.get("text"), MAX_TURN_LENGTH)}
        for turn in transcript
        if isinstance(turn, dict) and turn.get("role") in ("user", "partner") and text_value(turn.get("text"), MAX_TURN_LENGTH)
    ][-MAX_TRANSCRIPT_TURNS:]
    try:
        turns = min(MAX_TRANSCRIPT_TURNS, max(0, int(session_payload.get("turns") or 0)))
    except (TypeError, ValueError):
        turns = len([turn for turn in safe_transcript if turn["role"] == "user"])
    payload = {
        "level": text_value(session_payload.get("level"), 10) or "A2",
        "overall": session_payload.get("overall"),
        "turns": turns,
        "completed_at": text_value(session_payload.get("completed_at"), 40),
        "transcript": safe_transcript,
    }
    database.save_session(current_user()["id"], title, payload, client_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("=" * 56)
    print(config.APP_NAME)
    print("=" * 56)
    print(f"AI: {'on (' + config.GEMINI_MODEL + ')' if coach.online else 'off (chế độ offline)'}")
    print(f"Địa chỉ: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    if not coach.online:
        print("Mẹo: đặt GEMINI_API_KEY trong .env để bật chấm điểm & hội thoại bằng AI.")
    print("=" * 56)
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.FLASK_DEBUG)
