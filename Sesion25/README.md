# Sesión 25 — Supervisión y alta disponibilidad

Presentación de **22 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 24: revisión, logro, saberes previos, utilidad, dos partes de teoría, un laboratorio, cierre y referencias.

La revisión retoma BigQuery con la práctica **BigQuery sin BigQuery**: los estudiantes repiten con Python y DuckDB las consultas del lab de la sesión anterior y comparan sus resultados. La teoría tiene dos partes cortas para principiantes:

1. **Supervisar recursos:** métricas, registros y alertas; las métricas que más se revisan; cómo leer una gráfica de uso de CPU; los problemas que ocurren seguido; Google Cloud Observability (Cloud Monitoring y Cloud Logging) y cómo funciona una política de alertas.
2. **Alta disponibilidad:** qué significa 99 %, 99.9 % y 99.99 %, el punto único de falla y cómo se evita en Google Cloud (grupo de instancias administrado en varias zonas, Cloud SQL con alta disponibilidad y Cloud Storage).

La práctica es el laboratorio **[Supervisa recursos con Google Cloud Observability](https://www.skills.google/catalog_lab/1785)**.

El balanceo de carga, Cloud CDN y la práctica con Nginx pasaron a la [Sesión 26](../Sesion26/).

- [Diapositivas PDF](slides/build/S25.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Revisión: BigQuery sin BigQuery

En la carpeta [`practica/`](practica/) está el notebook [`practica_bigquery_python.ipynb`](practica/practica_bigquery_python.ipynb). Repite las consultas del lab de la Sesión 24 con Python y DuckDB sobre 1.2 millones de pedidos de Pedidos Express (2023–2025), sin usar Google Cloud.

- Se abre en Google Colab (*Archivo → Subir cuaderno*) o en Jupyter / VS Code.
- **De dónde salen los datos:** no se descargan. La primera celda del notebook escribe y ejecuta [`generar_ventas.py`](practica/generar_ventas.py), que crea `ventas.csv` (1.2 millones de filas, unos 105 MB). Los datos usan una semilla fija, así que todos obtienen los mismos resultados.
- Para abrirlo desde Colab: *Archivo → Abrir cuaderno → GitHub*, pegar `github.com/rgap/rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026` y elegir `Sesion25/practica/practica_bigquery_python.ipynb`.
- Termina con cinco retos; las soluciones están en [respuestas.md](respuestas.md).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión: BigQuery sin BigQuery | 1–4 | 15 |
| Logro, saberes previos y utilidad | 5–7 | 4 |
| Parte 1: supervisar recursos | 8–15 | 15 |
| Parte 2: alta disponibilidad | 16–19 | 10 |
| Práctica: laboratorio | 20 | 30 |
| Cierre | 21–22 | 6 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S25.pdf
```
