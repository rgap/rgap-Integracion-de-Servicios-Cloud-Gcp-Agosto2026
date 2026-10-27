# Sesión 23 — Bases de datos en Google Cloud: tipos, usos y Cloud SQL

Presentación de **19 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 22: revisión, logro, saberes previos, utilidad, dos partes de teoría, práctica, cierre y referencias.

La sesión es una introducción intuitiva a las bases de datos con el caso de facturación de Pedidos Express: la diferencia entre una base relacional y una no relacional, los servicios de Google Cloud (Cloud SQL, Spanner, Firestore, Bigtable y BigQuery) qué dato va en cada uno, los motores que ofrece Cloud SQL (MySQL, PostgreSQL y SQL Server) y cuándo conviene SQLite, MySQL, PostgreSQL o SQL Server. La segunda parte resume en palabras simples el laboratorio **[Implementa Cloud SQL](https://www.skills.google/paths/11/course_templates/49/labs/592108)**, que es la práctica de la sesión.

- [Diapositivas PDF](slides/build/S23.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Diagramas

Los dos diagramas de las diapositivas están en SystemModeler (`/Users/rgap/Desktop/Proyectos/SystemModeler/ejemplos/`), cada uno en contexto, contenedores y despliegue:

- `pedidos_express/`: qué dato de Pedidos Express va en cada servicio (diapositiva 11 usa `2_contenedores.md`).
- `wordpress_con_cloud_sql/`: el sistema del lab, con un WordPress conectado por proxy y otro por IP privada (diapositiva 16 usa `3_despliegue.md`).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Inicio y repaso | 1–7 | 14 |
| Parte 1: tipos de bases de datos | 8–13 | 22 |
| Parte 2: Cloud SQL en el lab | 14–16 | 8 |
| Práctica: laboratorio | 17 | 30 |
| Cierre | 18–19 | 6 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S23.pdf
```
