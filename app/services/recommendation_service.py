"""RF-03: ordena por afinidad y devuelve hasta cinco prendas; nunca completa con productos ficticios."""
from app.models.color_analysis import ColorAnalysis
from app.models.product import Product

CLASSIFICATIONS = ("green", "green", "yellow", "yellow", "red")
BASE_SCORE = 10
RECOMMENDED_COLOR_POINTS = 45
REQUESTED_COLOR_POINTS = 30
REQUESTED_STYLE_POINTS = 15


def rank(products: list[Product], analysis: ColorAnalysis, filters: dict) -> list[dict]:
    """Devuelve [{"product", "score", "classification"}] de mayor a menor afinidad.

    El descuento solo desempata; la clasificación depende de la posición en la lista.
    """
    ordered = sorted(
        ((product, _score(product, analysis, filters)) for product in products),
        key=lambda item: (-item[1], -(item[0].discount or 0), item[0].id),
    )
    return [
        {"product": product, "score": score, "classification": classification}
        for (product, score), classification in zip(ordered, CLASSIFICATIONS)
    ]


def find_by_id(recommendations: list[dict], product_id: str | None) -> dict | None:
    return next((item for item in recommendations if item["product"].id == product_id), None)


def _score(product: Product, analysis: ColorAnalysis, filters: dict) -> int:
    score = BASE_SCORE
    if product.color in analysis.recommended_colors:
        score += RECOMMENDED_COLOR_POINTS
    if product.color == filters.get("color"):
        score += REQUESTED_COLOR_POINTS
    if product.style == filters.get("style"):
        score += REQUESTED_STYLE_POINTS
    return score
