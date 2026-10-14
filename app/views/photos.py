"""Tus fotografías: rostro y cuerpo completo. La vista traduce HTTP y delegará al servicio correspondiente."""
from flask import Blueprint, render_template
from app.services import image_service
bp = Blueprint('photos', __name__)
@bp.get('/photos')
def index():
    """Solo renderiza el maquetado. Las operaciones de negocio siguen pendientes."""
    return render_template('photos.html', title='Tus fotografías: rostro y cuerpo completo', status='Maquetado sin procesamiento real')

@bp.get('/photos/confirm')
def confirm():
    """Confirmación prevista antes de analizar las dos fotos; no hay subida implementada."""
    return render_template('confirm_photos.html', title='Confirmar fotografías', status='Pendiente')
