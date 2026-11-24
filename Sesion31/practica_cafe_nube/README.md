# Práctica: Café Nube sin servidores, y una prueba de carga

**Sesión 31 · App Engine, Cloud Run y pruebas de carga**

## El caso

En la Sesión 30, la API de Café Nube corría en Kubernetes. Para eso armaste un clúster, cargaste las imágenes y escribiste manifiestos. Hoy subes **la misma API** a Google Cloud **sin clúster**, de dos formas:

- En **App Engine** subes solo el código: `main.py`, `requirements.txt` y `app.yaml`.
- En **Cloud Run** subes una imagen de contenedor, construida con su `Dockerfile`.

Al final, con **Apache Bench** (`ab`), mandas cientos de pedidos a la vez a la API para medir cuántos responde por segundo y si falla alguno.

```
                         ┌── App Engine ──> https://PROYECTO.uc.r.appspot.com/menu
Cloud Shell (gcloud, ab) ┤
                         └── Cloud Build ──> Artifact Registry ──> Cloud Run ──> https://cafe-api-….run.app/menu
```

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`appengine/main.py`](appengine/main.py) | La API de Café Nube: `GET /menu` devuelve el menú en JSON. |
| [`appengine/requirements.txt`](appengine/requirements.txt) | Las bibliotecas que instala App Engine: Flask. |
| [`appengine/app.yaml`](appengine/app.yaml) | La configuración de App Engine: Python 3.12. |
| [`cloudrun/main.py`](cloudrun/main.py) | La misma API. |
| [`cloudrun/requirements.txt`](cloudrun/requirements.txt) | Flask y **gunicorn**, el servidor web que la arranca. |
| [`cloudrun/Dockerfile`](cloudrun/Dockerfile) | La receta de la imagen para Cloud Run. |

### `main.py`

```python
from flask import Flask, jsonify

app = Flask(__name__)

MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Latte", "precio": 12},
]


@app.get("/menu")
def menu():
    return jsonify(MENU)
```

Es la API de la Sesión 28 **sin** la última línea, `app.run(...)`. Aquí no la arrancas tú: **gunicorn** busca la variable `app` dentro de `main.py` y la arranca.

### `app.yaml` (App Engine)

```yaml
runtime: python312
```

| Clave | Qué hace |
| --- | --- |
| `runtime: python312` | Le pide a App Engine Python 3.12. App Engine instala lo de `requirements.txt` y arranca `main.py` con gunicorn. |

### `Dockerfile` (Cloud Run)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT --threads 8 main:app
```

| Línea | Qué hace |
| --- | --- |
| `FROM python:3.12-slim` | Parte de una imagen con Python, como en la Sesión 28. |
| `RUN pip install ...` | Instala Flask y gunicorn. |
| `CMD exec gunicorn --bind :$PORT --threads 8 main:app` | Arranca gunicorn en el puerto que le da Cloud Run en la variable `PORT` (el 8080), con la variable `app` de `main.py`. `--threads 8`: atiende hasta 8 pedidos a la vez. |

---

## Preparación

Necesitas un **proyecto de Google Cloud** donde puedas crear recursos.

1. Abre la consola de Google Cloud, elige tu proyecto arriba y haz clic en **Activar Cloud Shell**.
2. En Cloud Shell, descarga el material del curso y entra a esta carpeta:

```bash
git clone https://github.com/rgap/rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026.git
cd rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026/Sesion31/practica_cafe_nube
```

3. Habilita las APIs que vas a usar. Si aparece **Autorizar Cloud Shell**, haz clic en **Autorizar**:

```bash
gcloud services enable appengine.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com
```

---

## Prueba 1. Café Nube en App Engine

Entra a la carpeta de App Engine, crea la aplicación del proyecto y sube el código:

```bash
cd appengine
gcloud app create --region=us-central
gcloud app deploy
```

Cuando pregunte **Do you want to continue (Y/n)?**, escribe `Y` y presiona **Intro**. Tarda un par de minutos.

**Qué deberías ver** al final:

```text
Deployed service [default] to [https://TU-PROYECTO.uc.r.appspot.com]
```

Copia esa URL y guárdala en una variable, `AE`. Así no tienes que volver a escribirla:

```bash
AE=https://TU-PROYECTO.uc.r.appspot.com
curl $AE/menu
```

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Latte","precio":12}]
```

**Por qué:** no creaste ninguna máquina. App Engine leyó `app.yaml`, instaló Flask, arrancó la API y te dio una URL con HTTPS.

---

## Prueba 2. Café Nube en Cloud Run

Vuelve a la carpeta de la práctica y entra a la de Cloud Run:

```bash
cd ../cloudrun
```

Crea en Artifact Registry el repositorio `cafe`, donde guardarás la imagen:

```bash
gcloud artifacts repositories create cafe --repository-format=docker --location=us-central1
```

Guarda el nombre de la imagen en una variable. `$GOOGLE_CLOUD_PROJECT` ya tiene el ID de tu proyecto en Cloud Shell:

```bash
IMAGEN=us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/cafe/cafe-api
```

Construye la imagen con Cloud Build y súbela con la etiqueta `v1`:

```bash
gcloud builds submit --tag $IMAGEN:v1 .
```

Al final, Cloud Build muestra **SUCCESS**. Ahora crea el servicio de Cloud Run con esa imagen:

```bash
gcloud run deploy cafe-api --image $IMAGEN:v1 --region us-central1 --allow-unauthenticated --max-instances 3
```

**Qué deberías ver** al final:

```text
Service [cafe-api] revision [cafe-api-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://cafe-api-123456789.us-central1.run.app
```

Copia tu **Service URL** en la variable `CR` y pide el menú:

```bash
CR=https://cafe-api-123456789.us-central1.run.app
curl $CR/menu
```

**Por qué:** Cloud Build construyó la imagen con tu `Dockerfile`, Artifact Registry la guardó y Cloud Run la corrió, como en la Sesión 30 pero **sin clúster**. `--allow-unauthenticated` deja que cualquiera con la URL llame a la API, y `--max-instances 3` dice que nunca habrá más de tres copias.

---

## Prueba 3. Tu primera prueba de carga

Comprueba que tengas Apache Bench:

```bash
ab -V
```

Si dice `command not found`, instálalo:

```bash
sudo apt-get install -y apache2-utils
```

Manda **200** pedidos, **20** a la vez, a la API de Cloud Run. Ojo: la URL tiene que llevar la ruta, `/menu`:

```bash
ab -n 200 -c 20 $CR/menu
```

**Qué deberías ver** (tus números serán otros):

```text
Concurrency Level:      20
Time taken for tests:   1.079 seconds
Complete requests:      200
Failed requests:        0
...
Requests per second:    185.36 [#/sec] (mean)
Time per request:       107.90 [ms] (mean)
...
Percentage of the requests served within a certain time (ms)
  50%    101
  95%    139
 100%    312 (longest request)
```

| Línea | Qué te dice |
| --- | --- |
| `Complete requests` | Cuántos pedidos terminaron: los 200. |
| `Failed requests` | Cuántos fallaron. Lo que quieres ver: `0`. |
| `Requests per second` | Cuántos pedidos por segundo respondió la API: el número principal. |
| `Time per request` (la primera) | Cuánto esperó, en promedio, cada usuario. |
| `95%` | 95 de cada 100 pedidos tardaron eso o menos. |
| `100%` | El pedido más lento. |

Repite el comando. Si Cloud Run estaba en cero instancias, la primera vez el `100%` sale mucho mayor: el primer pedido esperó a que arrancara una.

---

## Prueba 4. Sube la carga y compara

Manda **1000** pedidos, **50** a la vez, a Cloud Run y después a App Engine:

```bash
ab -n 1000 -c 50 $CR/menu
ab -n 1000 -c 50 $AE/menu
```

Anota tus números:

| | Cloud Run | App Engine |
| --- | --- | --- |
| `Failed requests` | | |
| `Requests per second` | | |
| `Time per request` | | |
| `95%` | | |

En la consola, abre **Cloud Run > cafe-api > Métricas** y busca el gráfico **Cantidad de instancias de contenedor**: Cloud Run creó copias según los pedidos, nunca más de 3. En **App Engine > Instancias** ves las de App Engine.

**Por qué:** con más pedidos a la vez, cada uno espera un poco más, y los servicios crean más instancias para atenderlos. Los números cambian según la hora y la región: lo importante es saber **leerlos** y ver si algún pedido **falla**.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Cómo subo solo mi código? | `gcloud app deploy`, con `app.yaml` y `requirements.txt` |
| 2 | ¿Cómo corro mi contenedor sin clúster? | `gcloud builds submit` y `gcloud run deploy` |
| 3 | ¿Cuántos pedidos por segundo responde? | `ab -n 200 -c 20 $CR/menu`: `Requests per second` |
| 4 | ¿Qué pasa con más carga? | Cada pedido espera más y aparecen más instancias |

---

## Si algo falla

| Lo que ves | Qué hacer |
| --- | --- |
| `gcloud app create` dice que la aplicación ya existe | Tu proyecto ya tiene una: sigue con `gcloud app deploy` |
| `ab: invalid URL` | Falta la ruta: la URL tiene que terminar en `/menu` |
| `curl` o `ab` no encuentran la URL | Cloud Shell se reinició y perdió las variables: vuelve a escribir `AE=…`, `CR=…` e `IMAGEN=…` |
| `Non-2xx responses` en `ab` | La API respondió con error: prueba la misma URL con `curl` |
| `ab: command not found` | `sudo apt-get install -y apache2-utils` |

---

## Reto

Agrega `{"nombre": "Mocha", "precio": 13},` al menú de `cloudrun/main.py` y súbelo a **Cloud Run** como una revisión **v2** **sin tráfico**. Comprueba en **Cloud Run > cafe-api > Revisiones** que tiene 0 %, y después dale el 100 %. ¿Qué comandos usas? Pista: `gcloud run deploy` tiene la opción `--no-traffic`.

---

## Apagar todo

Borra el servicio de Cloud Run y el repositorio con la imagen. Responde `Y` en cada uno:

```bash
gcloud run services delete cafe-api --region us-central1
gcloud artifacts repositories delete cafe --location=us-central1
```

La aplicación de App Engine **no se puede borrar**. Sin visitas baja a cero instancias; si quieres que deje de responder, en **App Engine > Configuración** puedes inhabilitarla.

---

## Apache Bench en tu computadora

`ab` también corre en tu computadora, contra la URL de Cloud Run o de App Engine:

- **macOS:** ya viene instalado. Prueba `ab -V`.
- **Linux:** `sudo apt-get install -y apache2-utils`.
- **Windows:** con Docker Desktop abierto, usa la imagen `httpd`, que trae `ab` adentro:

```powershell
docker run --rm httpd ab -n 200 -c 20 https://cafe-api-123456789.us-central1.run.app/menu
```
