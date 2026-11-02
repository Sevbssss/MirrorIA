"""RF-03/RNF-02: estima tono de piel y subtono con MediaPipe y OpenCV.

Es una estimación por reglas, sensible a la iluminación de la foto; no es un diagnóstico.
Tono: ángulo tipológico individual (ITA). Subtono: ángulo de matiz en el espacio CIELAB.
"""
import math

import cv2
import numpy as np

from app.models.color_analysis import ColorAnalysis
from app.services import vision_models

# Puntos de MediaPipe Face Mesh: mejillas y frente, zonas con piel sin labios ni cejas.
SKIN_LANDMARKS = (50, 280, 101, 330, 151)
PATCH_RATIO = 0.03

SKIN_TONES = ((55, "muy claro"), (41, "claro"), (28, "intermedio"), (10, "bronceado"), (-30, "moreno"))
DARKEST_TONE = "oscuro"
UNDERTONES = ((62, "warm"), (54, "warm-neutral"), (46, "cool-neutral"))
COOLEST_UNDERTONE = "cool"
PALETTES = {
    "warm": ("Terracota", "Coral", "Beige", "Verde"),
    "warm-neutral": ("Terracota", "Coral", "Beige", "Azul"),
    "cool-neutral": ("Azul", "Gris", "Vino", "Verde"),
    "cool": ("Azul", "Celeste", "Gris", "Vino"),
}


class ColorimetryError(Exception):
    """No se pudo analizar el rostro; el mensaje se puede mostrar al usuario."""


def analyze(face: bytes) -> ColorAnalysis:
    """Analiza la foto de rostro y devuelve el tono, el subtono y los colores favorables."""
    bgr = vision_models.decode_image(face)
    landmarks = vision_models.detect_face_landmarks(bgr) if bgr is not None else None
    if landmarks is None:
        raise ColorimetryError("No detectamos un rostro en la foto. Usa una foto frontal y bien iluminada.")

    lightness, a_value, b_value = _median_skin_lab(bgr, landmarks)
    undertone = _classify_undertone(a_value, b_value)
    return ColorAnalysis(
        skin_tone=_classify_skin_tone(lightness, b_value),
        undertone=undertone,
        recommended_colors=PALETTES[undertone],
    )


def _median_skin_lab(bgr: np.ndarray, landmarks: list) -> tuple[float, float, float]:
    height, width = bgr.shape[:2]
    radius = max(2, int(max(height, width) * PATCH_RATIO / 2))
    patches = [_patch(bgr, int(landmarks[i].x * width), int(landmarks[i].y * height), radius) for i in SKIN_LANDMARKS]
    pixels = np.concatenate([patch.reshape(-1, 3) for patch in patches if patch.size])
    lab = cv2.cvtColor(pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    # OpenCV guarda L en 0-255 y a, b desplazados en 128.
    lightness, a_value, b_value = np.median(lab, axis=0)
    return float(lightness) * 100 / 255, float(a_value) - 128, float(b_value) - 128


def _patch(bgr: np.ndarray, x: int, y: int, radius: int) -> np.ndarray:
    return bgr[max(y - radius, 0):y + radius, max(x - radius, 0):x + radius]


def _classify_skin_tone(lightness: float, b_value: float) -> str:
    ita = math.degrees(math.atan2(lightness - 50, b_value))
    for threshold, name in SKIN_TONES:
        if ita > threshold:
            return name
    return DARKEST_TONE


def _classify_undertone(a_value: float, b_value: float) -> str:
    hue = math.degrees(math.atan2(b_value, a_value))
    for threshold, name in UNDERTONES:
        if hue >= threshold:
            return name
    return COOLEST_UNDERTONE
