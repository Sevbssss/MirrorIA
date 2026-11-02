# Mirror IA — Maquetado de arquitectura

Estructura inicial, sin implementación de la aplicación completa.

## Arquitectura seleccionada

**Cliente–Servidor + En Capas + Monolito Modular**, con **MVT adaptado a Flask + Services**.

- Cliente: navegador que recibe HTML y recursos CSS, JavaScript e imágenes.
- Servidor: una aplicación Flask, desplegable como una sola unidad.
- Presentación: `app/views/` contiene rutas/controladores HTTP; `app/templates/` contiene las plantillas y `app/static/` los recursos del cliente.
- Aplicación y negocio: `app/services/` coordina los casos de uso y las reglas del sistema.
- Modelos: `app/models/` representa datos del dominio. La persistencia aún no está definida ni implementada.
- Integración externa: `app/scraping/` aísla la obtención y transformación de datos del catálogo externo.

En esta adaptación de MVT, los modelos representan el dominio, las views gestionan solicitudes Flask y los templates representan la interfaz. Services mantiene la lógica fuera de las rutas. Flask no impone este patrón: es la organización elegida para el proyecto.

## Flujo y límites

Navegador → HTTP/HTTPS → views → services → modelos / integración externa → respuesta / templates.
Las plantillas no consultan fuentes externas. Los scrapers no dependen de las rutas. Todos los módulos pertenecen al mismo monolito; no son microservicios.

## Módulos previstos

Inicio, fotografías y confirmación, búsqueda, recomendaciones, probador y detalle de producto. Services, modelos y scraping contienen por ahora contratos pendientes de implementación; no hay análisis de imágenes, scraping ni probador real.

## Archivos principales

- `run.py`: arranque del servidor.
- `config.py`: configuración central.
- `app/__init__.py`: fábrica de la aplicación.
- `tests/`: espacio reservado para pruebas futuras.

## Instalación y ejecución

Requiere Python 3.10 o 3.11. En Windows (PowerShell):

```
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python run.py
```

La aplicación queda en http://127.0.0.1:5000. Si pip falla con un error de certificado SSL, agrega `--use-feature=truststore` al comando de instalación.

Las pruebas usan pytest, que se instala aparte: `python -m pip install pytest` y luego `python -m pytest`.

## Estado actual

Fase 1 completa: navegación entre todas las pantallas. Salvo la landing, las pantallas contienen marcadores; las fotografías, la búsqueda, el scraping, las recomendaciones, la colorimetría y el probador se implementan en las fases siguientes.

## Alcance
Tus fotografías (rostro y cuerpo completo) → Buscar prendas → Probador virtual → Ficha de compra.
DePrati; camisas/pantalones/shorts; colorimetría; ranking de cinco si hay suficientes.
Sin cuentas, historial, pago propio ni video. Fotos exclusivamente en memoria según RNF-04.
Módulos de vista, servicios y modelos trabajan dentro del mismo proceso.
Models representa datos, no implica una base de datos. Scraping es acceso externo, no microservicio.

## Trazabilidad
RF-01 a RF-05 y RNF-01 a RNF-05 recuperados de S1.docx (1).pdf, páginas 6–21.
Actualizar RF-01/HU-01: la entrega anterior dice una foto y el alcance vigente requiere dos.
RNF-02 debe definir métricas separadas para coordenadas y clasificación cromática.
RNF-01 necesita acordar un umbral numérico para «pocos segundos».
