# Mirror IA

Aplicación web universitaria (Flask) de recomendación de prendas, colorimetría y probador virtual aproximado, con catálogo de DePrati. Mirror IA no procesa pagos: la compra continúa en DePrati.

El detalle funcional está en `docs/especificacion.md`. Léelo solo al trabajar en la fase correspondiente.

## Cómo trabajar

- Trabaja **una fase a la vez** y detente al terminar. No avances a la siguiente sin que yo lo pida.
- Primer turno de la sesión: inspecciona el repositorio, muestra la estructura encontrada y qué falta. En turnos siguientes no repitas la inspección.
- Construye primero una versión ejecutable mínima (`python run.py`) y agrega módulos de forma progresiva.
- No elimines archivos útiles ni renombres módulos sin necesidad.
- Si encuentras un problema técnico real que obligue a cambiar la arquitectura, explícalo antes de modificarla.

## Arquitectura (no cambiar)

**Cliente–Servidor + Arquitectura en Capas + Monolito Modular**, con **MVT adaptado a Flask** y una capa de **Services**.

- Cliente: navegador (HTML, CSS, JavaScript). Servidor: Python + Flask. Comunicación HTTP.
- Una sola solución desplegable, separada internamente por responsabilidades. **Sin microservicios.**

Capas:

1. **Presentación:** `views/` (Blueprints) y `templates/` (Jinja2). Rutas, formularios, navegación, mensajes de error.
2. **Lógica de negocio:** `services/`. Fotos, colorimetría, interpretación de búsquedas, recomendaciones, ranking, probador virtual.
3. **Datos e integración:** `models/`, sesión temporal, archivos temporales, `scraping/`.

Flujo de una solicitud:

Usuario → Template → View → Service → Model / integración → Service → View → Template → Usuario.

Reglas MVT:

- **Model:** representa el dominio (Product, ColorAnalysis, UserSession).
- **View:** recibe la solicitud HTTP, llama al service y elige el template. **Sin lógica de negocio compleja.**
- **Template:** solo HTML con Jinja2.
- **Service:** toda la lógica de negocio.

## Estructura de carpetas

```
Mirror-IA/
├── run.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py          # create_app() (Application Factory)
│   ├── models/              # product.py, color_analysis.py, user_session.py
│   ├── views/               # home.py, photos.py, search.py, tryon.py, products.py
│   ├── services/            # image_service.py, colorimetry_service.py, search_service.py,
│   │                        # recommendation_service.py, tryon_service.py
│   ├── scraping/            # deprati_scraper.py, product_parser.py
│   ├── templates/           # base.html, index.html, photos.html, confirm_photos.html,
│   │                        # search.html, tryon.html, product_detail.html
│   └── static/              # css/styles.css, js/app.js, img/, uploads/, generated/
└── tests/                   # test_search.py, test_recommendations.py, test_routes.py
```

Puedes añadir archivos necesarios, pero no rompas esta organización.

Blueprints: `home_bp`, `photos_bp`, `search_bp`, `tryon_bp`, `products_bp`. Nunca todas las rutas en un solo archivo.

## Alcance

Categorías: camisas, pantalones y shorts. Una sola tienda: DePrati. Sesión temporal del usuario.

**No implementar:** cuentas, autenticación, historial, carrito, pagos, realidad aumentada en tiempo real, 3D, video, cálculo exacto de talla, múltiples tiendas.

**No añadir** (sin mi autorización): Docker, Kubernetes, Redis, RabbitMQ, Celery, React, Vue ni bases de datos complejas. Buscamos una solución universitaria: ordenada, funcional, entendible, demostrable y sin sobreingeniería.

## Flujo funcional

Landing → Tus fotografías → Confirmar fotografías → Buscar prendas → Resumen del análisis → Probador virtual → Ficha de compra → DePrati.

Barra de progreso visible, solo estas 4 etapas: **1. Tus fotografías · 2. Buscar prendas · 3. Probador virtual · 4. Ficha de compra.** No existe una etapa "Recomendaciones".

## Reglas de código

- Funciones pequeñas, nombres comprensibles, sin duplicación.
- Type hints cuando ayuden. Docstrings en servicios importantes. Comentarios solo si aportan valor.
- No mezclar HTML con lógica Python.
- No mezclar scraping con rutas, ni procesamiento de imágenes con Views.
- Colorimetría, scraping y probador virtual deben ser **reemplazables**: aislados detrás de un servicio, con implementación mock claramente identificada mientras no exista la real.
- Nunca mostrar tracebacks al usuario: errores controlados con mensajes claros.
- Python 3.10 o 3.11. `requirements.txt` solo con dependencias realmente usadas.
- Tests con pytest.

## Seguridad y configuración

`secure_filename`, extensiones permitidas (JPG, JPEG, PNG), límite de tamaño, nombres únicos de archivo, nunca ejecutar archivos subidos, rutas seguras. `SECRET_KEY`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH` y `DEPRATI_BASE_URL` vienen de variables de entorno (`.env`, con `.env.example` en el repo). Sin credenciales en el repositorio. No guardar fotos de forma permanente.

## Diseño

Responsive (desktop y móvil) con Flexbox, Grid y media queries. Una sola aplicación.

Paleta: `#911717` `#B34A3D` `#D67C63` `#F0A98B` `#F7CCB8` `#FBE0D2` `#FCEDE5` `#FEF7F3` `#FFFFFF` `#3A0909` `#F1F3F6`

## Fases

1. Estructura, Application Factory, Blueprints, templates base y navegación.
2. Carga y confirmación de fotografías.
3. Búsqueda conversacional.
4. Scraper y productos (**empezar con datos mock**).
5. Recomendaciones.
6. Colorimetría.
7. Probador virtual.
8. Ficha de compra.
9. Validaciones, errores, responsive y pruebas.

## Debo poder explicar en la exposición

Por qué Cliente–Servidor, por qué Capas, por qué Monolito Modular, qué hace MVT, qué hace Services, qué hace cada carpeta y cómo viaja una solicitud desde el navegador hasta los servicios y de vuelta.
