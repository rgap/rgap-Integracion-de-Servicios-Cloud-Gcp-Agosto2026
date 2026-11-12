# Práctica: la API de Café Nube en una imagen

**Sesión 28 · Dockerfile, puertos, variables de entorno y Compose**

## El caso

En la Sesión 27 encendiste la API de **Café Nube** en tu computadora, y para que funcionara hizo falta instalar **Python**, instalar **Flask** y tener **un puerto libre**. Si Diego quiere correrla en su laptop, tiene que repetir todo eso.

Hoy la API va dentro de una **imagen**: la imagen ya trae Python, Flask y el código. Con Docker, cualquiera la corre con un comando.

```
curl.exe o navegador  ──  localhost:8080/menu  ──>  -p 8080:8080  ──>  contenedor api
                                                                        (Python + Flask + api.py)
```

En esta práctica vas a construir la imagen, correr varias copias, cambiarles el puerto con una variable de entorno y, al final, levantar la API junto con un Nginx usando **Docker Compose**.

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`api.py`](api.py) | La API de la Sesión 27: `GET /menu` responde la carta en JSON. |
| [`requirements.txt`](requirements.txt) | Las bibliotecas que usa la API: `flask==3.1.0`. |
| [`Dockerfile`](Dockerfile) | Los pasos para armar la imagen de la API. |
| [`compose.yaml`](compose.yaml) | Dos servicios, la API y un Nginx, para levantarlos juntos. |

### `api.py`: un solo cambio

Es la misma API de la Sesión 27. Solo cambia la última línea:

```python
app.run(host="0.0.0.0", port=puerto)
```

`host="0.0.0.0"` hace que la API acepte pedidos que vienen **de afuera del contenedor**. Sin eso, solo atendería los que nacen dentro de él, y los que llegan por el puerto publicado no tendrían respuesta.

### `Dockerfile`, línea por línea

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "api.py"]
```

| Línea | Qué hace |
| --- | --- |
| `FROM python:3.12-slim` | Parte de una imagen que ya trae Python 3.12 (la variante `slim`, la más liviana). |
| `WORKDIR /app` | Todo lo que sigue pasa en la carpeta `/app`, dentro de la imagen. |
| `COPY requirements.txt .` | Copia la lista de bibliotecas a `/app`. |
| `RUN pip install -r requirements.txt` | Instala Flask **mientras se construye** la imagen. |
| `COPY . .` | Copia el resto del proyecto, con `api.py`. |
| `EXPOSE 8080` | Anota que la API escucha en el 8080. Solo lo documenta: el puerto se abre con `-p`. |
| `CMD ["python", "api.py"]` | El comando que corre **cada vez que arranca** un contenedor. |

### `compose.yaml`

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
  web:
    image: nginx:1.29
    ports:
      - "8081:80"
```

Dos servicios: `api` se construye con el `Dockerfile` de esta carpeta (`build: .`) y `web` usa la imagen de Nginx, ya hecha (`image:`). Cada uno publica su puerto.

---

## Preparación

La práctica se hace en **Windows**, con **PowerShell** y **Docker Desktop**. Si usas macOS o Linux, mira [al final](#si-usas-macos-o-linux).

### 1. Docker Desktop

Si todavía no lo tienes, instálalo con winget y reinicia la computadora cuando te lo pida:

```powershell
winget install --id Docker.DockerDesktop -e
```

**Abre Docker Desktop** y espera a que diga que está corriendo. Después, en PowerShell:

```powershell
docker --version
docker run hello-world
```

Debe responder la versión y, después, `Hello from Docker!`, como en la Sesión 27.

> Si responde `Cannot connect to the Docker daemon` o `error during connect`, Docker Desktop no está abierto: ábrelo, espera y vuelve a intentar.

### 2. Abrir la carpeta de la práctica

En PowerShell, entra a esta carpeta (`Sesion28\practica_cafe_nube\`) con `cd`. Todos los comandos que siguen se escriben ahí.

Esta vez **no** hace falta instalar Python ni Flask: los trae la imagen.

---

## Prueba 1. Construye la imagen

```powershell
docker build -t cafe-api .
```

`-t cafe-api` le pone nombre a la imagen y el `.` del final es la carpeta actual: ahí están el `Dockerfile` y los archivos que copia.

**Qué deberías ver** (la primera vez tarda: descarga la imagen de Python e instala Flask):

```text
[+] Building 9.8s (10/10) FINISHED
 => [1/5] FROM docker.io/library/python:3.12-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => naming to docker.io/library/cafe-api
```

Cada línea del `Dockerfile` es un paso: `[1/5]`, `[2/5]`… Ahora lista tus imágenes:

```powershell
docker images cafe-api
```

```text
IMAGE             ID             DISK USAGE   CONTENT SIZE
cafe-api:latest   9ad25f3c9695        159MB             0B
```

**Por qué:** la imagen guardó Python 3.12, Flask y `api.py`. Construir **no** enciende la API: `CMD` recién corre cuando arranca un contenedor.

---

## Prueba 2. Córrela y pide la carta

```powershell
docker run -d --name api -p 8080:8080 cafe-api
curl.exe localhost:8080/menu
```

`-d` la deja en segundo plano, `--name api` le pone nombre al contenedor y `-p 8080:8080` **publica el puerto**: lo que llega al 8080 de tu computadora pasa al 8080 del contenedor.

**Qué deberías ver:**

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Mocaccino","precio":12}]
```

Abre también **http://localhost:8080/menu** en el navegador. Luego mira lo que anotó la API:

```powershell
docker logs api
```

```text
 * Serving Flask app 'api'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
192.168.65.1 - - [12/Nov/2026 20:28:07] "GET /menu HTTP/1.1" 200 -
```

**Por qué:** es la misma API de la Sesión 27, pero ahora corre con el Python y el Flask **de la imagen**. Tu PowerShell quedó libre: los mensajes se leen con `docker logs`.

---

## Prueba 3. Una segunda copia

Corre otro contenedor de la misma imagen, también en el 8080:

```powershell
docker run -d --name api2 -p 8080:8080 cafe-api
```

**Qué deberías ver:**

```text
docker: Error response from daemon: ... Bind for 0.0.0.0:8080 failed: port is already allocated
```

El contenedor `api2` se creó, pero no arrancó. Bórralo y córrelo con **otro puerto de tu computadora**:

```powershell
docker rm api2
docker run -d --name api2 -p 8081:8080 cafe-api
curl.exe localhost:8081/menu
```

**Por qué:** cada contenedor tiene **sus propios** puertos, así que los dos escuchan en su 8080. Lo que no se puede repetir es el puerto de **tu computadora**: el primero usa el 8080 y el segundo, el 8081.

---

## Prueba 4. Otro puerto con una variable de entorno

`api.py` lee la variable `PUERTO` al encender. Pásasela al contenedor con `-e`:

```powershell
docker run -d --name api3 -e PUERTO=9090 -p 8082:9090 cafe-api
docker logs api3
curl.exe localhost:8082/menu
```

**Qué deberías ver** en los logs:

```text
 * Running on http://127.0.0.1:9090
```

y la misma carta en `localhost:8082/menu`. Ahora lista los contenedores:

```powershell
docker ps
```

Con las columnas resumidas:

```text
NAMES     IMAGE      STATUS          PORTS
api3      cafe-api   Up 2 seconds    0.0.0.0:8082->9090/tcp
api2      cafe-api   Up 4 seconds    0.0.0.0:8081->8080/tcp
api       cafe-api   Up 13 seconds   0.0.0.0:8080->8080/tcp
```

**Por qué:** la misma imagen corre con **otra configuración**, sin construirla de nuevo. Dentro de `api3`, la API escucha en el 9090, y por eso `-p` lleva al 9090: `8082:9090`.

---

## Prueba 5. Un café nuevo en la carta

Abre `api.py` y agrega un café a `MENU`:

```python
MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Mocaccino", "precio": 12},
    {"nombre": "Latte", "precio": 11},
]
```

Guarda el archivo y corre otra vez el contenedor `api`:

```powershell
docker rm -f api
docker run -d --name api -p 8080:8080 cafe-api
curl.exe localhost:8080/menu
```

`docker rm -f` lo detiene y lo borra de una vez.

**Qué deberías ver:** la carta **sin** el Latte. Ahora construye la imagen otra vez y vuelve a correrla:

```powershell
docker build -t cafe-api .
docker rm -f api
docker run -d --name api -p 8080:8080 cafe-api
curl.exe localhost:8080/menu
```

```text
 => CACHED [2/5] WORKDIR /app
 => CACHED [3/5] COPY requirements.txt .
 => CACHED [4/5] RUN pip install -r requirements.txt
 => [5/5] COPY . .
...
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Mocaccino","precio":12},{"nombre":"Latte","precio":11}]
```

**Por qué:** la imagen guardó una **copia** de `api.py` cuando se construyó. Para que traiga la nueva, hay que construirla otra vez. Fíjate en los `CACHED`: Docker no volvió a instalar Flask, porque `requirements.txt` no cambió; solo rehízo el último paso, `COPY . .`, y fue mucho más rápido.

Antes de seguir, borra los tres contenedores:

```powershell
docker rm -f api api2 api3
```

---

## Prueba 6. Dos servicios con Compose

Levanta la API y un Nginx con un solo comando:

```powershell
docker compose version
docker compose up -d
```

Se escribe `docker compose`, con espacio.

**Qué deberías ver:**

```text
[+] up 4/4
 ✔ Image practica_cafe_nube-api       Built
 ✔ Network practica_cafe_nube_default Created
 ✔ Container practica_cafe_nube-web-1 Started
 ✔ Container practica_cafe_nube-api-1 Started
```

Míralos, pídele la carta a la API y abre **http://localhost:8081** en el navegador (verás **Welcome to nginx!**):

```powershell
docker compose ps
curl.exe localhost:8080/menu
docker compose logs api
```

Lo que responde `docker compose ps`, con las columnas resumidas:

```text
NAME                       IMAGE                    SERVICE   STATUS         PORTS
practica_cafe_nube-api-1   practica_cafe_nube-api   api       Up 3 seconds   0.0.0.0:8080->8080/tcp
practica_cafe_nube-web-1   nginx:1.29               web       Up 3 seconds   0.0.0.0:8081->80/tcp
```

Cuando termines, bájalo todo:

```powershell
docker compose down
```

```text
[+] down 3/3
 ✔ Container practica_cafe_nube-web-1 Removed
 ✔ Container practica_cafe_nube-api-1 Removed
 ✔ Network practica_cafe_nube_default Removed
```

**Por qué:** `compose.yaml` describe los dos servicios, y cada comando actúa sobre **todos a la vez**. Compose nombra los contenedores con la carpeta, el servicio y un número: `practica_cafe_nube-api-1`. `down` borra los contenedores, pero las imágenes quedan para el próximo `up`.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Qué hace `docker build`? | Sigue el `Dockerfile` paso a paso y guarda la imagen `cafe-api` |
| 2 | ¿Cómo le llega un pedido a la API? | Por el puerto publicado: `-p 8080:8080` |
| 3 | ¿Dos copias en el 8080 de tu computadora? | No: `port is already allocated`. Con `-p 8081:8080`, sí |
| 4 | ¿Otra configuración sin otra imagen? | Sí: `-e PUERTO=9090` |
| 5 | ¿Un cambio en `api.py` se ve al correrla? | No: hay que construir otra vez. Flask queda `CACHED` |
| 6 | ¿Cómo se levantan varios servicios? | `docker compose up -d`, y se bajan con `docker compose down` |

---

## Reto

Agrega a `api.py` la ruta `GET /menu/<nombre>` del reto de la Sesión 27 y haz que funcione **en el contenedor de Compose**:

| Pedido | Respuesta | Código |
| --- | --- | --- |
| `localhost:8080/menu/capuchino` | `{"nombre":"Capuchino","precio":10}` | 200 |
| `localhost:8080/menu/te` | `{"error":"No lo tenemos en la carta"}` | 404 |

Pista: si después de `docker compose up -d` la ruta responde `Not Found`, recuerda la prueba 5. ¿Con qué opción le pides a Compose que construya otra vez?

---

## Apagar todo

```powershell
docker compose down
docker rm -f api api2 api3
```

El segundo comando solo hace falta si dejaste contenedores de las pruebas 2 a 5. Las imágenes quedan guardadas; se listan con `docker images`.

---

## Si usas macOS o Linux

Instala Docker Desktop desde `docs.docker.com` (en Linux, Docker Engine con el complemento de Compose) y ábrelo. Los comandos son los mismos; solo cambia `curl.exe` por `curl`.
