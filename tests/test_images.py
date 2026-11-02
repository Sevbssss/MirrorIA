"""Validación de fotografías: nada se escribe en disco y los errores son claros."""
from pathlib import Path

import pytest

from app import create_app
from app.services.image_service import PhotoError, validate_photo
from tests.conftest import image_bytes, photo_upload

MAX_BYTES = 1024 * 1024


@pytest.mark.parametrize("name, image_format", [("a.jpg", "JPEG"), ("a.jpeg", "JPEG"), ("a.PNG", "PNG")])
def test_accepts_allowed_images(name, image_format):
    assert validate_photo(name, image_bytes(image_format), MAX_BYTES).startswith(b"\xff\xd8")


@pytest.mark.parametrize("name", ["a.gif", "a.exe", "a.jpg.exe", "sin_extension", ""])
def test_rejects_disallowed_extensions(name):
    with pytest.raises(PhotoError):
        validate_photo(name, image_bytes(), MAX_BYTES)


@pytest.mark.parametrize(
    "name, data",
    [
        ("a.png", b""),
        ("a.png", b"esto no es una imagen"),
        ("a.png", image_bytes("GIF")),
        ("a.png", image_bytes(size=(50, 50))),
    ],
)
def test_rejects_invalid_content(name, data):
    with pytest.raises(PhotoError):
        validate_photo(name, data, MAX_BYTES)


def test_rejects_oversized_file():
    with pytest.raises(PhotoError, match="supera"):
        validate_photo("a.png", image_bytes(), 10)


def test_upload_missing_photo_explains_problem(client):
    response = client.post(
        "/fotografias/", data={"face": photo_upload()}, content_type="multipart/form-data", follow_redirects=True
    )
    assert "Falta la foto de cuerpo completo" in response.get_data(as_text=True)


def test_invalid_photo_does_not_replace_stored_one(client_with_photos):
    before = client_with_photos.get("/fotografias/vista-previa/face").data
    client_with_photos.post(
        "/fotografias/",
        data={"face": photo_upload(content=b"basura")},
        content_type="multipart/form-data",
    )
    assert client_with_photos.get("/fotografias/vista-previa/face").data == before


def test_preview_is_private_to_each_session(client_with_photos):
    assert client_with_photos.get("/fotografias/vista-previa/face").status_code == 200
    assert create_app().test_client().get("/fotografias/vista-previa/face").status_code == 404


def test_photos_are_not_written_to_disk(client_with_photos):
    uploads = Path(create_app().config["UPLOAD_FOLDER"])
    assert not any(uploads.iterdir())
