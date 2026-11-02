"""Presentación: recibe la consulta y muestra los filtros que interpreta search_service."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services import search_service
from app.services.search_service import SearchError
from app.views.session_helper import confirmed_photos_required, current_user_session

search_bp = Blueprint("search", __name__, url_prefix="/buscar")


@search_bp.get("/")
@confirmed_photos_required
def index():
    return render_template("search.html", user_session=current_user_session())


@search_bp.post("/")
@confirmed_photos_required
def submit():
    try:
        search_service.interpret(current_user_session(), request.form.get("query", ""))
    except SearchError as error:
        flash(str(error), "error")
    return redirect(url_for("search.index"))
