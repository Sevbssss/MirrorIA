"""RF-02: frontera hacia el catálogo de DePrati. IMPLEMENTACIÓN MOCK TEMPORAL.

DePrati prohíbe /search en robots.txt y responde con un desafío antibot de Cloudflare, así
que no se consulta el sitio real. Estos datos son de ejemplo: nombres y precios no son reales.
Para usar una fuente autorizada basta con reemplazar fetch_catalog; el resto no cambia.
"""
SECTIONS = ("Mujer", "Hombre")
COLORS = ("Azul", "Celeste", "Blanco", "Negro", "Gris", "Beige", "Verde", "Terracota", "Coral", "Vino")
CATALOG = {
    "Camisa": {"slug": "camisa", "styles": ("Formal", "Casual", "Fiesta"), "base_price": 29.90, "material": "Algodón"},
    "Pantalón": {"slug": "pantalon", "styles": ("Formal", "Casual", "Fiesta"), "base_price": 39.90, "material": "Gabardina"},
    "Short": {"slug": "short", "styles": ("Casual", "Deportivo", "Casual"), "base_price": 19.90, "material": "Algodón"},
}
DISCOUNTS = (None, 10, None, 20, None, 30)


class CatalogError(Exception):
    """El catálogo no está disponible; el mensaje se puede mostrar al usuario."""


def fetch_catalog(category: str, base_url: str) -> list[dict]:
    """Devuelve los datos crudos de la categoría."""
    definition = CATALOG.get(category)
    if definition is None:
        raise CatalogError("Esa categoría no está disponible en el catálogo.")
    return [
        _mock_item(category, definition, section, color, index, base_url)
        for section in SECTIONS
        for index, color in enumerate(COLORS)
    ]


def _mock_item(category: str, definition: dict, section: str, color: str, index: int, base_url: str) -> dict:
    previous = round(definition["base_price"] + index * 2, 2)
    discount = DISCOUNTS[index % len(DISCOUNTS)]
    style = definition["styles"][index % len(definition["styles"])]
    color_slug = color.lower()
    return {
        "id": f"mock-{definition['slug']}-{section.lower()}-{color_slug}",
        "name": f"{category} {style.lower()} {color_slug}",
        "brand": "Marca de ejemplo",
        "category": category,
        "section": section,
        "color": color,
        "style": style,
        "price": round(previous * (100 - discount) / 100, 2) if discount else previous,
        "previous_price": previous if discount else None,
        "discount": discount,
        "image_url": f"/static/img/products/{definition['slug']}_{color_slug}.png",
        "product_url": base_url,
        "material": definition["material"],
        "size": "S, M, L",
        "availability": "Disponible (dato de ejemplo)",
        "is_mock": True,
    }
