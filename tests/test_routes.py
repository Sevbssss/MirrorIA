"""Rutas principales y navegación de la Fase 1."""
import re
from pathlib import Path

import pytest

from app import create_app

SCREENS = [
    "/",
    "/fotografias/",
    "/fotografias/confirmar",
    "/buscar/",
    "/probador/",
    "/ficha/",
]
PROGRESS_LABELS = ["Tus fotografías", "Buscar prendas", "Probador virtual", "Ficha de compra"]


@pytest.fixture
def client():
    return create_app().test_client()


@pytest.mark.parametrize("path", SCREENS)
def test_screen_renders(client, path):
    assert client.get(path).status_code == 200


@pytest.mark.parametrize("path", SCREENS)
def test_internal_links_work(client, path):
    html = client.get(path).get_data(as_text=True)
    for link in re.findall(r'(?:href|src)="(/[^"#]*)', html):
        assert client.get(link).status_code == 200, link


@pytest.mark.parametrize(
    "path, step",
    [
        ("/fotografias/", 1),
        ("/fotografias/confirmar", 1),
        ("/buscar/", 2),
        ("/probador/", 3),
        ("/ficha/", 4),
    ],
)
def test_progress_bar_marks_current_step(client, path, step):
    html = client.get(path).get_data(as_text=True)
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
