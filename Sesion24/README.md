# Sesión 24 — Big Data y BigQuery: preguntas a millones de filas con SQL

Presentación de **22 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 23: revisión, logro, saberes previos, utilidad, dos partes de teoría, práctica, cierre y referencias.

La revisión retoma el uso de Cloud SQL con un caso de estudio: Pedidos Express diseña una sola instancia `mysql-server` con cuatro bases de datos, una por área (`ventas`, `inventario`, `facturacion` y `recursos_humanos`). La teoría presenta Big Data con ejemplos de tamaño concretos, las tres V, la diferencia entre registrar y analizar, las dos ideas que hacen rápido a BigQuery (leer por columnas y repartir el trabajo) y el SQL básico para analizar: filtrar, agrupar, contar y sumar. La práctica es el laboratorio **[Examina los datos de facturación con BigQuery](https://www.skills.google/catalog_lab/1784)** y una práctica con Python.

- [Diapositivas PDF](slides/build/S24.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Práctica 2: BigQuery sin BigQuery

En la carpeta [`practica/`](practica/) está el notebook [`practica_bigquery_python.ipynb`](practica/practica_bigquery_python.ipynb). Repite las consultas del lab con Python y DuckDB sobre 1.2 millones de pedidos de Pedidos Express (2023–2025), sin usar Google Cloud.

- Se abre en Google Colab (*Archivo → Subir cuaderno*) o en Jupyter / VS Code.
- **De dónde salen los datos:** no se descargan. La primera celda del notebook escribe y ejecuta [`generar_ventas.py`](practica/generar_ventas.py), que crea `ventas.csv` (1.2 millones de filas, unos 105 MB). Los datos usan una semilla fija, así que todos obtienen los mismos resultados.
- Para abrirlo desde Colab: *Archivo → Abrir cuaderno → GitHub*, pegar `github.com/rgap/rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026` y elegir `Sesion24/practica/practica_bigquery_python.ipynb`.
- Termina con cinco retos; las soluciones están en [respuestas.md](respuestas.md).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Inicio y repaso de Cloud SQL | 1–8 | 14 |
| Parte 1: Big Data | 9–13 | 12 |
| Parte 2: BigQuery y SQL para analizar | 14–18 | 12 |
| Práctica 1: laboratorio | 19 | 24 |
| Práctica 2: Python + DuckDB | 20 | 14 |
| Cierre | 21–22 | 4 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S24.pdf
```
