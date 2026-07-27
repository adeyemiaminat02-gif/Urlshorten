"""Utility and Helper Functions."""

import re
import time
from typing import Dict, List

URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
    r"localhost|"  # localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

# In-memory sliding window rate limiter: {user_id: [timestamps]}
RATE_LIMIT_STORE: Dict[int, List[float]] = {}
MAX_REQUESTS_PER_MINUTE = 10


def is_valid_url(url: str) -> bool:
    """Validate string against URL patterns."""
    return bool(URL_REGEX.match(url.strip()))


def is_rate_limited(user_id: int) -> bool:
    """Check if user has exceeded request rate limit."""
    now = time.time()
    window_start = now - 60.0

    if user_id not in RATE_LIMIT_STORE:
        RATE_LIMIT_STORE[user_id] = [now]
        return False

    # Filter timestamps within last 60 seconds
    timestamps = [t for t in RATE_LIMIT_STORE[user_id] if t > window_start]
    timestamps.append(now)
    RATE_LIMIT_STORE[user_id] = timestamps

    return len(timestamps) > MAX_REQUESTS_PER_MINUTE
