"""Catálogo de ejemplo y conversión al modelo Product."""
from decimal import Decimal

import pytest

from app.scraping.deprati_scraper import CatalogError, fetch_catalog
from app.scraping.product_parser import parse_products

BASE_URL = "https://www.deprati.com.ec"


@pytest.mark.parametrize("category", ["Camisa", "Pantalón", "Short"])
def test_catalog_parses_and_is_marked_as_mock(category):
    products = parse_products(fetch_catalog(category, BASE_URL))
    assert len(products) >= 5
    assert all(product.is_mock and product.category == category for product in products)
    assert len({product.id for product in products}) == len(products)


def test_unknown_category_raises_controlled_error():
    with pytest.raises(CatalogError):
        fetch_catalog("Zapatos", BASE_URL)


def test_discount_keeps_previous_price_higher():
    for product in parse_products(fetch_catalog("Camisa", BASE_URL)):
        if product.discount:
            assert product.previous_price > product.price
        else:
            assert product.previous_price is None


def test_parser_discards_incomplete_items():
    valid = fetch_catalog("Camisa", BASE_URL)[0]
    assert parse_products([{"id": "1"}, {**valid, "price": "gratis"}, valid])[0].price == Decimal(str(valid["price"]))
    assert len(parse_products([{"id": "1"}, {**valid, "price": "gratis"}, valid])) == 1


def test_all_product_images_exist(client):
    for category in ("Camisa", "Pantalón", "Short"):
        for item in fetch_catalog(category, BASE_URL):
            assert client.get(item["image_url"]).status_code == 200
