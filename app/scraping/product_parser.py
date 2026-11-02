"""Normaliza los datos crudos del catálogo a Product; sin lógica cromática."""
from decimal import Decimal, InvalidOperation

from app.models.product import Product

OPTIONAL_TEXT = ("style", "material", "size", "availability")
REQUIRED_TEXT = ("id", "name", "brand", "category", "section", "color", "image_url", "product_url")


def parse_products(items: list[dict]) -> list[Product]:
    """Convierte los datos a Product y descarta los incompletos o con precio inválido."""
    products = (_parse_item(item) for item in items)
    return [product for product in products if product is not None]


def _parse_item(item: dict) -> Product | None:
    if not all(item.get(key) for key in REQUIRED_TEXT):
        return None
    try:
        price = Decimal(str(item["price"]))
        previous = item.get("previous_price")
        previous_price = Decimal(str(previous)) if previous is not None else None
    except (KeyError, InvalidOperation):
        return None
    return Product(
        **{key: item[key] for key in REQUIRED_TEXT},
        **{key: item.get(key) for key in OPTIONAL_TEXT},
        price=price,
        previous_price=previous_price,
        discount=item.get("discount"),
        is_mock=bool(item.get("is_mock")),
    )
