# Sesión 28 — Docker: tu propia imagen, puertos y variables

Presentación de **10 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, teoría, cierre y referencias. Las diapositivas **no tienen práctica**; la guía de la carpeta `practica_cafe_nube/` queda aparte. Es una **introducción**: una idea por diapositiva.

La revisión retoma la Sesión 27 (lecciones 1 a 3 del curso **Docker desde cero**: desplegar, dependencias, imagen y contenedor, y el ciclo de vida) y termina con la API de Café Nube que hay que llevar a una imagen y abrir desde el navegador: de ahí salen las dos preguntas del día (Dockerfile, y puertos y variables).

La teoría es un **resumen en dos diapositivas** de las lecciones 4 a 7 de **Docker desde cero** (ruta *Despliegue con Docker*); el detalle se ve en la plataforma:

1. **Dockerfile: tu propia imagen.** El Dockerfile de Café Nube (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE` y `CMD`), `docker build` y `docker run`.
2. **Puertos y variables de entorno.** `-p 8080:8080` y `-e PUERTO=9090` con la misma imagen `cafe-api`.

- [Diapositivas PDF](slides/build/S28.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Guía aparte: la API de Café Nube en una imagen

No se presenta en las diapositivas. La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Es la API de la Sesión 27, ahora con su `Dockerfile`. Los estudiantes construyen la imagen y la corren con su puerto publicado y con una variable de entorno.

Se hace en **Windows con PowerShell** y **Docker Desktop**. No hace falta instalar Python ni Flask: los trae la imagen.

```powershell
docker build -t cafe-api .                          # construye la imagen
docker run -d --name api -p 8080:8080 cafe-api      # la corre con su puerto publicado
curl.exe localhost:8080/menu                        # pide la carta
docker rm -f api                                    # lo detiene y lo borra
```

| Archivo | Qué contiene |
| --- | --- |
| [`api.py`](practica_cafe_nube/api.py) | La API de la Sesión 27; ahora escucha en `0.0.0.0` para aceptar pedidos de afuera del contenedor |
| [`requirements.txt`](practica_cafe_nube/requirements.txt) | `flask==3.1.0` |
| [`Dockerfile`](practica_cafe_nube/Dockerfile) | El de la solución del escenario «Café Nube: la API en una imagen» |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `docker build -t cafe-api .` | Cinco pasos, uno por línea del `Dockerfile`; la API **no** enciende |
| 2 | `docker run -d --name api -p 8080:8080 cafe-api` y `curl.exe localhost:8080/menu` | La carta en JSON; `docker logs api` anota `GET /menu` con `200` |
| 3 | Otra copia con `-p 8080:8080`; después con `-p 8081:8080` | `port is already allocated`; con el 8081, dos copias a la vez |
| 4 | `-e PUERTO=9090 -p 8082:9090` | La misma imagen escucha en el 9090 adentro; tres contenedores en `docker ps` |
| 5 | Agregar un café a `MENU`, correr otra vez; después construir otra vez | Sin construir no aparece; al construir, los cuatro primeros pasos salen `CACHED` |

Termina con un reto: la ruta `GET /menu/<nombre>` de la Sesión 27, funcionando en el contenedor (hace falta construir la imagen otra vez). La solución está en [respuestas.md](respuestas.md).

Las salidas de la guía son las reales, con Docker 29.8, Python 3.12 y Flask 3.1.0 (algunas columnas resumidas).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 10 |
| Logro, saberes previos y utilidad | 4–6 | 6 |
| Teoría: Dockerfile, puertos y variables | 7–8 | 20 |
| Cierre | 9–10 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S28.pdf
```
