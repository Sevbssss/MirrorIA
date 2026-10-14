"""Inicio del flujo de cuatro pasos. La vista traduce HTTP y delegará al servicio correspondiente."""
from flask import Blueprint, render_template
bp = Blueprint('home', __name__)
@bp.get('/')
def index():
    """Solo renderiza el maquetado. Las operaciones de negocio siguen pendientes."""
    return render_template('index.html', title='Inicio del flujo de cuatro pasos', status='Maquetado sin procesamiento real')
