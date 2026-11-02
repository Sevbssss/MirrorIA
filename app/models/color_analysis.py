"""RF-03: resultado estimado de colorimetría; no es un diagnóstico médico."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ColorAnalysis:
    skin_tone: str
    undertone: str
    recommended_colors: tuple[str, ...]
