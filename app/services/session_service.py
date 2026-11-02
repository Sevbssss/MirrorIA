"""Almacén temporal en memoria de las sesiones; caducan por inactividad."""
import secrets
from threading import Lock
from time import time

from app.models.user_session import UserSession

SESSION_TTL_SECONDS = 30 * 60

_sessions: dict[str, UserSession] = {}
_lock = Lock()


def get_or_create(token: str | None) -> UserSession:
    """Devuelve la sesión del token o crea una nueva, y elimina las caducadas."""
    now = time()
    with _lock:
        _purge_expired(now)
        user_session = _sessions.get(token) if token else None
        if user_session is None:
            user_session = UserSession(token=secrets.token_urlsafe(32))
            _sessions[user_session.token] = user_session
        user_session.last_seen = now
        return user_session


def _purge_expired(now: float) -> None:
    expired = [t for t, s in _sessions.items() if now - s.last_seen > SESSION_TTL_SECONDS]
    for token in expired:
        _sessions.pop(token).clear()
