"""Presentación: recibirá solicitudes del probador y mostrará respuestas de tryon_service."""
from flask import Blueprint, render_template

tryon_bp = Blueprint("tryon", __name__, url_prefix="/probador")


@tryon_bp.get("/")
def index():
    return render_template("tryon.html")
