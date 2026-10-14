"""RF-03: resultado estimado de colorimetría; no diagnóstico médico."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ColorAnalysis:
    palette: tuple[str, ...]
    confidence: float
    # Método y umbral de confianza pendientes de validación experimental.
