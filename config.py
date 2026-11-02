"""Configuración central del monolito; los valores se obtienen del entorno (.env)."""
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    TESTING = False
    # Sin SECRET_KEY en el entorno se genera una temporal: la sesión se pierde al reiniciar.
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    UPLOAD_FOLDER = str(BASE_DIR / os.environ.get("UPLOAD_FOLDER", "app/static/uploads"))
    # Límite de la solicitud completa (dos fotos) y de cada fotografía.
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 20 * 1024 * 1024))
    MAX_PHOTO_SIZE = 10 * 1024 * 1024
    DEPRATI_BASE_URL = os.environ.get("DEPRATI_BASE_URL", "https://www.deprati.com.ec")
    CATEGORIES = ('camisas', 'pantalones', 'shorts')
    RANKING_SIZE = 5
    PHOTO_COUNT = 2
