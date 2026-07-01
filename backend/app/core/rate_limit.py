import time
from collections import defaultdict

RESET_ATTEMPTS = defaultdict(list)

RESET_LIMIT = 5
WINDOW_SECONDS = 60 * 10  # 10 minutes


def is_rate_limited(email: str) -> bool:
    now = time.time()

    attempts = RESET_ATTEMPTS[email]

    # remove expired attempts
    RESET_ATTEMPTS[email] = [
        t for t in attempts if now - t < WINDOW_SECONDS
    ]

    if len(RESET_ATTEMPTS[email]) >= RESET_LIMIT:
        return True

    RESET_ATTEMPTS[email].append(now)
    return False