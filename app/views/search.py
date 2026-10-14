"""Buscar prendas de DePrati y ranking de cinco opciones. La vista traduce HTTP y delegará al servicio correspondiente."""
from flask import Blueprint, render_template
from app.services import search_service
bp = Blueprint('search', __name__)
@bp.get('/search')
def index():
    """Solo renderiza el maquetado. Las operaciones de negocio siguen pendientes."""
    return render_template('search.html', title='Buscar prendas de DePrati y ranking de cinco opciones', status='Maquetado sin procesamiento real')
