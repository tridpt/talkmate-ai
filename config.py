"""Configuration for TalkMate."""
import os
import secrets
from pathlib import Path

# ── Nạp file .env (nếu có) ──────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def _env_bool(key: str, default: bool) -> bool:
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


# ── Gemini API ──────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

# ── Flask ───────────────────────────────────────────────────
APP_NAME = "TalkMate — Speak English in real situations"
FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.environ.get("FLASK_PORT", "5001"))
FLASK_DEBUG = _env_bool("FLASK_DEBUG", False)
DATABASE_PATH = Path(os.environ.get("TALKMATE_DB", str(Path(__file__).parent / "talkmate.db")))
SECRET_KEY = os.environ.get("TALKMATE_SECRET_KEY", "") or secrets.token_hex(32)


def ai_enabled() -> bool:
    """Có gọi được Gemini không (đã cấu hình key)."""
    return bool(GEMINI_API_KEY)
