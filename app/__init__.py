"""Application Factory: ensambla módulos en una única aplicación desplegable."""
from flask import Flask
from config import Config
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    from app.views import home, photos, search, tryon, products
    for module in (home, photos, search, tryon, products):
        app.register_blueprint(module.bp)
    return app
