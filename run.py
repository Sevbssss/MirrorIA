"""Entrada local del maquetado. No usar el servidor de desarrollo en producción."""
from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=False)
