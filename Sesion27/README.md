# Sesión 27 — Docker desde cero: desplegar, imagen y contenedor

Presentación de **19 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, práctica, teoría, cierre y referencias. La práctica va **antes** de la teoría: primero se enciende una API y se ve qué necesita para funcionar; después, cómo Docker la lleva con todo eso. Es una **introducción**: una idea por diapositiva, sin detalles de configuración.

La revisión retoma la Sesión 26 (balanceador de carga, CDN y contenedor) y termina con la tienda que hay que encender igual en `web-1`, `web-2` y `web-3`: de ahí salen las tres preguntas del día (desplegar, imagen y contenedor).

La teoría resume, con diagramas, las lecciones 1 a 3 del curso **Docker desde cero** (ruta *Despliegue con Docker*), con su mismo caso, Café Nube:

1. **¿Qué es desplegar?** Tu computadora → un servidor → cualquiera la usa. Servidor y desplegar.
2. **Las dependencias:** la laptop de Lucía (Python 3.12, Flask) frente a la de Diego (Python 3.9, sin Flask). Retoma el `ModuleNotFoundError` de la prueba 1 de la práctica.
3. **Imagen y contenedor:** la app con sus dependencias → la imagen (plantilla) → contenedores (copias en marcha). Con la imagen, Diego solo necesita Docker.
4. **Tu primer contenedor:** la salida de `docker run hello-world` (descarga la imagen la primera vez y luego la corre).
5. **El ciclo de vida:** corriendo, detenido y borrado, con `docker run`, `docker stop` y `docker rm`; segundo plano (`-d`) y logs.
6. **Los comandos de todos los días:** `docker run -d --name web nginx`, `docker ps`, `docker logs`, `docker stop`, `docker ps -a` y `docker rm`, con el estado en que queda el contenedor.

Los comandos de Docker se muestran en las diapositivas; la práctica no los usa.

- [Diapositivas PDF](slides/build/S27.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Práctica: la API de Café Nube

La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Café Nube, una cafetería de barrio, necesita una API que entregue su carta. Los estudiantes la encienden en su computadora con Python y Flask, y ven qué necesita para funcionar: **Python**, **Flask** (`requirements.txt`) y **un puerto libre**.

Se hace en **Windows con PowerShell** y **sin entorno virtual**: se instala Python y luego todo se ejecuta con `python`.

```powershell
winget install --id Python.Python.3.12 -e   # instala Python (luego, cerrar y abrir PowerShell)
python api.py                                # prueba 1: falta Flask
python -m pip install -r requirements.txt    # instala Flask
python api.py                                # enciende la API en localhost:8080
```

El paquete de winget instala Python con `PrependPath=1`, así que `python` responde en una ventana de PowerShell nueva.

| Archivo | Qué contiene |
| --- | --- |
| [`api.py`](practica_cafe_nube/api.py) | La API: `GET /menu` responde la carta en JSON; el puerto sale de la variable `PUERTO` (8080 si no existe) |
| [`requirements.txt`](practica_cafe_nube/requirements.txt) | `flask==3.1.0` |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | Encender la API con Python recién instalado | `ModuleNotFoundError: No module named 'flask'`: falta una dependencia |
| 2 | Instalar `requirements.txt`, encender y abrir `localhost:8080/menu` | La carta en JSON; la terminal anota `GET /menu` con código `200` |
| 3 | Abrir `localhost:8080/postres` | `Not Found`; la terminal anota `404` |
| 4 | Encender una segunda copia | `Address already in use`: el 8080 ya está ocupado |
| 5 | `$env:PUERTO = "9090"` y encender | Dos copias de la API, en el 8080 y en el 9090, sin cambiar el código |
| 6 | Agregar un café a `MENU` y recargar | No aparece hasta reiniciar la API |

Termina con un reto: la ruta `GET /menu/<nombre>`, que responde un solo café o un `404`. La solución está en [respuestas.md](respuestas.md).

La práctica es solo sobre la aplicación: no usa ni menciona Docker. Es la misma API que se empaqueta en el primer caso de estudio de la ruta *Despliegue con Docker* («Café Nube: la API en una imagen»), con dos cambios: el puerto sale de una variable de entorno y escucha solo en `127.0.0.1`.

La guía trae al final los pasos para macOS / Linux: ahí sí hace falta un entorno virtual, porque el Python del sistema no deja instalar con `pip` (`externally-managed-environment`). Las salidas de la guía son las reales, con Python 3.12 y Flask 3.1.0.

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 6 |
| Logro, saberes previos y utilidad | 4–6 | 4 |
| Práctica: la API de Café Nube | 7–10 | 42 |
| Teoría: Docker desde cero | 11–17 | 20 |
| Cierre | 18–19 | 8 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S27.pdf
```
