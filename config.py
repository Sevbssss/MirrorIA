"""Configuración tentativa. Fotos exclusivamente en memoria según RNF-04."""
class Config:
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Límite propuesto; validar con el equipo.
    CATEGORIES = ('camisas', 'pantalones', 'shorts')
    RANKING_SIZE = 5
    PHOTO_COUNT = 2
    # No hay cuentas, historial ni almacenamiento persistente de fotografías.
