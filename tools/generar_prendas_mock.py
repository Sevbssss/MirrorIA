"""Genera las siluetas PNG de las prendas de ejemplo. Ejecutar: python tools/generar_prendas_mock.py"""
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parents[1] / "app" / "static" / "img" / "products"
SIZE = (400, 500)
COLORS = {
    "azul": (38, 70, 140),
    "celeste": (135, 190, 225),
    "blanco": (240, 240, 236),
    "negro": (35, 35, 38),
    "gris": (130, 134, 140),
    "beige": (214, 195, 160),
    "verde": (55, 110, 75),
    "terracota": (178, 90, 60),
    "coral": (232, 118, 98),
    "vino": (110, 25, 45),
}
SHAPES = {
    "camisa": [(130, 30), (270, 30), (390, 110), (345, 190), (300, 150), (300, 470), (100, 470), (100, 150), (55, 190), (10, 110)],
    "pantalon": [(110, 20), (290, 20), (330, 480), (225, 480), (200, 170), (175, 480), (70, 480)],
    "short": [(90, 30), (310, 30), (360, 330), (225, 330), (200, 140), (175, 330), (40, 330)],
}


def draw_garment(shape: list, color: tuple) -> Image.Image:
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.polygon(shape, fill=(*color, 255))
    outline = tuple(max(channel - 35, 0) for channel in color) + (255,)
    draw.line(shape + shape[:1], fill=outline, width=4, joint="curve")
    return image


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for category, shape in SHAPES.items():
        for name, color in COLORS.items():
            draw_garment(shape, color).save(OUTPUT / f"{category}_{name}.png", optimize=True)


if __name__ == "__main__":
    main()
