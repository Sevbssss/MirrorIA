"""Fixtures compartidas de las pruebas."""
import io

import pytest
from PIL import Image

from app import create_app


def image_bytes(image_format: str = "PNG", size: tuple[int, int] = (300, 400)) -> bytes:
    output = io.BytesIO()
    Image.new("RGB", size, (200, 150, 130)).save(output, format=image_format)
    return output.getvalue()


def photo_upload(name: str = "foto.png", content: bytes | None = None) -> tuple:
    return (io.BytesIO(image_bytes() if content is None else content), name)


@pytest.fixture
def client():
    return create_app().test_client()


@pytest.fixture
def client_with_photos(client):
    response = client.post(
        "/fotografias/",
        data={"face": photo_upload(), "body": photo_upload()},
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    return client


@pytest.fixture
def confirmed_client(client_with_photos):
    assert client_with_photos.post("/fotografias/confirmar").status_code == 302
    return client_with_photos
