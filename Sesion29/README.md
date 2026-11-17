# Sesión 29 — Varios contenedores con Docker Compose

Presentación de **11 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, teoría, cierre y referencias. Las diapositivas **no tienen práctica**; la guía de la carpeta `practica_cafe_nube/` queda aparte. Es una **introducción**: una idea por diapositiva.

La revisión retoma la Sesión 28 (Dockerfile, puertos y variables de entorno) y termina con Café Nube en tres piezas, la página, la API y la base: de ahí salen las tres preguntas del día (Compose, redes y volúmenes).

La teoría es un **resumen en tres diapositivas** del curso **Varios contenedores con Compose** (ruta *Despliegue con Docker*); el detalle se ve en la plataforma:

1. **Docker Compose.** Qué es un servicio, un `compose.yaml` resumido con `web`, `api` y `db`, y `up`, `ps`, `logs` y `down`.
2. **Redes.** Cada servicio se alcanza por su nombre (`api:8080`, `db:5432`); `localhost`, dentro de un contenedor, es ese mismo contenedor.
3. **Volúmenes.** `environment:` y `volumes:` del servicio `db`; `down` deja los pedidos y `down -v` los borra.

- [Diapositivas PDF](slides/build/S29.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Guía aparte: Café Nube con la página, la API y la base

No se presenta en las diapositivas. La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Son los archivos del escenario «Café Nube: la página, la API y la base» del curso. Los estudiantes levantan los tres servicios, hacen un pedido, prueban la red por nombre y comprueban que el volumen guarda los pedidos.

Se hace en **Windows con PowerShell** y **Docker Desktop**.

```powershell
docker compose up -d                                            # levanta web, api y db
curl.exe -X POST localhost:8080/api/pedidos -d producto=Capuchino  # hace un pedido
docker compose down                                             # los baja; el volumen queda
```

| Archivo | Qué contiene |
| --- | --- |
| [`compose.yaml`](practica_cafe_nube/compose.yaml) | `web` (`build: ./web`, 8080:80), `api` (`build: ./api`, `DATABASE_URL`) y `db` (`postgres:17`, volumen `datos`) |
| [`web/`](practica_cafe_nube/web) | La página del menú y Nginx, que le pasa a la API lo que empieza con `/api/` |
| [`api/`](practica_cafe_nube/api) | La API de Café Nube con `GET /menu`, `POST /pedidos` y `GET /pedidos`, guardados en PostgreSQL |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `docker compose up -d` | Dos imágenes construidas, la red, el volumen y tres contenedores |
| 2 | `docker compose ps` y `localhost:8080` | Solo `web` publica un puerto; la página muestra el menú |
| 3 | `curl.exe` al menú, un `POST` y la lista de pedidos | `{"ok":true}` y el pedido del Capuchino |
| 4 | `docker compose exec web curl` a `api:8080` y a `localhost:8080` | Por nombre responde; por `localhost`, `Could not connect to server` |
| 5 | `down` y `up -d` | El pedido sigue |
| 6 | `down -v` y `up -d` | `[]`: el volumen se borró |

Termina con un reto: publicar la página en el 8090 cambiando una línea. La solución está en [respuestas.md](respuestas.md).

Las salidas de la guía son las reales, con Docker 29.8, Docker Compose 5.5, Nginx 1.29 y PostgreSQL 17 (algunas columnas resumidas).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 10 |
| Logro, saberes previos y utilidad | 4–6 | 6 |
| Teoría: Compose, redes y volúmenes | 7–9 | 20 |
| Cierre | 10–11 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S29.pdf
```
