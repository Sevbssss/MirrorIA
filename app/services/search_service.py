"""RF-02: interpreta la consulta con diccionarios y reglas, y obtiene productos del catálogo."""
import re
import unicodedata

from app.models.product import Product
from app.models.user_session import UserSession
from app.scraping import deprati_scraper, product_parser
from app.scraping.deprati_scraper import CatalogError
from app.services import recommendation_service

MAX_QUERY_LENGTH = 300
DEFAULT_SECTION = "Unisex"
NO_PRODUCTS_MESSAGE = "No encontramos prendas que coincidan con tu búsqueda."

SECTIONS = {
    "Mujer": r"mujer(es)?|dama(s)?|femenin[oa]s?|chica(s)?",
    "Hombre": r"hombre(s)?|caballero(s)?|masculin[oa]s?|chico(s)?",
    "Unisex": r"unisex",
}
CATEGORIES = {
    "Camisa": r"camisa(s)?|blusa(s)?",
    "Pantalón": r"pantalon(es)?|jean(s)?",
    "Short": r"short(s)?|bermuda(s)?|pantaloneta(s)?",
}
COLORS = {
    "Azul": r"azul(es)?",
    "Celeste": r"celeste(s)?",
    "Blanco": r"blanc[oa]s?",
    "Negro": r"negr[oa]s?",
    "Gris": r"gris(es)?",
    "Beige": r"beige(s)?|crema",
    "Verde": r"verde(s)?",
    "Terracota": r"terracota(s)?",
    "Coral": r"coral(es)?",
    "Vino": r"vino|vinotinto",
}
STYLES = {
    "Formal": r"formal(es)?|elegante(s)?|oficina|trabajo|entrevista",
    "Casual": r"casual(es)?|informal(es)?|diario|fin de semana",
    "Deportivo": r"deportiv[oa]s?|deporte(s)?|gimnasio|gym",
    "Fiesta": r"fiesta(s)?|evento(s)?|noche",
}


class SearchError(Exception):
    """La consulta no se puede interpretar; el mensaje se puede mostrar al usuario."""


def parse_query(text: str) -> dict:
    """Convierte una frase en filtros, por ejemplo {"section": "Mujer", "category": "Camisa",
    "color": "Azul", "style": "Formal"}. Lo que la frase no indique queda en None."""
    normalized = _normalize(text)
    return {
        "section": _find(SECTIONS, normalized) or DEFAULT_SECTION,
        "category": _find(CATEGORIES, normalized),
        "color": _find(COLORS, normalized),
        "style": _find(STYLES, normalized),
    }


def interpret(user_session: UserSession, query: str) -> dict:
    """Valida la consulta, la interpreta y guarda el resultado en la sesión."""
    query = (query or "").strip()
    if not query:
        raise SearchError("Escribe qué prenda buscas, por ejemplo: camisa azul para una ocasión formal.")
    if len(query) > MAX_QUERY_LENGTH:
        raise SearchError(f"La búsqueda es muy larga. Usa hasta {MAX_QUERY_LENGTH} caracteres.")

    filters = parse_query(query)
    if filters["category"] is None:
        raise SearchError("Por ahora buscamos camisas, pantalones y shorts. Indica cuál de ellos quieres.")
    user_session.search_query = query
    user_session.search_filters = filters
    user_session.recommended_products = []
    return filters


def run_search(user_session: UserSession, query: str, base_url: str) -> None:
    """Interpreta la consulta, obtiene los productos y guarda las recomendaciones en la sesión."""
    filters = interpret(user_session, query)
    try:
        products = find_products(filters, base_url)
    except CatalogError as error:
        user_session.recommended_products = []
        raise SearchError(str(error)) from error
    user_session.recommended_products = recommendation_service.rank(
        products, user_session.color_analysis, filters
    )
    if not user_session.recommended_products:
        raise SearchError(NO_PRODUCTS_MESSAGE)


def find_products(filters: dict, base_url: str) -> list[Product]:
    """Consulta el catálogo y deja los productos de la sección pedida, sin repetir prendas."""
    products = product_parser.parse_products(deprati_scraper.fetch_catalog(filters["category"], base_url))
    section = filters["section"]
    if section == DEFAULT_SECTION:
        return list({product.name: product for product in reversed(products)}.values())
    return [product for product in products if product.section in (section, DEFAULT_SECTION)]


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _find(options: dict[str, str], text: str) -> str | None:
    for name, pattern in options.items():
        if re.search(rf"\b(?:{pattern})\b", text):
            return name
    return None
