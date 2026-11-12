# Sesión 28 — Docker: tu propia imagen, puertos, variables y Compose

Presentación de **25 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, práctica, teoría, cierre y referencias. Como en la Sesión 27, la práctica va **antes** de la teoría: primero se construye y se corre la imagen de la API de Café Nube; después se explica cada paso. Es una **introducción**: una idea por diapositiva.

La revisión retoma la Sesión 27 (lecciones 1 a 3 del curso **Docker desde cero**: desplegar, dependencias, imagen y contenedor, y el ciclo de vida) y termina con la API de Café Nube que hay que llevar a una imagen y abrir desde el navegador: de ahí salen las tres preguntas del día (Dockerfile, puertos y variables, Compose).

La teoría resume, con diagramas, las lecciones 4 a 7 de **Docker desde cero** y las dos primeras de **Varios contenedores con Compose** (ruta *Despliegue con Docker*), con su mismo caso, Café Nube:

1. **Dockerfile: tu propia imagen.** `FROM`, `WORKDIR`, `COPY` y `CMD`, con el proyecto `hola-docker`.
2. **Construir y correr.** `docker build -t hola .` y `docker run hola`: se construye una vez y se corre muchas; `CMD` corre al arrancar; si cambias el código, construyes otra vez.
3. **Puertos.** Puerto y publicar un puerto: `-p 8080:80` con Nginx; `port is already allocated`.
4. **Variables de entorno.** `-e NOMBRE=valor`: la misma imagen `cafe-api` con `PUERTO=9090`; producción.
5. **Una base de datos que pide contraseña.** `postgres:17` sin y con `POSTGRES_PASSWORD`; los logs dicen por qué se detuvo.
6. **Café Nube: la API en una imagen.** Cada frase del enunciado se vuelve una línea del Dockerfile; `RUN` y `EXPOSE`.
7. **Capas.** Por qué se copia `requirements.txt` e instala Flask antes de `COPY . .` (`CACHED`).
8. **Errores frecuentes** de Café Nube y `docker logs`.
9. **Una aplicación, varias piezas.** Frontend, backend y servicio: `web`, `api` y `db`, un programa por contenedor.
10. **Docker Compose.** Los `docker run` de cada pieza frente a un `compose.yaml`; `docker compose`, con espacio.
11. **El archivo `compose.yaml`.** YAML y las claves `services`, `build`, `image` y `ports`.
12. **Compose: up, ps, logs y down.** Su equivalente con `docker`, y `up -d --build` cuando cambia el código.

- [Diapositivas PDF](slides/build/S28.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Práctica: la API de Café Nube en una imagen

La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Es la API de la Sesión 27, ahora con su `Dockerfile` y un `compose.yaml`. Los estudiantes construyen la imagen, la corren con su puerto publicado y con una variable de entorno, y la levantan junto con un Nginx usando Compose.

Se hace en **Windows con PowerShell** y **Docker Desktop**. No hace falta instalar Python ni Flask: los trae la imagen.

```powershell
docker build -t cafe-api .                          # construye la imagen
docker run -d --name api -p 8080:8080 cafe-api      # la corre con su puerto publicado
curl.exe localhost:8080/menu                        # pide la carta
docker compose up -d                                # levanta la API y Nginx
docker compose down                                 # los baja
```

| Archivo | Qué contiene |
| --- | --- |
| [`api.py`](practica_cafe_nube/api.py) | La API de la Sesión 27; ahora escucha en `0.0.0.0` para aceptar pedidos de afuera del contenedor |
| [`requirements.txt`](practica_cafe_nube/requirements.txt) | `flask==3.1.0` |
| [`Dockerfile`](practica_cafe_nube/Dockerfile) | El de la solución del escenario «Café Nube: la API en una imagen» |
| [`compose.yaml`](practica_cafe_nube/compose.yaml) | `api` (`build: .`, 8080) y `web` (`nginx:1.29`, 8081) |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `docker build -t cafe-api .` | Cinco pasos, uno por línea del `Dockerfile`; la API **no** enciende |
| 2 | `docker run -d --name api -p 8080:8080 cafe-api` y `curl.exe localhost:8080/menu` | La carta en JSON; `docker logs api` anota `GET /menu` con `200` |
| 3 | Otra copia con `-p 8080:8080`; después con `-p 8081:8080` | `port is already allocated`; con el 8081, dos copias a la vez |
| 4 | `-e PUERTO=9090 -p 8082:9090` | La misma imagen escucha en el 9090 adentro; tres contenedores en `docker ps` |
| 5 | Agregar un café a `MENU`, correr otra vez; después construir otra vez | Sin construir no aparece; al construir, los cuatro primeros pasos salen `CACHED` |
| 6 | `docker compose up -d`, `ps`, `logs api` y `down` | Dos contenedores (`practica_cafe_nube-api-1` y `-web-1`); `down` los borra y las imágenes quedan |

Termina con un reto: la ruta `GET /menu/<nombre>` de la Sesión 27, funcionando en el contenedor de Compose (hace falta `docker compose up -d --build`). La solución está en [respuestas.md](respuestas.md).

Las salidas de la guía son las reales, con Docker 29.8, Docker Compose 5.5, Python 3.12 y Flask 3.1.0 (algunas columnas resumidas).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 6 |
| Logro, saberes previos y utilidad | 4–6 | 4 |
| Práctica: la API de Café Nube en una imagen | 7–10 | 36 |
| Teoría: Dockerfile, puertos, variables y Compose | 11–23 | 28 |
| Cierre | 24–25 | 6 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S28.pdf
```
