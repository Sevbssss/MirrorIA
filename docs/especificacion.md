# Mirror IA: especificación funcional

Guardar como `docs/especificacion.md`. Claude Code debe leer solo la sección de la fase en curso. La arquitectura y las reglas generales están en `CLAUDE.md`.

## 1. Objetivo del usuario

1. Entra por la landing.
2. Carga dos fotografías: rostro frontal (colorimetría) y cuerpo completo frontal (probador virtual).
3. Revisa y confirma ambas.
4. Busca prendas de forma conversacional.
5. El sistema obtiene prendas reales de DePrati y las analiza según su colorimetría.
6. Recibe **exactamente 5 prendas** ordenadas por afinidad.
7. Elige una, ve una visualización aproximada sobre su foto y la ficha del producto.
8. Continúa la compra en DePrati.

## 2. Fotografías (Fase 2) — `image_service.py`

- Foto 1 (colorimetría): rostro visible, frontal, buena iluminación.
- Foto 2 (probador): cuerpo completo, frontal, postura neutra.
- Opciones en la UI: usar cámara o subir imagen.
- Validaciones: archivo existente, extensión (JPG, JPEG, PNG), tamaño máximo, archivo legible (abrir con Pillow).
- Archivos guardados con nombre único en `static/uploads/`, con estrategia de limpieza de temporales.
- Si falla: mostrar explicación clara y opción de intentar de nuevo o volver a cargar.

Pantallas: `photos.html` (dos tarjetas) y `confirm_photos.html` (vista previa de ambas; volver a tomar, regresar, continuar).

## 3. Búsqueda conversacional (Fase 3) — `search_service.py`

Entrada de ejemplo: "Quiero una camisa azul para una ocasión formal."

Salida:

```python
{"section": "Mujer", "category": "Camisa", "color": "Azul", "style": "Formal"}
```

- `section`: Mujer, Hombre o Unisex. `category`: camisa, pantalón o short.
- Primera versión: palabras clave, expresiones regulares, diccionarios y reglas. No requiere LLM.
- Debe poder reemplazarse después por una solución más avanzada sin tocar las Views.

Pantalla `search.html`: interfaz tipo chat que muestra análisis básico, colores sugeridos, filtros detectados, productos encontrados y botón para ir al probador.

## 4. Scraping y productos (Fase 4) — `scraping/`

- `deprati_scraper.py`: accede al catálogo, busca productos, recupera HTML/datos, maneja errores de navegación.
- `product_parser.py`: convierte los resultados al modelo interno `Product`.
- Tecnologías posibles: requests, BeautifulSoup, Selenium.
- DePrati puede usar contenido dinámico y antibot, por lo que: timeouts, sin loops infinitos, errores controlados y **resultados mock para desarrollo (usar mock primero)**.
- El scraper debe poder reemplazarse sin afectar el resto. Nunca llamarlo desde una View directamente; siempre vía service.

Product:

```python
{"id": "...", "name": "Camisa Oxford", "brand": "DePrati", "price": 39.99,
 "previous_price": 49.99, "discount": 20, "color": "Azul",
 "category": "Camisa", "section": "Mujer",
 "image_url": "...", "product_url": "..."}
```

Para la ficha, material, talla y disponibilidad se muestran solo si están disponibles.

## 5. Recomendaciones (Fase 5) — `recommendation_service.py`

Entrada: análisis de colorimetría, productos obtenidos y criterios de búsqueda. Salida: **exactamente 5 productos**, de mayor a menor afinidad.

```python
[{"product": {...}, "score": 92, "classification": "green"}]
```

| Posiciones | Clasificación | Afinidad |
|---|---|---|
| 1 y 2 | green | mayor |
| 3 y 4 | yellow | media |
| 5 | red | menor |

Primera versión: puntuación basada en reglas (coincidencia del color del producto con `recommended_colors`, coincidencia con filtros de búsqueda, descuento como desempate). Debe poder evolucionar.

## 6. Colorimetría (Fase 6) — `colorimetry_service.py`

Entrada: foto facial. Salida:

```python
{"skin_tone": "...", "undertone": "warm-neutral",
 "recommended_colors": ["terracotta", "coral", "warm beige", "brick red"]}
```

- Versión real: OpenCV + MediaPipe Face Mesh.
- Mientras no exista, usar una implementación **mock claramente identificada** como temporal.
- Aislada del resto del sistema; no mezclar con rutas.

## 7. Probador virtual (Fase 7) — `tryon_service.py`

Entrada: foto corporal y producto seleccionado. Salida: visualización aproximada en `static/generated/`.

- Versión inicial: MediaPipe Pose + OpenCV, landmarks, torso aproximado, redimensionar la prenda y superponer.
- Mostrar siempre: "La representación es aproximada y no representa talla, ajuste ni caída exactos."
- Desacoplado para poder reemplazarlo por una API de Virtual Try-On con IA.

Pantalla `tryon.html`:

- Modal inicial "Resumen del análisis": sección, subtono, colores favorables, categoría, color y ocasión/estilo.
- Foto corporal con la prenda seleccionada.
- Exactamente 5 recomendaciones con semáforo.
- Botones "Ver ficha de compra" y "Probar otra prenda".

## 8. Ficha de compra (Fase 8) — `product_detail.html`

Imagen, nombre, marca, precio, precio anterior (si existe), descuento, color, material, talla, disponibilidad, afinidad y botón "Ir a DePrati" (enlace externo). Mirror IA no procesa pagos.

## 9. Modelos y sesión

- `Product`: id, name, brand, price, previous_price, discount, image_url, product_url, color, category, section.
- `ColorAnalysis`: skin_tone, undertone, recommended_colors.
- `UserSession`: face_photo, body_photo, color_analysis, search_filters, recommended_products, selected_product, generated_tryon.
- Sesión temporal con Flask session, archivos temporales o estructuras internas. Sin base de datos compleja ni usuarios persistentes.

## 10. Manejo de errores (Fase 9)

| Situación | Comportamiento |
|---|---|
| Error al cargar foto | Explicación + intentar de nuevo |
| Imagen no procesable | Explicación + volver a cargar |
| Sin productos | "No encontramos prendas que coincidan con tu búsqueda." + modificar búsqueda o reintentar |
| Error de scraping | Respuesta controlada, nunca traceback |

## 11. Landing (`index.html`)

Hero, CTA, "Cómo funciona", características principales, "Sobre nosotros" y footer.

## 12. Tests (pytest)

Parser de búsquedas, ranking de recomendaciones, rutas principales y validación de imágenes. No se exige cobertura total.

## 13. README

Descripción, arquitectura, requisitos, instalación, entorno virtual, dependencias, ejecución, estructura de carpetas, limitaciones actuales y funcionalidades pendientes.

## 14. Dependencias posibles

Flask, python-dotenv, opencv-python, mediapipe, selenium, beautifulsoup4, requests, Pillow. Agregar solo las que se usen realmente.
