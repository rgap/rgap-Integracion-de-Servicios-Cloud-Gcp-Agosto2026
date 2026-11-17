# Práctica: Café Nube con la página, la API y la base

**Sesión 29 · Varios contenedores con Docker Compose**

## El caso

En la Sesión 28 pusiste la API de **Café Nube** en una imagen. Ahora la cafetería quiere dos cosas más:

- Una **página** para ver el menú en el navegador.
- Guardar los **pedidos** en una base de datos **PostgreSQL**.

Son tres piezas, cada una en su contenedor. Con **Docker Compose** las levantas todas con un comando:

```
navegador  ──  localhost:8080  ──>  web (Nginx)  ──  api:8080  ──>  api (Flask)  ──  db:5432  ──>  db (PostgreSQL)
                                                                                                    └─ volumen datos
```

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`compose.yaml`](compose.yaml) | Los tres servicios: `web`, `api` y `db`. |
| [`web/`](web) | La página (`index.html` y `estilos.css`) y su `Dockerfile` con Nginx. |
| [`api/`](api) | La API de Café Nube, ahora con pedidos guardados en la base, y su `Dockerfile`. |

### `compose.yaml`

```yaml
services:
  web:
    build: ./web
    ports:
      - "8080:80"
    depends_on:
      - api
  api:
    build: ./api
    restart: on-failure
    environment:
      DATABASE_URL: postgresql://cafe:cafe@db:5432/cafe
    depends_on:
      - db
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: cafe
      POSTGRES_PASSWORD: cafe
      POSTGRES_DB: cafe
    volumes:
      - datos:/var/lib/postgresql/data

volumes:
  datos:
```

| Clave | Qué hace |
| --- | --- |
| `build: ./web` | Construye la imagen con el `Dockerfile` de la carpeta `web`. |
| `image: postgres:17` | Usa una imagen ya hecha, la de PostgreSQL 17. |
| `ports: "8080:80"` | Publica el puerto: el 8080 de tu computadora va al 80 de `web`. Solo `web` publica uno. |
| `environment:` | Las variables de entorno, lo que en la Sesión 28 era `-e`. |
| `DATABASE_URL` | Dónde está la base: en `db`, el nombre del servicio, puerto `5432`. |
| `depends_on:` | El orden de arranque: primero `db`, después `api`, después `web`. |
| `restart: on-failure` | Si la API arranca antes de que la base esté lista y falla, Docker la vuelve a arrancar. |
| `volumes:` | Guarda los archivos de la base en el volumen `datos`. Abajo, sin sangría, se declara. |

---

## Preparación

La práctica se hace en **Windows**, con **PowerShell** y **Docker Desktop**, como en la Sesión 28. **Abre Docker Desktop** y espera a que diga que está corriendo.

En PowerShell, entra a esta carpeta (`Sesion29\practica_cafe_nube\`) con `cd`. Todos los comandos se escriben ahí.

Si te quedó algún contenedor de la Sesión 28 en el 8080, bórralo:

```powershell
docker rm -f api api2 api3
```

---

## Prueba 1. Levanta todo

```powershell
docker compose up -d
```

**Qué deberías ver** (la primera vez tarda: construye dos imágenes y descarga PostgreSQL):

```text
 ✔ Image practica_cafe_nube-api        Built
 ✔ Image practica_cafe_nube-web        Built
 ✔ Network practica_cafe_nube_default  Created
 ✔ Volume practica_cafe_nube_datos     Created
 ✔ Container practica_cafe_nube-db-1   Started
 ✔ Container practica_cafe_nube-api-1  Started
 ✔ Container practica_cafe_nube-web-1  Started
```

**Por qué:** un solo comando construyó las imágenes, creó la red y el volumen, y arrancó los tres contenedores **en orden**: `db`, `api` y `web`.

---

## Prueba 2. Mira los contenedores y abre la página

```powershell
docker compose ps
```

Con las columnas resumidas:

```text
NAME                       SERVICE   STATUS         PORTS
practica_cafe_nube-api-1   api       Up 5 seconds   8080/tcp
practica_cafe_nube-db-1    db        Up 6 seconds   5432/tcp
practica_cafe_nube-web-1   web       Up 6 seconds   0.0.0.0:8080->80/tcp
```

Abre **http://localhost:8080** en el navegador: ves **Café Nube** y el menú.

**Por qué:** fíjate en `PORTS`. Solo `web` tiene `0.0.0.0:8080->80`: es el único que publica un puerto. `api` y `db` no se pueden abrir desde tu computadora; solo los alcanzan los otros contenedores.

---

## Prueba 3. Haz un pedido

```powershell
curl.exe localhost:8080/api/menu
curl.exe -X POST localhost:8080/api/pedidos -d producto=Capuchino
curl.exe localhost:8080/api/pedidos
```

El segundo `curl` no pide: **envía** un pedido. `-X POST` envía datos y `-d` son los datos.

**Qué deberías ver:**

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Latte","precio":12}]
{"ok":true}
[{"hora":"20:35","id":1,"precio":10,"producto":"Capuchino"}]
```

Mira lo que anotó la API:

```powershell
docker compose logs api
```

```text
api-1  | 172.24.0.4 - - [17/Nov/2026 20:35:52] "GET /menu HTTP/1.1" 200 -
api-1  | 172.24.0.4 - - [17/Nov/2026 20:35:52] "POST /pedidos HTTP/1.1" 201 -
api-1  | 172.24.0.4 - - [17/Nov/2026 20:35:52] "GET /pedidos HTTP/1.1" 200 -
```

**Por qué:** tú le pides a `web`, en el 8080. Nginx le pasa a la API todo lo que empieza con `/api/`, y la API guarda el pedido en la base.

---

## Prueba 4. La red: cada servicio por su nombre

Entra al contenedor `web` y pídele el menú a la API desde ahí, de dos formas:

```powershell
docker compose exec web curl http://api:8080/menu
docker compose exec web curl http://localhost:8080/menu
```

`docker compose exec web` corre un comando **dentro** del contenedor `web`.

**Qué deberías ver:**

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Latte","precio":12}]
curl: (7) Failed to connect to localhost port 8080 after 0 ms: Could not connect to server
```

**Por qué:** dentro de la red de Docker, la API está en `api`, el nombre de su servicio. En cambio, dentro de `web`, `localhost` es **el mismo** `web`, y ahí nadie escucha en el 8080. Por eso la API busca la base en `db:5432`, no en `localhost`.

---

## Prueba 5. Apaga y vuelve a levantar

```powershell
docker compose down
docker compose up -d
curl.exe localhost:8080/api/pedidos
```

**Qué deberías ver:**

```text
[{"hora":"20:35","id":1,"precio":10,"producto":"Capuchino"}]
```

**Por qué:** `down` borró los tres contenedores, pero **no** el volumen `datos`. La base nueva encontró ahí sus archivos, con el pedido.

---

## Prueba 6. Borra el volumen

```powershell
docker compose down -v
docker compose up -d
curl.exe localhost:8080/api/pedidos
```

**Qué deberías ver:**

```text
[]
```

En la salida de `down -v` aparece una línea más: `Volume practica_cafe_nube_datos Removed`.

**Por qué:** `-v` borra también el volumen, y con él los pedidos. Úsalo solo cuando quieras empezar de cero.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Cómo se levantan las tres piezas? | `docker compose up -d` |
| 2 | ¿Quién publica un puerto? | Solo `web`: `8080:80` |
| 3 | ¿Funciona la app entera? | La página, la API y la base guardan el pedido |
| 4 | ¿Cómo encuentra un contenedor a otro? | Por el nombre del servicio: `api:8080`, `db:5432` |
| 5 | ¿`down` borra los pedidos? | No: quedan en el volumen |
| 6 | ¿Y `down -v`? | Sí: borra el volumen |

---

## Si algo falla

| Lo que ves | Qué hacer |
| --- | --- |
| `port is already allocated` | Sigue corriendo un contenedor de la Sesión 28: `docker rm -f api api2 api3` |
| `502 Bad Gateway` | La API todavía arranca: espera unos segundos y vuelve a pedir |
| La página dice «Cargando…» y no cambia | Mira qué pasó con `docker compose logs api` |

---

## Reto

Haz que la página se abra en **http://localhost:8090** en lugar del 8080, cambiando **una sola línea** de `compose.yaml`. ¿Tienes que cambiar algo en la API o en la base?

---

## Apagar todo

```powershell
docker compose down
```

Si además quieres borrar los pedidos, usa `docker compose down -v`.

---

## Si usas macOS o Linux

Instala Docker Desktop desde `docs.docker.com` (en Linux, Docker Engine con el complemento de Compose) y ábrelo. Los comandos son los mismos; solo cambia `curl.exe` por `curl`.
