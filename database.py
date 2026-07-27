"""Database Abstraction Layer for SQLite/PostgreSQL."""

import sqlite3
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime
import config


def get_connection() -> sqlite3.Connection:
    """Establish and return a database connection."""
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                original_url TEXT NOT NULL,
                short_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """
        )
        conn.commit()


def register_user(user_id: int, username: Optional[str]) -> None:
    """Insert or update user record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET username = excluded.username
        """,
            (user_id, username),
        )
        conn.commit()


def save_url(user_id: int, original_url: str, short_url: str) -> None:
    """Save shortened URL record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO urls (user_id, original_url, short_url)
            VALUES (?, ?, ?)
        """,
            (user_id, original_url, short_url),
        )
        conn.commit()


def get_user_history(user_id: int, limit: int = 10) -> List[sqlite3.Row]:
    """Retrieve user's shortened link history."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, original_url, short_url, created_at
            FROM urls
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """,
            (user_id, limit),
        )
        return cursor.fetchall()


def delete_single_url(user_id: int, url_id: int) -> bool:
    """Delete a single URL record owned by the user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM urls WHERE id = ? AND user_id = ?", (url_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def clear_user_history(user_id: int) -> int:
    """Delete all URL records for a given user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM urls WHERE user_id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount


def get_all_user_ids() -> List[int]:
    """Fetch all registered Telegram User IDs for broadcasting."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        return [row["user_id"] for row in cursor.fetchall()]


def get_admin_stats() -> Dict[str, Any]:
    """Gather overall database statistics for the admin dashboard."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM urls")
        total_urls = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(*) FROM urls WHERE DATE(created_at) = DATE('now')"
        )
        today_urls = cursor.fetchone()[0]
        
        cursor.execute(
            """
            SELECT users.username, users.user_id, COUNT(urls.id) as link_count
            FROM urls
            JOIN users ON users.user_id = urls.user_id
            GROUP BY urls.user_id
            ORDER BY link_count DESC
            LIMIT 5
        """
        )
        active_users = cursor.fetchall()
        
        return {
            "total_users": total_users,
            "total_urls": total_urls,
            "today_urls": today_urls,
            "active_users": active_users,
        }
