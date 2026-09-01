"""TalkMate Flask API server.

Server không lưu trạng thái phiên: client gửi kèm lịch sử hội thoại mỗi lượt,
nên có thể chạy nhiều tiến trình mà không cần chia sẻ session.
"""
from __future__ import annotations

import random
import secrets
import sys
from functools import wraps

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
coach = Coach()
database.init_db()

MAX_HISTORY = 40  # chặn payload quá lớn


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
    data = request.get_json(silent=True) or {}
    level_id = (data.get("level") or "").strip()
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
    data = request.get_json(silent=True) or {}
    level_id = (data.get("level") or "").strip()
    message = (data.get("message") or "").strip()
    difficulty = (data.get("difficulty") or "vua").strip()
    learner = data.get("learner") or {}
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
        {"role": t.get("role"), "text": str(t.get("text", ""))}
        for t in history
        if isinstance(t, dict) and t.get("role") in ("user", "partner")
    ][-MAX_HISTORY:]

    result = coach.respond(
        level_id, scenario_index, difficulty, history, message, learner, english_only
    )
    status = 400 if result.get("error") else 200
    return jsonify(result), status


@app.route("/api/pronunciation", methods=["POST"])
def api_pronunciation():
    data = request.get_json(silent=True) or {}
    transcript = (data.get("transcript") or "").strip()
    confidence = data.get("confidence")
    try:
        confidence = float(confidence) if confidence is not None else None
    except (TypeError, ValueError):
        confidence = None
    return jsonify(pronunciation_check(transcript, confidence))


@app.route("/api/auth/me")
def auth_me():
    user = current_user()
    return jsonify({"authenticated": bool(user), "user": user})


@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    name = str(data.get("name") or "").strip()
    password = str(data.get("password") or "")
    if not email or "@" not in email or len(name) < 2 or len(password) < 6:
        return jsonify({"error": "Enter a valid name, email, and password (6+ characters)."}), 400
    if database.get_user_by_email(email):
        return jsonify({"error": "An account with this email already exists."}), 409
    user_id = database.create_user(email, name[:80], generate_password_hash(password))
    session["user_id"] = user_id
    database.save_progress(user_id, {"completed": [], "scores": [], "activeDays": []})
    return jsonify({"user": database.get_user(user_id)})


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    password = str(data.get("password") or "")
    user = database.get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Email or password is incorrect."}), 401
    session["user_id"] = user["id"]
    return jsonify({"user": database.get_user(user["id"])})


@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/sync", methods=["GET", "POST"])
@login_required
def sync_progress():
    user = current_user()
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        payload = data.get("progress") if isinstance(data.get("progress"), dict) else {}
        database.save_progress(user["id"], payload)
        return jsonify({"ok": True, "progress": database.get_progress(user["id"])})
    return jsonify({"progress": database.get_progress(user["id"]), "sessions": database.get_sessions(user["id"])})


@app.route("/api/sessions", methods=["POST"])
@login_required
def sync_session():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title") or "TalkMate session")
    payload = data.get("session") if isinstance(data.get("session"), dict) else {}
    database.save_session(current_user()["id"], title, payload)
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
