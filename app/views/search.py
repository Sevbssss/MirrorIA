"""Presentación: recibirá criterios de búsqueda y mostrará resultados de search_service."""
from flask import Blueprint, render_template

search_bp = Blueprint("search", __name__, url_prefix="/buscar")


@search_bp.get("/")
def index():
    return render_template("search.html")
