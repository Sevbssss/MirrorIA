"""Punto de entrada del servidor Flask."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
