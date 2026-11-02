"""Ranking de recomendaciones."""
from decimal import Decimal

from app.models.color_analysis import ColorAnalysis
from app.models.product import Product
from app.services.recommendation_service import find_by_id, rank

ANALYSIS = ColorAnalysis("claro", "warm", ("Terracota", "Coral"))
FILTERS = {"section": "Unisex", "category": "Camisa", "color": "Azul", "style": "Formal"}


def product(product_id, color="Negro", style="Casual", discount=None):
    return Product(
        id=product_id, name=product_id, category="Camisa", section="Mujer", brand="Marca", color=color,
        price=Decimal("10"), image_url="/x.png", product_url="https://x", style=style, discount=discount,
    )


def catalog(size=7):
    return [product(f"p{i}") for i in range(size)]


def test_returns_exactly_five_with_position_classification():
    result = rank(catalog(), ANALYSIS, FILTERS)
    assert [item["classification"] for item in result] == ["green", "green", "yellow", "yellow", "red"]


def test_orders_from_highest_to_lowest_score():
    products = [product("nada"), product("favorable", color="Coral"), product("pedido", color="Azul", style="Formal")]
    result = rank(products, ANALYSIS, FILTERS)
    assert [item["product"].id for item in result] == ["favorable", "pedido", "nada"]
    scores = [item["score"] for item in result]
    assert scores == sorted(scores, reverse=True)


def test_recommended_and_requested_color_reach_maximum():
    result = rank([product("a", color="Azul", style="Formal")], ColorAnalysis("x", "cool", ("Azul",)), FILTERS)
    assert result[0]["score"] == 100


def test_discount_breaks_ties():
    result = rank([product("sin"), product("con", discount=20)], ANALYSIS, FILTERS)
    assert result[0]["product"].id == "con"


def test_does_not_invent_products_when_there_are_few():
    assert len(rank(catalog(3), ANALYSIS, FILTERS)) == 3


def test_empty_catalog_returns_empty_list():
    assert rank([], ANALYSIS, FILTERS) == []


def test_find_by_id_only_finds_recommended_products():
    result = rank(catalog(), ANALYSIS, FILTERS)
    assert find_by_id(result, result[0]["product"].id) is result[0]
    assert find_by_id(result, "otro") is None
