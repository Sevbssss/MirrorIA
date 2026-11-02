"""Presentación: recepción y confirmación de fotografías; la validación está en image_service."""
from flask import Blueprint, Response, abort, current_app, flash, redirect, render_template, request, url_for

from app.services import image_service
from app.services.image_service import PhotoError
from app.views.session_helper import current_user_session, photos_required

photos_bp = Blueprint("photos", __name__, url_prefix="/fotografias")


@photos_bp.get("/")
def upload():
    return render_template("photos.html", user_session=current_user_session())


@photos_bp.post("/")
def save():
    uploads = {kind: _read_upload(kind) for kind in image_service.PHOTO_LABELS}
    try:
        image_service.store_photos(current_user_session(), uploads, current_app.config["MAX_PHOTO_SIZE"])
    except PhotoError as error:
        flash(str(error), "error")
        return redirect(url_for("photos.upload"))
    return redirect(url_for("photos.confirm"))


@photos_bp.get("/confirmar")
@photos_required
def confirm():
    return render_template("confirm_photos.html")


@photos_bp.post("/confirmar")
@photos_required
def accept():
    current_user_session().photos_confirmed = True
    return redirect(url_for("search.index"))


@photos_bp.get("/vista-previa/<kind>")
def preview(kind: str):
    photo = image_service.get_photo(current_user_session(), kind)
    if photo is None:
        abort(404)
    return Response(photo, mimetype="image/jpeg", headers={"Cache-Control": "no-store"})


@photos_bp.app_errorhandler(413)
def too_large(_error):
    flash("Las fotografías superan el tamaño máximo permitido. Usa archivos más livianos.", "error")
    return redirect(url_for("photos.upload"))


def _read_upload(kind: str) -> tuple[str, bytes] | None:
    file = request.files.get(kind)
    return (file.filename, file.read()) if file and file.filename else None
