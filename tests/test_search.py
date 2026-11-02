"""Intérprete de búsquedas."""
import pytest

from app.services.search_service import parse_query


def test_spec_example():
    assert parse_query("Quiero una camisa azul para una ocasión formal de mujer") == {
        "section": "Mujer",
        "category": "Camisa",
        "color": "Azul",
        "style": "Formal",
    }


@pytest.mark.parametrize(
    "text, category",
    [("un pantalón", "Pantalón"), ("PANTALONES", "Pantalón"), ("unos shorts", "Short"), ("una blusa", "Camisa")],
)
def test_detects_category(text, category):
    assert parse_query(text)["category"] == category


def test_pantaloneta_is_a_short():
    assert parse_query("una pantaloneta")["category"] == "Short"


def test_informal_is_not_formal():
    assert parse_query("camisa informal")["style"] == "Casual"


def test_values_not_mentioned_stay_empty():
    assert parse_query("una camisa") == {"section": "Unisex", "category": "Camisa", "color": None, "style": None}


def test_detects_man_section_and_feminine_color():
    filters = parse_query("camisa blanca para caballero")
    assert filters["section"] == "Hombre"
    assert filters["color"] == "Blanco"
