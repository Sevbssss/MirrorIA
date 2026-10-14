"""Ficha de compra con enlace oficial. La vista traduce HTTP y delegará al servicio correspondiente."""
from flask import Blueprint, render_template
from app.services import search_service
bp = Blueprint('products', __name__)
@bp.get('/products/<product_id>')
def index(product_id):
    """Solo renderiza el maquetado. Las operaciones de negocio siguen pendientes."""
    return render_template('product_detail.html', title='Ficha de compra con enlace oficial', status='Maquetado sin procesamiento real')
