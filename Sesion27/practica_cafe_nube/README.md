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

En esta práctica vas a instalar Python, encender la API, pedirle la carta y ver qué necesita para funcionar: **Python**, **Flask** y **un puerto libre**.

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

La práctica se hace en **Windows**, con **PowerShell**. Si usas macOS o Linux, mira [al final](#si-usas-macos-o-linux).

### 1. Instalar Python

Abre PowerShell e instala Python 3.12 con **winget**, el instalador de programas que trae Windows:

```powershell
winget install --id Python.Python.3.12 -e
```

`--id Python.Python.3.12` elige el paquete y `-e` pide que el nombre coincida exacto, para que no instale otro parecido.

### 2. Comprobar que `python` responde

**Cierra PowerShell y ábrelo otra vez**: una ventana que ya estaba abierta no ve los programas que se instalan después. Luego:

```powershell
python --version
```

Debe responder `Python 3.12.x`.

> Si abre la Microsoft Store o dice `Python was not found`, cierra y abre PowerShell una vez más. Si sigue igual, en **Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones**, apaga los dos alias de `python.exe` y `python3.exe`.

### 3. Abrir la carpeta de la práctica

En PowerShell, entra a esta carpeta (`Sesion27/practica_cafe_nube/`) con `cd`. Todos los comandos que siguen se escriben ahí.

Todavía **no** instales nada: la prueba 1 empieza así.

---

## Prueba 1. ¿Qué pasa si falta Flask?

Enciende la API **sin haber instalado** `requirements.txt`:

```powershell
python api.py
```

**Qué deberías ver:**

```text
Traceback (most recent call last):
  File "...\api.py", line 3, in <module>
    from flask import Flask, jsonify
ModuleNotFoundError: No module named 'flask'
```

**Por qué:** el código está completo, pero el Python que acabas de instalar no trae Flask. A esto se le llama **dependencia**: algo que el programa necesita para funcionar y que no es su propio código. Es el típico «en mi computadora sí funciona»: en la computadora de quien lo programó, Flask ya estaba instalado.

> Si ya habías instalado Flask antes, la API va a encender. No pasa nada: lee el porqué y sigue.

Ahora instala lo que pide `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

`pip` es el instalador de bibliotecas de Python, como en la Sesión 11. Al final debe decir `Successfully installed ... flask-3.1.0 ...`.

---

## Prueba 2. Pide la carta

Enciende la API:

```powershell
python api.py
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

Abre en el navegador **http://localhost:8080/menu**. También puedes pedirla desde **otra ventana de PowerShell**:

```powershell
curl.exe localhost:8080/menu
```

Se escribe `curl.exe`, con `.exe`: en PowerShell, `curl` a secas es otro comando.

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

Deja la primera API encendida. En **otra ventana de PowerShell**, en esta misma carpeta, enciéndela otra vez:

```powershell
python api.py
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

En esa segunda ventana, pon la variable de entorno `PUERTO` y enciende la API:

```powershell
$env:PUERTO = "9090"
python api.py
```

**Qué deberías ver:** `* Running on http://127.0.0.1:9090`. Abre **http://localhost:9090/menu**: la misma carta.

**Por qué:** `api.py` lee `PUERTO` al encender. Ahora tienes **dos copias** de la misma API, una en el 8080 y otra en el 9090. Cambiaste su configuración sin tocar el código.

> `$env:PUERTO` queda puesta mientras esa ventana siga abierta. Para volver al 8080, ciérrala o escribe `Remove-Item Env:PUERTO`.

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

- `Ctrl + C` en cada ventana donde esté encendida la API.

---

## Si usas macOS o Linux

Ahí el Python del sistema no deja instalar bibliotecas con `pip` (responde `error: externally-managed-environment`). Por eso, en macOS y Linux se usa un **entorno virtual**, como en la Sesión 11: una carpeta `.venv` con su propio Python.

```bash
python3 -m venv .venv                                  # crea el entorno virtual
.venv/bin/python api.py                                # prueba 1: falta Flask
.venv/bin/python -m pip install -r requirements.txt    # instala lo de requirements.txt
.venv/bin/python api.py                                # enciende la API
```

En las pruebas, cambia `python` por `.venv/bin/python` y `curl.exe` por `curl`. En la prueba 5, la variable va en la misma línea: `PUERTO=9090 .venv/bin/python api.py`.
