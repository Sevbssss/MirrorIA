"""Presentación: recepción y confirmación de fotografías; delegará validación y procesamiento a image_service."""
from flask import Blueprint, render_template

photos_bp = Blueprint("photos", __name__, url_prefix="/fotografias")


@photos_bp.get("/")
def upload():
    return render_template("photos.html")


@photos_bp.get("/confirmar")
def confirm():
    return render_template("confirm_photos.html")
