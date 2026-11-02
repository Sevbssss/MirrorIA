"""Presentación: mostrará la ficha de compra de productos mediante servicios."""
from flask import Blueprint, render_template

products_bp = Blueprint("products", __name__, url_prefix="/ficha")


@products_bp.get("/")
def detail():
    return render_template("product_detail.html")
