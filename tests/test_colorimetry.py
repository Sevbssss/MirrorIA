"""Colorimetría: reglas de clasificación y comportamiento sin rostro."""
import pytest

from app.services.colorimetry_service import (
    PALETTES,
    ColorimetryError,
    _classify_skin_tone,
    _classify_undertone,
    analyze,
)
from tests.conftest import image_bytes


@pytest.mark.parametrize(
    "a_value, b_value, expected",
    [(5, 20, "warm"), (10, 17, "warm-neutral"), (12, 14, "cool-neutral"), (15, 10, "cool")],
)
def test_undertone_follows_hue_angle(a_value, b_value, expected):
    assert _classify_undertone(a_value, b_value) == expected


@pytest.mark.parametrize(
    "lightness, b_value, expected", [(90, 15, "muy claro"), (60, 15, "intermedio"), (40, 20, "moreno"), (20, 10, "oscuro")]
)
def test_skin_tone_follows_ita(lightness, b_value, expected):
    assert _classify_skin_tone(lightness, b_value) == expected


def test_every_undertone_has_a_palette():
    for a_value, b_value in [(5, 20), (10, 17), (12, 14), (15, 10)]:
        assert PALETTES[_classify_undertone(a_value, b_value)]


def test_image_without_face_raises_controlled_error():
    with pytest.raises(ColorimetryError):
        analyze(image_bytes("JPEG"))
