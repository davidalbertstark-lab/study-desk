import secrets
import time

from app.modules.auth.exceptions import InvalidLoginTicketError

# 60 seconds
_TICKET_TTL = 60

# ticket -> payload
_LOGIN_TICKETS: dict[str, dict] = {}


def create_login_ticket(
    *,
    access_token: str,
    refresh_token: str,
    user: dict,
) -> str:
    """
    Creates a one-time login ticket.

    Stored only in memory.

    Valid once.
    Valid for 60 seconds.
    """

    ticket = secrets.token_urlsafe(32)

    _LOGIN_TICKETS[ticket] = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user,
        "expires_at": time.time() + _TICKET_TTL,
    }

    return ticket


def exchange_login_ticket(ticket: str):
    """
    Exchanges a login ticket exactly once.
    """

    payload = _LOGIN_TICKETS.pop(ticket, None)

    if payload is None:
        raise InvalidLoginTicketError()

    if payload["expires_at"] < time.time():
        raise InvalidLoginTicketError()

    return {
        "access_token": payload["access_token"],
        "refresh_token": payload["refresh_token"],
        "user": payload["user"],
        "token_type": "bearer",
    }