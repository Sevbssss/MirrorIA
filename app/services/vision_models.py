"""Modelos de MediaPipe. Se crea un detector por análisis: son pocos y evita compartir estado."""
from pathlib import Path

import cv2
import numpy as np

MODELS_DIR = Path(__file__).resolve().parents[1] / "ml_models"


def decode_image(data: bytes) -> np.ndarray | None:
    """Convierte bytes de imagen a una matriz BGR de OpenCV."""
    return cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)


def detect_face_landmarks(bgr: np.ndarray) -> list | None:
    """Devuelve los puntos del primer rostro o None si no hay ninguno."""
    # MediaPipe tarda varios segundos en importarse: se carga solo cuando se necesita.
    from mediapipe.tasks.python import vision

    options = vision.FaceLandmarkerOptions(base_options=_model_options("face_landmarker.task"), num_faces=1)
    with vision.FaceLandmarker.create_from_options(options) as detector:
        faces = detector.detect(_to_mediapipe_image(bgr)).face_landmarks
    return faces[0] if faces else None


def _to_mediapipe_image(bgr: np.ndarray):
    import mediapipe as mp

    return mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))


def _model_options(filename: str):
    from mediapipe.tasks.python import BaseOptions

    # Por buffer: MediaPipe no abre rutas con caracteres fuera de ASCII en Windows.
    return BaseOptions(model_asset_buffer=(MODELS_DIR / filename).read_bytes())
