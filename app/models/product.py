"""RF-02 y RF-05: datos normalizados del producto, sin operaciones de compra."""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    category: str
    section: str
    brand: str
    color: str
    price: Decimal
    image_url: str
    product_url: str
    previous_price: Decimal | None = None
    discount: int | None = None
    style: str | None = None
    material: str | None = None
    size: str | None = None
    availability: str | None = None
    is_mock: bool = False
