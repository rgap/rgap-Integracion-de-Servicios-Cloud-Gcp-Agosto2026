# Sesión 27 — Contenedores: Docker, Docker Compose y Kubernetes

Presentación de **18 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 26: revisión, logro, saberes previos, utilidad, teoría, práctica, cierre y referencias. Es una **introducción**: una idea por diapositiva, sin detalles de configuración.

La revisión retoma la Sesión 26 (balanceador de carga, CDN y contenedor) y termina con la tienda que hay que encender igual en `web-1`, `web-2` y `web-3`: de ahí salen las tres preguntas del día, una por herramienta. La teoría continúa donde quedó la Sesión 26:

1. **Docker: imagen y contenedor** (la Sesión 26 termina en esta misma diapositiva).
2. **El `Dockerfile` de la tienda:** sus cuatro líneas en palabras, `docker build` y `docker run`.
3. **Docker Compose:** un archivo y un comando para encender Nginx y tres tiendas.
4. **Kubernetes:** «quiero 3 copias», repartidas en varias máquinas; si una se cae, enciende otra.
5. **Las tres herramientas:** Docker empaqueta, Docker Compose junta y Kubernetes mantiene.

- [Diapositivas PDF](slides/build/S27.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Práctica: la API de Café Nube

La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Café Nube, una cafetería de barrio, necesita una API que entregue su carta. Los estudiantes la encienden en su computadora con Python y Flask, y ven qué necesita para funcionar: **Python**, **Flask** (`requirements.txt`) y **un puerto libre**.

| Archivo | Qué contiene |
| --- | --- |
| [`api.py`](practica_cafe_nube/api.py) | La API: `GET /menu` responde la carta en JSON; el puerto sale de la variable `PUERTO` (8080 si no existe) |
| [`requirements.txt`](practica_cafe_nube/requirements.txt) | `flask==3.1.0` |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | Encender la API con el entorno virtual vacío | `ModuleNotFoundError: No module named 'flask'`: falta una dependencia |
| 2 | Instalar `requirements.txt`, encender y abrir `localhost:8080/menu` | La carta en JSON; la terminal anota `GET /menu` con código `200` |
| 3 | Abrir `localhost:8080/postres` | `Not Found`; la terminal anota `404` |
| 4 | Encender una segunda copia | `Address already in use`: el 8080 ya está ocupado |
| 5 | `PUERTO=9090` y encender | Dos copias de la API, en el 8080 y en el 9090, sin cambiar el código |
| 6 | Agregar un café a `MENU` y recargar | No aparece hasta reiniciar la API |

Termina con un reto: la ruta `GET /menu/<nombre>`, que responde un solo café o un `404`. La solución está en [respuestas.md](respuestas.md).

La práctica es solo sobre la aplicación: no usa ni menciona Docker. Es la misma API que se empaqueta en el primer caso de estudio de la ruta *Despliegue con Docker* («Café Nube: la API en una imagen»), con dos cambios: el puerto sale de una variable de entorno y escucha solo en `127.0.0.1`.

Requiere Python 3.10 o más nuevo. La guía trae los comandos para macOS / Linux y para Windows (PowerShell). Todo se verificó con Python 3.12 y Flask 3.1.0 en macOS; las salidas de la guía son las reales.

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 6 |
| Logro, saberes previos y utilidad | 4–6 | 4 |
| Teoría: contenedores | 7–12 | 20 |
| Práctica: la API de Café Nube | 13–16 | 42 |
| Cierre | 17–18 | 8 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S27.pdf
```
