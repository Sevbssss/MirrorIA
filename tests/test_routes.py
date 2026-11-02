"""Rutas principales, orden del flujo y navegación."""
import re
from pathlib import Path

import pytest

from app import create_app

SCREENS = ["/", "/fotografias/", "/fotografias/confirmar", "/buscar/", "/probador/", "/ficha/"]
PROGRESS_LABELS = ["Tus fotografías", "Buscar prendas", "Probador virtual", "Ficha de compra"]


@pytest.mark.parametrize("path", ["/", "/fotografias/", "/probador/", "/ficha/"])
def test_open_screens_render(client, path):
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("path", ["/fotografias/confirmar", "/buscar/"])
def test_flow_screens_require_photos(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/fotografias/")


@pytest.mark.parametrize("path", SCREENS)
def test_internal_links_work(confirmed_client, path):
    html = confirmed_client.get(path).get_data(as_text=True)
    for link in re.findall(r'(?:href|src)="(/[^"#]*)', html):
        assert confirmed_client.get(link).status_code == 200, link


@pytest.mark.parametrize(
    "path, step",
    [("/fotografias/", 1), ("/fotografias/confirmar", 1), ("/buscar/", 2), ("/probador/", 3), ("/ficha/", 4)],
)
def test_progress_bar_marks_current_step(confirmed_client, path, step):
    html = confirmed_client.get(path).get_data(as_text=True)
    assert re.findall(r'progress__label">([^<]+)<', html) == PROGRESS_LABELS
    current = re.search(r'aria-current="step">\s*<span class="progress__number">(\d)<', html)
    assert int(current.group(1)) == step


def test_landing_has_required_sections(client):
    html = client.get("/").get_data(as_text=True)
    for text in ["Comenzar", "Cómo funciona", "Características principales", "Sobre nosotros", "<footer"]:
        assert text in html


def test_temp_folders_exist():
    app = create_app()
    assert Path(app.config["UPLOAD_FOLDER"]).is_dir()
    assert (Path(app.static_folder) / "generated").is_dir()


def test_search_shows_detected_filters(confirmed_client):
    response = confirmed_client.post(
        "/buscar/", data={"query": "Quiero una camisa azul formal para mujer"}, follow_redirects=True
    )
    html = response.get_data(as_text=True)
    for text in ["Mujer", "Camisa", "Azul", "Formal"]:
        assert f"<dd>{text}</dd>" in html


def test_search_without_category_explains_problem(confirmed_client):
    html = confirmed_client.post("/buscar/", data={"query": "algo azul"}, follow_redirects=True).get_data(as_text=True)
    assert "Indica cuál de ellos quieres" in html


def test_search_returns_five_recommendations(confirmed_client):
    html = confirmed_client.post("/buscar/", data={"query": "un short"}, follow_redirects=True).get_data(as_text=True)
    classifications = re.findall(r'data-classification="(\w+)"', html)
    assert classifications == ["green", "green", "yellow", "yellow", "red"]
    assert "Productos de ejemplo" in html


def test_search_respects_requested_section():
    from app.services.search_service import find_products

    products = find_products({"section": "Hombre", "category": "Camisa"}, "https://x")
    assert products and all(product.section == "Hombre" for product in products)


def test_search_without_section_does_not_repeat_garments():
    from app.services.search_service import find_products

    names = [product.name for product in find_products({"section": "Unisex", "category": "Camisa"}, "https://x")]
    assert len(names) >= 5 and len(names) == len(set(names))


def test_catalog_failure_is_controlled(confirmed_client, monkeypatch):
    from app.scraping import deprati_scraper

    def fail(*_args):
        raise deprati_scraper.CatalogError("El catálogo no está disponible.")

    monkeypatch.setattr(deprati_scraper, "fetch_catalog", fail)
    response = confirmed_client.post("/buscar/", data={"query": "un short"}, follow_redirects=True)
    assert response.status_code == 200
    assert "El catálogo no está disponible." in response.get_data(as_text=True)


def test_face_analysis_failure_returns_to_photos(client_with_photos):
    response = client_with_photos.post("/fotografias/confirmar", follow_redirects=True)
    assert "No detectamos un rostro" in response.get_data(as_text=True)


def test_search_escapes_user_text(confirmed_client):
    html = confirmed_client.post(
        "/buscar/", data={"query": "camisa <script>alert(1)</script>"}, follow_redirects=True
    ).get_data(as_text=True)
    assert "<script>alert(1)" not in html
