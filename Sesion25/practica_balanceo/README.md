# Práctica: balanceo de carga con Nginx

**Sesión 25 · Caso de estudio: la tienda online de Pedidos Express**

## El caso

Pedidos Express abre su tienda online y se acerca el Cyber Day. El equipo encendió **tres copias del mismo servidor** (Node.js) y puso delante **Nginx** como balanceador. Los clientes solo conocen una dirección: `localhost:8080`.

```
                         ┌──> servidor 3001
clientes ──> Nginx :8080 ├──> servidor 3002
                         └──> servidor 3003
```

Nginx reparte por **turnos** (*round robin*): la primera solicitud va al 3001, la segunda al 3002, la tercera al 3003, la cuarta otra vez al 3001, y así.

La tienda atiende cuatro operaciones:

| Ruta | Qué hace | Cuánto tarda | Qué hace el servidor mientras tanto |
| --- | --- | --- | --- |
| `GET /` | Muestra la página principal | Nada | — |
| `GET /productos` | Consulta productos en la base de datos | 2 s | **Espera** la respuesta de la base |
| `POST /comprar` | Cobra la compra con el banco | 5 s | **Espera** la respuesta del banco |
| `GET /reporte` | Calcula un reporte de ventas | 5 s | **Trabaja**: la CPU calcula sin parar |

Antes del Cyber Day, el equipo quiere responder seis preguntas. Cada pregunta es una prueba.

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`server.js`](server.js) | El servidor de la tienda. Se ejecuta tres veces, una por puerto. |
| [`nginx.conf`](nginx.conf) | La configuración de Nginx: el grupo `tienda` con los tres servidores. |
| [`prueba.js`](prueba.js) | Simula clientes: envía varias solicitudes y muestra qué servidor respondió cada una y cuánto tardó. |
| [`package.json`](package.json) | Solo indica `"type": "module"`, para poder usar `import` en los archivos `.js`. |

No hay nada que instalar con `npm`: solo se importan módulos que ya trae Node.js (`node:http`, `node:timers/promises` y `node:process`).

---

## Preparación

### 1. Instalar Node.js y Nginx

- **Node.js 18 o más nuevo** (`node --version`).
- **Nginx:**
  - macOS: `brew install nginx`
  - Ubuntu / WSL: `sudo apt install nginx`
  - Windows: descarga el `.zip` de *nginx/Windows* en `nginx.org/en/download.html` y descomprímelo, por ejemplo en `C:\nginx`.

### 2. Encender los tres servidores

Abre **tres terminales** en esta carpeta, una por servidor:

```bash
node server.js 3001
node server.js 3002
node server.js 3003
```

Cada terminal debe mostrar `Servidor de la tienda escuchando en el puerto ...`. Déjalas abiertas y a la vista: ahí verás qué servidor atiende cada solicitud.

### 3. Encender Nginx

Abre una **cuarta terminal** en esta carpeta.

**macOS:**

```bash
nginx -p "$PWD" -c nginx.conf -t     # revisa que la configuración esté bien
nginx -p "$PWD" -c nginx.conf        # enciende Nginx
```

**Ubuntu / WSL:** los mismos comandos con `sudo` delante.

**Windows:** copia `nginx.conf` de esta carpeta encima de `C:\nginx\conf\nginx.conf`. Luego, en `C:\nginx`:

```bat
nginx -t
start nginx
```

`-p "$PWD"` le dice a Nginx que trabaje en esta carpeta y `-c nginx.conf` qué configuración usar. Por eso aparecen aquí `nginx.pid`, `error.log` y unas carpetas `temp_*`.

### 4. Cómo leer el resultado de `prueba.js`

Abre una **quinta terminal** para las pruebas. Ejemplo:

```text
$ node prueba.js /productos 3

3 × GET /productos  →  Nginx (puerto 8080)

  #   servidor        tardó
  1   3001            2.0 s
  2   3002            2.0 s
  3   3003            2.0 s

Reparto: 3001: 1   3002: 1   3003: 1
Tiempo total: 2.0 s
```

- **servidor:** qué copia atendió esa solicitud (lo responde el propio servidor).
- **tardó:** cuánto esperó ese cliente.
- **Reparto:** cuántas solicitudes atendió cada servidor.
- **Tiempo total:** cuánto pasó desde la primera solicitud hasta la última respuesta.

Opciones:

| Opción | Qué hace |
| --- | --- |
| `--en-fila` | Envía una solicitud, espera la respuesta y recién envía la siguiente. |
| `--directo 3001` | Le pide directamente al servidor 3001, **sin pasar por Nginx**. |

---

## Prueba 1. ¿Nginx reparte por turnos?

```bash
node prueba.js / 6 --en-fila
```

**Qué deberías ver:**

```text
  #   servidor        tardó
  1   3001            0.0 s
  2   3002            0.0 s
  3   3003            0.0 s
  4   3001            0.0 s
  5   3002            0.0 s
  6   3003            0.0 s

Reparto: 3001: 2   3002: 2   3003: 2
```

**Por qué:** eso es *round robin*: un turno para cada servidor, en orden, y se vuelve a empezar. Mira las tres terminales de los servidores: cada una imprime dos `INICIO GET /`. El cliente siempre habló con `localhost:8080`; nunca supo que había tres servidores.

> Puede que la vuelta no empiece en el 3001: Nginx sigue los turnos donde quedaron en la prueba anterior. Lo importante es el orden 3001 → 3002 → 3003 → 3001.

---

## Prueba 2. Si el servidor solo espera, ¿atiende a varios a la vez?

Primero, **un solo servidor y sin Nginx**:

```bash
node prueba.js /productos 6 --directo 3001
```

**Qué deberías ver:** las 6 solicitudes tardan **2 s** cada una y el tiempo total es **2 s**, no 12 s.

**Por qué:** durante esos 2 s el servidor no trabaja: está esperando a la base de datos. Mientras espera, Node.js recibe a los siguientes clientes. Las 6 esperas ocurren al mismo tiempo.

Ahora a través de Nginx, con compras:

```bash
node prueba.js /comprar 3
```

**Qué deberías ver:** una compra en cada servidor, todas en **5 s**, total **5 s**.

**Conclusión:** para operaciones que **esperan** (base de datos, banco), un solo servidor ya atiende a muchos clientes a la vez.

---

## Prueba 3. Si el servidor trabaja con la CPU, ¿qué pasa?

Seis reportes a **un solo servidor, sin Nginx**:

```bash
node prueba.js /reporte 6 --directo 3001
```

**Qué deberías ver:**

```text
  #   servidor        tardó
  1   3001            5.0 s
  2   3001           10.0 s
  3   3001           15.0 s
  4   3001           20.0 s
  5   3001           25.0 s
  6   3001           30.0 s

Tiempo total: 30.0 s
```

**Por qué:** un reporte ocupa la CPU 5 s sin parar. Un proceso de Node.js hace **un cálculo a la vez**, así que los reportes forman una cola: el sexto cliente espera 30 s. En la terminal del 3001 verás que cada `INICIO` empieza recién cuando termina el anterior.

---

## Prueba 4. ¿El balanceador ayuda con los reportes?

Los mismos seis reportes, ahora **a través de Nginx**:

```bash
node prueba.js /reporte 6
```

**Qué deberías ver:** dos reportes por servidor. Tres clientes reciben su reporte a los **5 s** y los otros tres a los **10 s**. Tiempo total: **10 s**.

**Por qué:** Nginx reparte los 6 reportes entre 3 servidores (2 cada uno). Los tres calculan al mismo tiempo, cada uno en un núcleo de tu CPU.

| | Un servidor | Tres servidores con Nginx |
| --- | ---: | ---: |
| 6 reportes | 30 s | 10 s |

> Los tiempos dependen de tu computadora. Si tiene menos de 3 núcleos, la mejora será menor.

---

## Prueba 5. ¿Round robin sabe si un servidor está ocupado?

Necesitas **dos terminales** de prueba.

1. En la primera, pide un reporte. Ese servidor quedará ocupado 5 s:

```bash
node prueba.js /reporte 1
```

2. **Antes de que pasen 5 s**, en la segunda terminal envía 6 visitas a la página principal:

```bash
node prueba.js / 6
```

**Qué deberías ver** en la segunda terminal (los números de servidor pueden cambiar):

```text
  #   servidor        tardó
  1   3002            0.0 s
  2   3001            4.0 s   <- le tocó al servidor ocupado
  3   3003            0.0 s
  4   3002            0.0 s
  5   3003            0.0 s
  6   3001            4.0 s   <- también
```

**Por qué:** round robin solo cuenta turnos; no mira si el servidor está ocupado. El servidor que calcula el reporte no puede atender a nadie. Cuando le toca su turno, esa visita a la página principal, que debía ser inmediata, espera hasta que termine el reporte.

**Conclusión:** con round robin, un servidor ocupado hace esperar a los clientes que le tocan. Por eso conviene que todas las copias sean iguales y que ninguna operación pesada tarde demasiado.

---

## Prueba 6. ¿Qué pasa si se cae un servidor?

1. En la terminal del servidor **3002**, presiona `Ctrl + C` para apagarlo.
2. Envía visitas a la tienda:

```bash
node prueba.js / 6 --en-fila
```

**Qué deberías ver:** las 6 solicitudes responden bien; solo aparecen **3001** y **3003**. Ningún cliente ve un error. Puede que uno de los dos reciba una más que el otro: se quedó con el turno que era del 3002.

**Por qué:** cuando a Nginx le toca el turno del 3002 y no logra conectarse, reenvía esa misma solicitud al siguiente servidor. Además, deja de enviarle solicitudes al 3002 durante **10 segundos** y luego vuelve a intentarlo. El intento fallido queda anotado en `error.log`:

```text
connect() failed (Connection refused) while connecting to upstream, ... upstream: "http://127.0.0.1:3002/"
```

3. Vuelve a encender el 3002 (`node server.js 3002`), espera unos 10 segundos y repite la prueba: el 3002 vuelve a recibir turnos.

> Nginx se entera de la falla **cuando una solicitud falla**. El balanceador de Google Cloud, en cambio, pregunta a cada VM cada pocos segundos con una **verificación de estado** y deja de enviarle tráfico antes de que un cliente lo note.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Nginx reparte por turnos? | Sí: 3001 → 3002 → 3003 → 3001… |
| 2 | Si el servidor solo espera, ¿atiende a varios? | Sí: 6 consultas en 2 s con un solo servidor |
| 3 | Si trabaja con la CPU, ¿qué pasa? | Forman cola: 6 reportes tardan 30 s |
| 4 | ¿El balanceador ayuda con los reportes? | Sí: 6 reportes en 10 s con tres servidores |
| 5 | ¿Round robin sabe si un servidor está ocupado? | No: le envía clientes igual, y esos esperan |
| 6 | ¿Qué pasa si se cae un servidor? | Nginx reparte entre los que quedan; nadie ve un error |

## Apagar todo

- Servidores: `Ctrl + C` en cada terminal.
- Nginx en macOS: `nginx -p "$PWD" -c nginx.conf -s stop` (en Ubuntu / WSL, con `sudo`).
- Nginx en Windows: `nginx -s stop` dentro de `C:\nginx`.

Si cambias `nginx.conf` con Nginx encendido, recarga la configuración con `-s reload` en lugar de `-s stop`.
