"""RF-02 y RF-05: datos normalizados del producto, sin operaciones de compra."""
from dataclasses import dataclass
from decimal import Decimal
@dataclass(frozen=True)
class Product:
    id: str
    name: str
    category: str
    brand: str
    price: Decimal
    image_url: str
    purchase_url: str
    discount: str | None = None
