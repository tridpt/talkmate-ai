"""Small SQLite persistence layer for TalkMate accounts and sync data."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

import config


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
                title TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
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
    serialized = json.dumps(payload, ensure_ascii=False)
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
            payload = json.loads(row["payload"])
        except json.JSONDecodeError:
            payload = {}
        payload["updated_at"] = row["updated_at"]
        return payload


def save_session(user_id: int, title: str, payload: dict):
    with _connect() as connection:
        connection.execute(
            "INSERT INTO sessions (user_id, title, payload, created_at) VALUES (?, ?, ?, ?)",
            (user_id, title[:140], json.dumps(payload, ensure_ascii=False), now_iso()),
        )


def get_sessions(user_id: int, limit: int = 30):
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, title, payload, created_at FROM sessions WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, max(1, min(100, int(limit)))),
        ).fetchall()
    result = []
    for row in rows:
        try:
            payload = json.loads(row["payload"])
        except json.JSONDecodeError:
            payload = {}
        result.append({"id": row["id"], "title": row["title"], "created_at": row["created_at"], **payload})
    return result
