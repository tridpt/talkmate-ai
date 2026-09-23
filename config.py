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


def _env_int(key: str, default: int, minimum: int = 0) -> int:
    try:
        return max(minimum, int(os.environ.get(key, default)))
    except (TypeError, ValueError):
        return default


# ── Gemini API ──────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()

# ── Flask ───────────────────────────────────────────────────
APP_NAME = "TalkMate — Speak English in real situations"
TALKMATE_ENV = os.environ.get("TALKMATE_ENV", "development").strip().lower()
IS_PRODUCTION = TALKMATE_ENV in {"production", "prod"}
FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
FLASK_PORT = _env_int("FLASK_PORT", 5001, minimum=1)
FLASK_DEBUG = _env_bool("FLASK_DEBUG", False)
DATABASE_PATH = Path(os.environ.get("TALKMATE_DB", str(Path(__file__).parent / "talkmate.db")))
DATABASE_TIMEOUT_SECONDS = _env_int("TALKMATE_DB_TIMEOUT_SECONDS", 10, minimum=1)
_configured_secret = os.environ.get("TALKMATE_SECRET_KEY", "").strip()
SECRET_KEY = _configured_secret or secrets.token_hex(32)
SECRET_KEY_CONFIGURED = bool(_configured_secret)
SESSION_COOKIE_SECURE = _env_bool("TALKMATE_SESSION_SECURE", False)
TRUST_PROXY = _env_bool("TALKMATE_TRUST_PROXY", False)
MAX_REQUEST_BYTES = _env_int("TALKMATE_MAX_REQUEST_BYTES", 102400, minimum=1)
AUTH_RATE_LIMIT = _env_int("TALKMATE_AUTH_RATE_LIMIT", 10, minimum=1)
AUTH_RATE_WINDOW_SECONDS = _env_int("TALKMATE_AUTH_RATE_WINDOW_SECONDS", 60, minimum=1)


def validate_runtime_config() -> None:
    """Fail safely when a public deployment misses session security settings."""
    if not IS_PRODUCTION:
        return
    missing = []
    if not SECRET_KEY_CONFIGURED:
        missing.append("TALKMATE_SECRET_KEY")
    if not SESSION_COOKIE_SECURE:
        missing.append("TALKMATE_SESSION_SECURE=true")
    if missing:
        raise RuntimeError(
            "Production configuration is incomplete. Set " + ", ".join(missing) + "."
        )


def ai_enabled() -> bool:
    """Có gọi được Gemini không (đã cấu hình key)."""
    return bool(GEMINI_API_KEY)
