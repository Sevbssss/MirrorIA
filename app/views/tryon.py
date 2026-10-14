"""Probador virtual aproximado. La vista traduce HTTP y delegará al servicio correspondiente."""
from flask import Blueprint, render_template
from app.services import tryon_service
bp = Blueprint('tryon', __name__)
@bp.get('/tryon')
def index():
    """Solo renderiza el maquetado. Las operaciones de negocio siguen pendientes."""
    return render_template('tryon.html', title='Probador virtual aproximado', status='Maquetado sin procesamiento real')
