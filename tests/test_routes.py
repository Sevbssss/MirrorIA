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


def test_search_escapes_user_text(confirmed_client):
    html = confirmed_client.post(
        "/buscar/", data={"query": "camisa <script>alert(1)</script>"}, follow_redirects=True
    ).get_data(as_text=True)
    assert "<script>alert(1)" not in html
