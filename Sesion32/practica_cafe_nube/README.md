# Práctica: ¿cuánto aguanta Café Nube? Carga, estrés y red

**Sesión 32 · Pruebas de rendimiento: carga, estrés y red**

## El caso

En la Sesión 31 subiste la API de Café Nube a Cloud Run y la mediste con Apache Bench. Hoy respondes tres preguntas con números:

1. **Prueba de carga:** con 20 usuarios a la vez, ¿cumple la meta? La meta: 95 de cada 100 pedidos en menos de **300 ms** y menos del **1 %** con error.
2. **Prueba de estrés:** si los usuarios suben hasta 200 a la vez, ¿dónde se rompe?
3. **Prueba de red:** entre dos máquinas virtuales, ¿cuántos datos pasan por segundo? ¿Cambia si la otra máquina está lejos?

```
                        ┌── ab y k6 ────> Cloud Run (cafe-api) ──> Cloud Run > Métricas
Cloud Shell (gcloud) ───┤
                        └── crea las VMs ─> servidor y cliente-cerca (us-central1-a)
                                            cliente-lejos (southamerica-west1-a)
                                            iperf3 y ping entre ellas ──> Performance Dashboard
```

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`carga.js`](carga.js) | Guion de k6 para la **prueba de carga**: 20 usuarios durante 30 segundos, con una meta. |
| [`estres.js`](estres.js) | Guion de k6 para la **prueba de estrés**: los usuarios suben de 0 a 200. |
| [`../../Sesion31/practica_cafe_nube/cloudrun/`](../../Sesion31/practica_cafe_nube/cloudrun) | La API de Café Nube y su `Dockerfile`, de la Sesión 31. No cambia. |

### `carga.js`

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 20,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<300'], // 95 de cada 100 pedidos en menos de 300 ms
    http_req_failed: ['rate<0.01'],   // menos del 1 % de pedidos con error
  },
};

export default function () {
  const res = http.get(`${__ENV.URL}/menu`);
  check(res, { 'responde 200': (r) => r.status === 200 });
  sleep(1);
}
```

| Parte | Qué hace |
| --- | --- |
| `vus: 20` | 20 **usuarios virtuales** (VUs) a la vez. Es lo mismo que `-c 20` en `ab`. |
| `duration: '30s'` | La prueba dura 30 segundos. |
| `thresholds` | La **meta**. Si no se cumple, k6 marca la prueba con ✗. |
| `export default function` | Lo que hace **cada usuario**, una y otra vez, hasta que termina la prueba. |
| `__ENV.URL` | La URL de tu API. Se la pasas al correr k6 con `-e URL=...`. |
| `check(...)` | Revisa que cada respuesta sea `200`. |
| `sleep(1)` | El usuario espera 1 segundo antes de volver a pedir, como alguien que lee el menú. |

### `estres.js`

Tiene la misma meta y el mismo pedido. Cambian dos cosas:

```javascript
  stages: [
    { duration: '30s', target: 20 },
    { duration: '30s', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 200 },
    { duration: '10s', target: 0 },
  ],
```

| Cambio | Qué hace |
| --- | --- |
| `stages` | En vez de 20 usuarios fijos, los **sube poco a poco**: a 20 en 30 s, a 50, a 100, a 200, y al final baja a 0. Dura 2 min 10 s. |
| Sin `sleep(1)` | Cada usuario vuelve a pedir **apenas** recibe la respuesta. Así la carga es mucho mayor. |

---

## Preparación

Necesitas un **proyecto de Google Cloud** donde puedas crear recursos.

1. Abre la consola de Google Cloud, elige tu proyecto arriba y haz clic en **Activar Cloud Shell**.
2. En Cloud Shell, descarga el material del curso y entra a esta carpeta:

```bash
git clone https://github.com/rgap/rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026.git
cd rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026/Sesion32/practica_cafe_nube
```

3. Habilita las APIs que vas a usar. Si aparece **Autorizar Cloud Shell**, haz clic en **Autorizar**:

```bash
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com compute.googleapis.com
```

---

## Prueba 1. Café Nube en Cloud Run, con una sola instancia

Es la API de la Sesión 31. Si ya borraste el servicio, vuelve a crearlo. Si el repositorio `cafe` ya existe, salta el primer comando.

```bash
gcloud artifacts repositories create cafe --repository-format=docker --location=us-central1
IMAGEN=us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/cafe/cafe-api
gcloud builds submit --tag $IMAGEN:v1 ../../Sesion31/practica_cafe_nube/cloudrun
gcloud run deploy cafe-api --image $IMAGEN:v1 --region us-central1 --allow-unauthenticated --max-instances 1
```

El último dato de `gcloud builds submit` es la carpeta con el `Dockerfile`: la de la Sesión 31.

**Qué deberías ver** al final:

```text
Service URL: https://cafe-api-123456789.us-central1.run.app
```

Copia tu **Service URL** en la variable `CR` y pide el menú:

```bash
CR=https://cafe-api-123456789.us-central1.run.app
curl $CR/menu
```

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Latte","precio":12}]
```

**Por qué:** ese `curl` es una **prueba funcional**: responde «¿hace lo que debe?». Devuelve el menú, así que sí. Las pruebas de hoy son **no funcionales**: «¿qué tan bien lo hace con muchos usuarios?». Con `--max-instances 1`, Cloud Run usa **una sola instancia**: así el punto de quiebre llega antes y cuesta menos.

---

## Prueba 2. Prueba de carga: ¿cumple la meta?

Primero, la prueba de la Sesión 31 con Apache Bench: 1000 pedidos, 20 a la vez.

```bash
ab -n 1000 -c 20 $CR/menu
```

Si dice `command not found`: `sudo apt-get install -y apache2-utils`. Anota `Failed requests`, `Requests per second` y la línea `95%`.

Ahora la misma carga con **k6**. Cloud Shell trae Docker, así que corres k6 con su imagen oficial, `grafana/k6`, sin instalar nada:

```bash
docker run --rm -i grafana/k6 run -e URL=$CR - < carga.js
```

| Parte | Qué hace |
| --- | --- |
| `docker run --rm -i grafana/k6` | Arranca un contenedor con k6 y lo borra al terminar. `-i` deja que le pases el guion. |
| `run -e URL=$CR` | Corre una prueba y le pasa tu URL al guion, en `__ENV.URL`. |
| `- < carga.js` | El guion es `carga.js`. El `-` le dice a k6 que lo lea de la entrada. |

La primera vez descarga la imagen. Después, la prueba dura 30 segundos.

**Qué deberías ver** (tus números serán otros):

```text
  █ THRESHOLDS

    http_req_duration
    ✓ 'p(95)<300' p(95)=142.6ms

    http_req_failed
    ✓ 'rate<0.01' rate=0.00%

  █ TOTAL RESULTS

    checks_succeeded...: 100.00% 540 out of 540
    ✓ responde 200

    HTTP
    http_req_duration..............: avg=121.3ms min=98.2ms med=115.4ms max=1.31s p(90)=135.1ms p(95)=142.6ms
    http_req_failed................: 0.00%  0 out of 540
    http_reqs......................: 540    17.9/s
```

| Línea | Qué te dice |
| --- | --- |
| `✓ 'p(95)<300'` | **Se cumplió** la meta de tiempo: el p95 fue 142.6 ms. Con ✗, no se cumplió. |
| `✓ 'rate<0.01'` | **Se cumplió** la meta de errores: 0 % falló. |
| `http_req_duration` | Cuánto tardó cada pedido: promedio (`avg`), el más rápido, el del medio (`med`), el más lento y el p95. |
| `http_req_failed` | Cuántos pedidos fallaron. |
| `http_reqs` | Cuántos pedidos hubo en total y **cuántos por segundo**. |

**Por qué:** `ab` y k6 miden lo mismo: pedidos por segundo, tiempo de respuesta y errores. k6, además, **compara con tu meta** y te dice si pasó o no. ¿Por qué son casi 18 pedidos por segundo? Cada usuario pide, espera la respuesta y después 1 segundo más: 20 usuarios dan un poco menos de 20 pedidos por segundo.

Si el `max` es de más de un segundo, fue el primer pedido: esperó a que arrancara la instancia.

---

## Prueba 3. Prueba de estrés: ¿dónde se rompe?

Abre otra pestaña del navegador con la consola, en **Cloud Run > cafe-api > Métricas**. Ahí verás la prueba desde el lado del servidor.

En Cloud Shell, corre el guion de estrés. Dura 2 minutos y 10 segundos:

```bash
docker run --rm -i grafana/k6 run -e URL=$CR - < estres.js
```

Mientras corre, k6 muestra cuántos usuarios hay en ese momento:

```text
running (1m05.0s), 052/200 VUs, 41230 complete and 0 interrupted iterations
```

**Qué podrías ver** al final (tus números serán otros):

```text
  █ THRESHOLDS

    http_req_duration
    ✗ 'p(95)<300' p(95)=1.21s

    http_req_failed
    ✗ 'rate<0.01' rate=6.84%

  █ TOTAL RESULTS

    checks_succeeded...: 93.15% 152400 out of 163600
    ✗ responde 200
      ↳  93% — ✓ 152400 / ✗ 11200

    HTTP
    http_req_duration..............: avg=402.5ms min=95.1ms med=231.7ms max=10.2s p(90)=930.4ms p(95)=1.21s
    http_req_failed................: 6.84%  11200 out of 163600
    http_reqs......................: 163600 1258.4/s

level=error msg="thresholds on metrics 'http_req_duration, http_req_failed' have been crossed"
```

**Qué significa:** con muchos usuarios, la única instancia ya no da abasto. Los pedidos **esperan más** (el p95 pasó de 300 ms) y algunos **fallan**. Esos fallos suelen ser el error **`429`**: Cloud Run llegó a su máximo de instancias, `1`, y no tiene dónde atender el pedido.

Ahora mira **Cloud Run > cafe-api > Métricas**. Puede tardar un par de minutos en aparecer:

| Gráfico | Qué ves |
| --- | --- |
| **Cantidad de solicitudes** (*Request count*) | Los pedidos por segundo. Si hubo fallos, aparece una línea de `4xx`. |
| **Latencias de solicitudes** (*Request latencies*) | El tiempo de respuesta, que sube con los usuarios. |
| **Cantidad de instancias de contenedor** (*Container instance count*) | Siempre 1: es el máximo que le diste. |
| **Uso de CPU del contenedor** (*Container CPU utilization*) | Cerca del 100 %: la instancia está al límite. |

**El punto de quiebre** es el número de usuarios donde el tiempo **se dispara** o aparecen **errores**. Busca en los gráficos a qué hora pasó, y en la escalera de `estres.js` cuántos usuarios había.

**¿Tu prueba pasó con ✓?** Entonces la API aguantó 200 usuarios y aún no encontraste su límite. Cambia `200` por `400` en `estres.js` (`nano estres.js`, guarda con **Ctrl+O** y sal con **Ctrl+X**) y repite.

---

## Prueba 4. Prueba de red con iperf3 y ping

Ahora mides **la red**, no la API. Creas tres máquinas virtuales: dos en la **misma zona** y una en **otra región**, en Santiago de Chile.

```bash
gcloud compute instances create servidor cliente-cerca --zone us-central1-a --machine-type e2-medium
gcloud compute instances create cliente-lejos --zone southamerica-west1-a --machine-type e2-medium
gcloud compute instances list
```

**Qué deberías ver** (tus IPs serán otras):

```text
NAME           ZONE                  MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS
cliente-lejos  southamerica-west1-a  e2-medium                  10.194.0.2   34.x.x.x     RUNNING
cliente-cerca  us-central1-a         e2-medium                  10.128.0.3   34.x.x.x     RUNNING
servidor       us-central1-a         e2-medium                  10.128.0.2   34.x.x.x     RUNNING
```

Anota la **IP interna** de `servidor`. En los comandos de abajo, cambia `10.128.0.2` por la tuya.

**Por qué no creas una regla de firewall:** las tres están en la red `default`. Su regla `default-allow-internal` deja pasar todo entre IPs internas: el `ping` y el puerto **5201**, el de iperf3.

### El servidor

En la consola, ve a **Compute Engine > Instancias de VM** y haz clic en **SSH** en la fila de `servidor`. Se abre una ventana con su terminal. Instala iperf3 y arráncalo como **servidor**:

```bash
sudo apt-get update
sudo apt-get install -y iperf3
iperf3 -s
```

Si aparece una pantalla que pregunta si iperf3 debe arrancar solo como servicio (*daemon*), deja **No** y presiona **Intro**: lo arrancas tú con `iperf3 -s`.

**Qué deberías ver:**

```text
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```

Deja esa ventana abierta: el servidor espera.

### El cliente cerca: misma zona

Abre **SSH** en la fila de `cliente-cerca`. Instala iperf3, mide la latencia con `ping` y el ancho de banda con `iperf3 -c`:

```bash
sudo apt-get update
sudo apt-get install -y iperf3
ping -c 5 10.128.0.2
iperf3 -c 10.128.0.2
```

**Qué deberías ver** (tus números serán otros):

```text
rtt min/avg/max/mdev = 0.212/0.298/0.501/0.102 ms
...
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  2.25 GBytes  1.93 Gbits/sec    0             sender
[  5]   0.00-10.04  sec  2.25 GBytes  1.92 Gbits/sec                  receiver

iperf Done.
```

| Línea | Qué te dice |
| --- | --- |
| `rtt ... avg` | La **latencia**: cuánto tarda un paquete en ir y volver, en promedio. Aquí, 0.3 ms. |
| `Interval 0.00-10.00 sec` | iperf3 mandó datos durante **10 segundos**. |
| `Transfer` | Cuántos datos pasaron en total. |
| `Bitrate` | El **ancho de banda**: cuántos bits pasaron por segundo. El número principal. |
| `Retr` | Paquetes que hubo que volver a enviar. Muchos indican **pérdida**. |

**Por qué 1.93 Gbits/sec:** una VM `e2-medium` puede enviar **hasta 2 Gbits/s**. En la misma zona, la red da casi todo eso.

### El cliente lejos: otra región

Abre **SSH** en la fila de `cliente-lejos` y repite lo mismo, con la **misma IP** de `servidor`:

```bash
sudo apt-get update
sudo apt-get install -y iperf3
ping -c 5 10.128.0.2
iperf3 -c 10.128.0.2
```

Anota tus números:

| | `cliente-cerca` (misma zona) | `cliente-lejos` (otra región) |
| --- | --- | --- |
| Latencia (`ping`, `avg`) | | |
| Ancho de banda (`iperf3`, `Bitrate`) | | |
| Reenvíos (`Retr`) | | |

**Por qué:** los datos viajan miles de kilómetros, así que la latencia pasa de menos de 1 ms a más de 100 ms. Con una sola conexión, el emisor manda un bloque de datos y espera la confirmación antes de mandar más. Si la confirmación tarda más en volver, pasan menos datos por segundo.

Al terminar, en la ventana de `servidor` presiona **Ctrl+C** para detener iperf3.

---

## Prueba 5. Performance Dashboard: la latencia que mide Google

Google mide todo el tiempo la latencia y la pérdida de paquetes entre sus zonas. Lo puedes ver sin crear nada.

1. En la barra de búsqueda de la consola escribe **Performance Dashboard** y ábrelo. Es parte de **Network Intelligence Center**.
2. Haz clic en la pestaña **Google Cloud**.
3. En **Traffic type**, elige **Cross-zonal**. En **Metric**, elige **Latency (RTT)**.
4. En **Google Cloud regions**, elige `us-central1` y `southamerica-west1`.
5. Haz clic en un cuadro del mapa de calor que une las dos regiones.

Si tu consola está en español, esos nombres pueden salir traducidos.

**Qué deberías ver:** la latencia mediana entre zonas, en milisegundos. Compárala con tu `ping` desde `cliente-lejos`: deberían ser parecidas.

**Por qué:** si tu app va lenta, este panel te ayuda a separar dos problemas: ¿es tu app o es la red de Google? Si la red está normal, el problema está en tu app.

---

## Resumen

| Prueba | Pregunta | Herramienta | Dónde lo ves en Google Cloud |
| --- | --- | --- | --- |
| 1 | ¿Hace lo que debe? (funcional) | `curl` | — |
| 2 | ¿Cumple la meta con 20 usuarios? (carga) | `ab` y k6 con `carga.js` | Cloud Run > Métricas |
| 3 | ¿Dónde se rompe? (estrés) | k6 con `estres.js` | Cloud Run > Métricas |
| 4 | ¿Qué tan rápida es la red entre VMs? | `ping` e `iperf3` | Compute Engine |
| 5 | ¿Cómo está la red de Google? | — | Performance Dashboard |

---

## Si algo falla

| Lo que ves | Qué hacer |
| --- | --- |
| `curl`, `ab` o k6 no encuentran la URL | Cloud Shell se reinició y perdió las variables: vuelve a escribir `CR=…` e `IMAGEN=…` |
| `carga.js: No such file or directory`, o k6 se queda esperando | Estás en otra carpeta o falta el `<`: entra a `Sesion32/practica_cafe_nube` y revisa `- < carga.js` |
| k6: todos los pedidos fallan | Revisa que `$CR` no termine en `/`: el guion ya agrega `/menu` |
| `iperf3: error - unable to connect to server` | El servidor no está corriendo (`iperf3 -s`) o la IP no es la **interna** de `servidor` |
| `iperf3: error - the server is busy running a test` | Otro cliente está midiendo. Espera a que termine y repite |
| `ping` e `iperf3` no responden | En **Red de VPC > Firewall**, revisa que exista `default-allow-internal`. Si no está: `gcloud compute firewall-rules create default-allow-internal --network default --allow tcp,udp,icmp --source-ranges 10.128.0.0/9` |
| No puedes crear la VM en `southamerica-west1-a` | Usa otra zona lejana, como `southamerica-east1-a` |

---

## Reto

Con `--max-instances 1`, la API se rompió en la prueba de estrés. Sube el máximo a **3 instancias** y repite **la misma** prueba de estrés. ¿Cambia el p95? ¿Cambia el porcentaje de errores? ¿Cuántas instancias ves en **Cantidad de instancias de contenedor**? Pista: `gcloud run services update cafe-api` tiene la opción `--max-instances`.

---

## Apagar todo

Borra las VMs, el servicio de Cloud Run y el repositorio con la imagen. Responde `Y` en cada uno:

```bash
gcloud compute instances delete servidor cliente-cerca --zone us-central1-a
gcloud compute instances delete cliente-lejos --zone southamerica-west1-a
gcloud run services delete cafe-api --region us-central1
gcloud artifacts repositories delete cafe --location=us-central1
```

---

## k6 en tu computadora

k6 también corre en tu computadora, contra la URL de Cloud Run:

- **Con Docker Desktop** (Windows, macOS o Linux): el mismo comando, desde la carpeta `practica_cafe_nube`. En PowerShell, cambia `- < carga.js` por `-` y pasa el archivo con `Get-Content`:

```powershell
Get-Content carga.js | docker run --rm -i grafana/k6 run -e URL=https://cafe-api-123456789.us-central1.run.app -
```

- **Sin Docker:** instálalo con `brew install k6` (macOS) o `winget install k6 --source winget` (Windows), y corre `k6 run -e URL=$CR carga.js`.
