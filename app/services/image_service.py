"""RF-01: valida y normaliza las fotografías de rostro y cuerpo; nunca las guarda en disco."""
import io

from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.utils import secure_filename

from app.models.user_session import UserSession

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_FORMATS = {"JPEG", "PNG"}
MIN_SIDE_PIXELS = 200
MAX_SIDE_PIXELS = 1600
PHOTO_LABELS = {"face": "foto de rostro", "body": "foto de cuerpo completo"}


class PhotoError(Exception):
    """Error de validación con un mensaje que se puede mostrar al usuario."""


def store_photos(user_session: UserSession, uploads: dict, max_bytes: int) -> None:
    """Valida las fotos recibidas y solo las guarda en la sesión si todas son correctas.

    `uploads` asocia "face" y "body" con (nombre de archivo, contenido) o None.
    Una foto ausente es válida si la sesión ya tiene una de ese tipo.
    """
    validated = {}
    for kind, label in PHOTO_LABELS.items():
        upload = uploads.get(kind)
        if upload is not None:
            validated[kind] = validate_photo(upload[0], upload[1], max_bytes, label)
        elif get_photo(user_session, kind) is None:
            raise PhotoError(f"Falta la {label}. Selecciona un archivo o usa la cámara.")

    for kind, photo in validated.items():
        setattr(user_session, f"{kind}_photo", photo)
    user_session.reset_progress()


def get_photo(user_session: UserSession, kind: str) -> bytes | None:
    return getattr(user_session, f"{kind}_photo") if kind in PHOTO_LABELS else None


def validate_photo(filename: str, data: bytes, max_bytes: int, label: str = "fotografía") -> bytes:
    """Comprueba nombre, tamaño y contenido, y devuelve la imagen como JPEG sin metadatos."""
    if _extension(filename) not in ALLOWED_EXTENSIONS:
        raise PhotoError(f"La {label} debe ser un archivo JPG, JPEG o PNG.")
    if not data:
        raise PhotoError(f"La {label} está vacía. Vuelve a cargarla.")
    if len(data) > max_bytes:
        raise PhotoError(f"La {label} supera el máximo de {max_bytes // (1024 * 1024)} MB.")
    return _normalize(data, label)


def _extension(filename: str) -> str:
    return secure_filename(filename or "").rpartition(".")[2].lower()


def _normalize(data: bytes, label: str) -> bytes:
    try:
        with Image.open(io.BytesIO(data)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise PhotoError(f"La {label} debe ser un archivo JPG, JPEG o PNG.")
            image.load()
            normalized = ImageOps.exif_transpose(image).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as error:
        raise PhotoError(f"No pudimos leer la {label}. Vuelve a cargarla.") from error

    if min(normalized.size) < MIN_SIDE_PIXELS:
        raise PhotoError(f"La {label} es demasiado pequeña. Usa una de al menos {MIN_SIDE_PIXELS} px por lado.")
    normalized.thumbnail((MAX_SIDE_PIXELS, MAX_SIDE_PIXELS))
    output = io.BytesIO()
    normalized.save(output, format="JPEG", quality=90)
    return output.getvalue()
