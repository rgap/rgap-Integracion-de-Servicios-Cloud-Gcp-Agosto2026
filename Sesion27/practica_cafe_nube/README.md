# Práctica: la API de Café Nube

**Sesión 27 · Python y Flask en tu computadora**

## El caso

**Café Nube** es una cafetería de barrio. Quiere mostrar su carta en internet, y el primer paso es un programa que entregue la lista de cafés y sus precios a otros programas, por ejemplo a una página web.

Ese programa es una **API**: no muestra páginas, **entrega datos**. Está escrito en **Python** con **Flask**, una biblioteca para hacer APIs con pocas líneas.

```
navegador o curl  ──  GET /menu  ──>  API de Café Nube (puerto 8080)
                  <──  la carta  ──
```

| Ruta | Qué responde |
| --- | --- |
| `GET /menu` | La carta: cada café con su nombre y su precio en soles |

En esta práctica vas a encender la API, pedirle la carta y ver qué necesita para funcionar: **Python**, **Flask** y **un puerto libre**.

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`api.py`](api.py) | El programa de la API. |
| [`requirements.txt`](requirements.txt) | La lista de bibliotecas que usa la API. Solo una: `flask==3.1.0`. |

### El programa, línea por línea

```python
import os

from flask import Flask, jsonify

app = Flask(__name__)

MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Mocaccino", "precio": 12},
]


@app.get("/menu")
def menu():
    return jsonify(MENU)


puerto = int(os.environ.get("PUERTO", 8080))
app.run(port=puerto)
```

| Línea | Qué hace |
| --- | --- |
| `from flask import Flask, jsonify` | Usa Flask. Si Flask no está instalado, el programa falla aquí. |
| `app = Flask(__name__)` | Crea la API. |
| `MENU = [...]` | La carta: tres cafés, cada uno con `nombre` y `precio`. |
| `@app.get("/menu")` | Cuando alguien pide la ruta `/menu`… |
| `return jsonify(MENU)` | …le responde la carta en **JSON**, el formato de texto con que los programas se pasan datos. |
| `os.environ.get("PUERTO", 8080)` | Lee la variable de entorno `PUERTO`. Si no existe, usa 8080. |
| `app.run(port=puerto)` | Enciende la API y la deja esperando pedidos en ese puerto. |

---

## Preparación

Necesitas **Python 3.10 o más nuevo**:

- macOS / Linux: `python3 --version`
- Windows: `python --version` (si no responde, prueba con `py --version`)

Abre una terminal **en esta carpeta** (`Sesion27/practica_cafe_nube/`) y crea un **entorno virtual**, como en la Sesión 11: una carpeta `.venv` con su propio Python, donde se instalan las bibliotecas de este proyecto.

**macOS / Linux:**

```bash
python3 -m venv .venv
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

Todavía **no** instales nada: la prueba 1 empieza así.

En el resto de la guía, los comandos van primero para macOS / Linux y después para Windows. Solo cambia la ruta al Python del entorno virtual: `.venv/bin/python` o `.venv\Scripts\python`.

---

## Prueba 1. ¿Qué pasa si falta Flask?

Enciende la API **sin haber instalado** `requirements.txt`:

```bash
.venv/bin/python api.py
```

```powershell
.venv\Scripts\python api.py
```

**Qué deberías ver:**

```text
Traceback (most recent call last):
  File ".../api.py", line 3, in <module>
    from flask import Flask, jsonify
ModuleNotFoundError: No module named 'flask'
```

**Por qué:** el código está completo, pero el entorno virtual está vacío: no tiene Flask. A esto se le llama **dependencia**: algo que el programa necesita para funcionar y que no es su propio código. Es el típico «en mi computadora sí funciona»: en la computadora de quien lo programó, Flask ya estaba instalado.

Ahora instala lo que pide `requirements.txt`:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
```

Al final debe decir `Successfully installed ... flask-3.1.0 ...`.

---

## Prueba 2. Pide la carta

Enciende la API:

```bash
.venv/bin/python api.py
```

```powershell
.venv\Scripts\python api.py
```

**Qué deberías ver** en la terminal:

```text
 * Serving Flask app 'api'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

La API quedó encendida en el puerto **8080** de tu computadora (`127.0.0.1`). La terminal se queda ocupada: déjala abierta. El `WARNING` es un aviso de Flask: este modo es para probar en tu computadora.

Abre en el navegador **http://localhost:8080/menu**. También puedes pedirla desde **otra terminal**:

```bash
curl localhost:8080/menu
```

```powershell
curl.exe localhost:8080/menu
```

**Qué deberías ver:**

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Mocaccino","precio":12}]
```

Vuelve a la terminal de la API: anotó cada pedido, con la ruta y un **código de respuesta**. `200` significa que salió bien.

```text
127.0.0.1 - - [10/Nov/2026 15:37:59] "GET /menu HTTP/1.1" 200 -
```

---

## Prueba 3. ¿Y una ruta que no existe?

Abre **http://localhost:8080/postres**.

**Qué deberías ver:** una página que dice **Not Found**, y en la terminal de la API:

```text
127.0.0.1 - - [10/Nov/2026 15:37:59] "GET /postres HTTP/1.1" 404 -
```

**Por qué:** la API solo conoce las rutas que tienen un `@app.get(...)`. Para cualquier otra responde **404**: no existe.

---

## Prueba 4. ¿Puedo encender la API dos veces?

Deja la primera API encendida. En **otra terminal**, en esta misma carpeta, enciéndela otra vez:

```bash
.venv/bin/python api.py
```

```powershell
.venv\Scripts\python api.py
```

**Qué deberías ver:**

```text
 * Serving Flask app 'api'
 * Debug mode: off
Address already in use
Port 8080 is in use by another program. Either identify and stop that program, or start the server with a different port.
```

**Por qué:** un puerto lo usa **un solo programa a la vez**. El 8080 ya lo tiene la primera API.

---

## Prueba 5. Otro puerto, sin cambiar el código

En esa segunda terminal, enciende la API con la variable de entorno `PUERTO`:

```bash
PUERTO=9090 .venv/bin/python api.py
```

```powershell
$env:PUERTO = "9090"
.venv\Scripts\python api.py
```

**Qué deberías ver:** `* Running on http://127.0.0.1:9090`. Abre **http://localhost:9090/menu**: la misma carta.

**Por qué:** `api.py` lee `PUERTO` al encender. Ahora tienes **dos copias** de la misma API, una en el 8080 y otra en el 9090. Cambiaste su configuración sin tocar el código.

> En Windows, `$env:PUERTO` queda puesta mientras esa terminal siga abierta. Para volver al 8080, cierra la terminal o escribe `Remove-Item Env:PUERTO`.

Apaga esta segunda copia con `Ctrl + C`.

---

## Prueba 6. Un café nuevo en la carta

Con la API del 8080 encendida, abre `api.py` y agrega un café a `MENU`:

```python
MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Mocaccino", "precio": 12},
    {"nombre": "Latte", "precio": 11},
]
```

Guarda el archivo y recarga **http://localhost:8080/menu**.

**Qué deberías ver:** la carta **sin** el Latte.

Ahora reinicia la API: `Ctrl + C` en su terminal y enciéndela otra vez. Recarga la página: ahora sí aparece.

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Mocaccino","precio":12},{"nombre":"Latte","precio":11}]
```

**Por qué:** la API leyó `api.py` una sola vez, al encender. Lo que cambies después en el archivo recién cuenta cuando la vuelves a encender.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Qué pasa si falta Flask? | `ModuleNotFoundError`: falta una dependencia |
| 2 | ¿Qué responde `/menu`? | La carta en JSON, con código `200` |
| 3 | ¿Y una ruta que no existe? | Código `404`: Not Found |
| 4 | ¿Puedo encender la API dos veces en el 8080? | No: `Address already in use` |
| 5 | ¿Puedo usar otro puerto sin cambiar el código? | Sí: `PUERTO=9090` |
| 6 | ¿Un cambio en `api.py` se ve al instante? | No: hay que volver a encender la API |

Para funcionar, la API necesita tres cosas además de su código: **Python**, **Flask** (lo que dice `requirements.txt`) y **un puerto libre**.

---

## Reto

Agrega la ruta `GET /menu/<nombre>`, que responda **un solo café**:

| Pedido | Respuesta | Código |
| --- | --- | --- |
| `/menu/capuchino` | `{"nombre":"Capuchino","precio":10}` | 200 |
| `/menu/te` | `{"error":"No lo tenemos en la carta"}` | 404 |

Pistas:

- `@app.get("/menu/<nombre>")` le pasa a tu función lo que venga después de `/menu/` en un parámetro `nombre`.
- Recorre `MENU` con un `for` y compara en minúsculas con `.lower()`, para que `capuchino` y `Capuchino` sean lo mismo.
- Para responder con otro código, devuelve dos cosas: `return jsonify({...}), 404`.

No olvides reiniciar la API para probarla.

---

## Apagar todo

- `Ctrl + C` en cada terminal donde esté encendida la API.
- La carpeta `.venv` puedes borrarla cuando termines: se vuelve a crear con los comandos de la preparación.
