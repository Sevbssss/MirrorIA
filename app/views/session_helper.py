"""Une la cookie de sesión de Flask con el almacén temporal y protege el orden del flujo."""
from functools import wraps

from flask import flash, redirect, session, url_for

from app.models.user_session import UserSession
from app.services import session_service


def current_user_session() -> UserSession:
    user_session = session_service.get_or_create(session.get("token"))
    session["token"] = user_session.token
    return user_session


def _requires(condition, message: str, endpoint: str):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not condition(current_user_session()):
                flash(message, "info")
                return redirect(url_for(endpoint))
            return view(*args, **kwargs)
        return wrapper
    return decorator


photos_required = _requires(
    lambda s: s.has_photos, "Primero carga tus dos fotografías.", "photos.upload"
)
confirmed_photos_required = _requires(
    lambda s: s.has_photos and s.photos_confirmed, "Primero carga y confirma tus dos fotografías.", "photos.upload"
)
