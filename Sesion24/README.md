# Sesión 24 — Big Data y BigQuery: preguntas a millones de filas con SQL

Presentación de **21 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 23: revisión, logro, saberes previos, utilidad, dos partes de teoría, práctica, cierre y referencias.

La revisión retoma el uso de Cloud SQL con un caso de estudio: Pedidos Express diseña una sola instancia `mysql-server` con cuatro bases de datos, una por área (`ventas`, `inventario`, `facturacion` y `recursos_humanos`). La teoría presenta Big Data con ejemplos de tamaño concretos, las tres V, la diferencia entre registrar y analizar, las dos ideas que hacen rápido a BigQuery (leer por columnas y repartir el trabajo) y el SQL básico para analizar: filtrar, agrupar, contar y sumar. La práctica es el laboratorio **[Examina los datos de facturación con BigQuery](https://www.skills.google/catalog_lab/1784)**.

- [Diapositivas PDF](slides/build/S24.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Inicio y repaso de Cloud SQL | 1–8 | 14 |
| Parte 1: Big Data | 9–13 | 12 |
| Parte 2: BigQuery y SQL para analizar | 14–18 | 14 |
| Práctica: laboratorio | 19 | 36 |
| Cierre | 20–21 | 4 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S24.pdf
```
