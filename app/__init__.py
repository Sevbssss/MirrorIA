"""Composición del monolito modular mediante una fábrica Flask."""
from pathlib import Path

from flask import Flask

from app.views.home import home_bp
from app.views.photos import photos_bp
from app.views.products import products_bp
from app.views.search import search_bp
from app.views.tryon import tryon_bp
from config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    _create_temp_folders(app)
    _register_blueprints(app)
    return app


def _create_temp_folders(app: Flask) -> None:
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    (Path(app.static_folder) / "generated").mkdir(parents=True, exist_ok=True)


def _register_blueprints(app: Flask) -> None:
    for blueprint in (home_bp, photos_bp, search_bp, tryon_bp, products_bp):
        app.register_blueprint(blueprint)
