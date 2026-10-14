# Mirror IA — Propuesta 1

Arquitectura tentativa: Cliente–Servidor + En Capas + Monolito Modular.
Patrón de organización: MVT adaptado a Flask + Services. Una sola unidad desplegable.

## Ejecutar el maquetado
Crear un entorno virtual, instalar requirements.txt y ejecutar `python run.py`.
Abrir http://127.0.0.1:5000. Las rutas GET solo muestran páginas de estructura.
No hay subida de fotos, scraping, IA ni productos simulados. Services declara contratos
con NotImplementedError. Las rutas importan servicios para mostrar la frontera prevista;
la delegación funcional se añadirá al implementar los casos de uso.

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
