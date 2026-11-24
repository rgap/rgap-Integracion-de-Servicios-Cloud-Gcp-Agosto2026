# Sesión 31 — App Engine, Cloud Run y pruebas de carga

Presentación de **20 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, teoría, cierre y referencias. Las diapositivas **no tienen práctica**; la guía de la carpeta `practica_cafe_nube/` queda aparte. Es una **introducción**: una idea por diapositiva.

La revisión resume la Sesión 30 en cuatro diapositivas:

1. **Un sistema que necesita Kubernetes.** Café Nube en una sola computadora: si se apaga, se cae; una copia de la API no alcanza. Lo que necesita: varias máquinas, varias copias, que se reparen solas y un nombre fijo.
2. **Qué pieza resuelve cada cosa.** Un dibujo del clúster con el nodo maestro, tres nodos, un Deployment de tres réplicas, el Service y el manifiesto, y una frase para cada pieza.
3. **Café Nube en Kubernetes.** Los Services `web` y `api` y sus pods, qué corre en cada nodo y qué pasa si se borra un pod o se apaga un nodo.
4. **GKE.** Cloud Build, Artifact Registry y GKE: Kubernetes administrado por Google, con los mismos manifiestos.

Los saberes previos preguntan definiciones (Flask, imagen, Dockerfile, puerto, variable de entorno) y qué hacen algunas piezas de la API.

1. **Sin servidores.** Qué hace uno en una VM y qué hace Google en App Engine y Cloud Run: máquinas, instalación, copias, bajar a cero y HTTPS.
2. **App Engine: subes tu código.** Solo lo básico: `main.py`, `requirements.txt` y `app.yaml`; `gcloud app create` y `gcloud app deploy`; App Engine instala, arranca y da la URL.
3. **Cloud Run: subes un contenedor.** Cloud Build, Artifact Registry y Cloud Run; el `Dockerfile` con gunicorn en el puerto de `PORT`.
4. **Cloud Run: crear el servicio.** `gcloud run deploy` con región, acceso público (si se pide autenticación, `403 Forbidden`), máximo de instancias y variables de entorno.
5. **Cloud Run: revisiones y tráfico.** Cada cambio crea una revisión; una revisión sin tráfico y un canary del 10 %.
6. **App Engine y Cloud Run, lado a lado.** Qué se sube, qué archivo, cuántos por proyecto, la URL.
7. **Prueba de carga.** Una diapositiva que solo dice «Pruebas de carga» abre el tema. Después: qué es, las tres preguntas que responde y cinco herramientas: Apache Bench, hey, k6, Locust y JMeter.
8. **Apache Bench: el comando.** `ab -n 200 -c 20 URL/menu`: pedidos en total y a la vez.
9. **Apache Bench: el resultado.** `Complete`, `Failed`, `Requests per second`, `Time per request` y los porcentajes.

- [Diapositivas PDF](slides/build/S31.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Guía aparte: Café Nube sin servidores, y una prueba de carga

No se presenta en las diapositivas. La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Los estudiantes suben la API de Café Nube a App Engine y a Cloud Run, y la miden con Apache Bench.

Se hace en **Cloud Shell**, en un proyecto de Google Cloud.

```bash
gcloud app deploy                                                # App Engine
gcloud run deploy cafe-api --image $IMAGEN:v1 --region us-central1 --allow-unauthenticated --max-instances 3
ab -n 200 -c 20 $CR/menu                                         # prueba de carga
```

| Archivo | Qué contiene |
| --- | --- |
| [`appengine/`](practica_cafe_nube/appengine) | La API (`main.py`), `requirements.txt` con Flask y `app.yaml` |
| [`cloudrun/`](practica_cafe_nube/cloudrun) | La misma API, `requirements.txt` con Flask y gunicorn, y el `Dockerfile` |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `gcloud app create` y `gcloud app deploy` | El menú en `https://PROYECTO.uc.r.appspot.com/menu` |
| 2 | `gcloud builds submit` y `gcloud run deploy` | El menú en `https://cafe-api-….run.app/menu` |
| 3 | `ab -n 200 -c 20` | `Failed requests: 0` y los pedidos por segundo |
| 4 | `ab -n 1000 -c 50` a Cloud Run y a App Engine | Una tabla con los números y las instancias en la consola |

Termina con un reto: hacer en Cloud Run una revisión `v2` sin tráfico y darle el 100 %. La solución está en [respuestas.md](respuestas.md).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–5 | 12 |
| Logro, saberes previos y utilidad | 6–8 | 7 |
| Teoría: sin servidores y App Engine | 9–10 | 10 |
| Teoría: Cloud Run | 11–14 | 22 |
| Teoría: pruebas de carga y Apache Bench | 15–18 | 24 |
| Cierre | 19–20 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S31.pdf
```
