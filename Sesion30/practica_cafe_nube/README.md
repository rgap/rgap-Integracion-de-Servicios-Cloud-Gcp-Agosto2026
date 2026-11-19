# Práctica: Café Nube en Kubernetes con kind

**Sesión 30 · Redes, volúmenes y una introducción a Kubernetes**

## El caso

En la Sesión 29, Café Nube corría con Docker Compose: la página, la API y la base, en **una sola computadora**. Si esa computadora se apaga, la app se cae. Y los lunes a primera hora todos piden el menú a la vez: una sola copia de la API no alcanza.

Hoy llevas la **página** y la **API** a un clúster de Kubernetes que corre en tu computadora, con **kind**:

- La API corre en **tres copias**. Si una se cae, Kubernetes crea otra sola.
- La página corre en **dos copias**.
- Nginx sigue buscando la API por su nombre, `api:8080`, como en Compose.

```
navegador ── localhost:8080 ── port-forward ──> Service web ──> pods web (×2) ── api:8080 ──> Service api ──> pods api (×3)
                                               └──────────────────── clúster de kind ─────────────────────────────────┘
```

La base de datos queda fuera: en Kubernetes necesita más piezas.

---

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| [`deployment.yaml`](deployment.yaml) | El Deployment `api`: tres copias del pod con la imagen `cafe-api:1`. |
| [`service.yaml`](service.yaml) | El Service `api`: el nombre fijo de la API, en el 8080. |
| [`web.yaml`](web.yaml) | La página: su Deployment, con dos copias de `cafe-web:1`, y su Service `web`, separados por `---`. |
| [`api/`](api) | La API de Café Nube de la Sesión 28, con el menú en el código, y su `Dockerfile`. |
| [`web/`](web) | La página y Nginx, iguales a los de la Sesión 29. |

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: cafe-api:1
          ports:
            - containerPort: 8080
```

| Clave | Qué hace |
| --- | --- |
| `kind: Deployment` | El tipo de objeto: uno que mantiene corriendo un número de pods iguales. |
| `name: api` | Su nombre. |
| `replicas: 3` | Cuántas copias del pod quieres. |
| `selector:` | Cuáles pods son suyos: los que llevan la label `app: api`. |
| `template:` | Cómo es cada pod. Sus `labels:` dicen `app: api`, lo mismo que busca el `selector:`. |
| `image: cafe-api:1` | La imagen del contenedor. La construyes tú y la cargas en kind. |
| `containerPort: 8080` | En qué puerto escucha la API, como `EXPOSE` en el Dockerfile. |

### `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - port: 8080
      targetPort: 8080
```

| Clave | Qué hace |
| --- | --- |
| `name: api` | El nombre fijo. Nginx busca la API en `api:8080`, igual que en Compose. |
| `selector:` | Reparte los pedidos entre los pods con `app: api`. |
| `port: 8080` | Donde recibe el Service. |
| `targetPort: 8080` | Donde escucha el contenedor. |

---

## Preparación

La práctica se hace en **Windows**, con **PowerShell** y **Docker Desktop**, como en la Sesión 29. **Abre Docker Desktop** y espera a que diga que está corriendo.

Instala **kind** y **kubectl** en PowerShell. Después cierra PowerShell y vuelve a abrirlo:

```powershell
winget install Kubernetes.kind Kubernetes.kubectl
```

Si te quedó Café Nube de la Sesión 29 corriendo, entra a su carpeta y bájalo, porque usa el 8080:

```powershell
docker compose down
```

Luego entra a esta carpeta (`Sesion30\practica_cafe_nube\`) con `cd`. Todos los comandos se escriben ahí.

---

## Prueba 1. Crea el clúster

```powershell
kind create cluster --name cafe-nube
kubectl get nodes
```

La primera vez tarda un par de minutos: descarga la imagen del nodo.

**Qué deberías ver** (con las columnas resumidas):

```text
NAME                      STATUS   ROLES
cafe-nube-control-plane   Ready    control-plane
```

Si dice `NotReady`, espera unos segundos y vuelve a preguntar.

Ahora mira tus contenedores de Docker:

```powershell
docker ps
```

Aparece un contenedor llamado `cafe-nube-control-plane`.

**Por qué:** kind arma el clúster **dentro de Docker**: cada nodo es un contenedor. Tu clúster tiene **un solo nodo**, que es a la vez el plano de control y la máquina que corre los pods.

---

## Prueba 2. Construye las imágenes y cárgalas en el clúster

```powershell
docker build -t cafe-api:1 api
docker build -t cafe-web:1 web
kind load docker-image cafe-api:1 cafe-web:1 --name cafe-nube
```

**Qué deberías ver** al final:

```text
Image: "cafe-api:1" with ID "sha256:…" not yet present on node "cafe-nube-control-plane", loading...
Image: "cafe-web:1" with ID "sha256:…" not yet present on node "cafe-nube-control-plane", loading...
```

**Por qué:** las imágenes que construyes quedan en tu Docker, pero el nodo **no las ve**. `kind load docker-image` se las copia. En un clúster de verdad, como GKE, el clúster las descarga de un registro, como Artifact Registry.

---

## Prueba 3. Entrega los manifiestos

```powershell
kubectl apply -f deployment.yaml -f service.yaml -f web.yaml
kubectl get pods
```

**Qué deberías ver** (tus nombres terminan distinto):

```text
deployment.apps/api created
service/api created
deployment.apps/web created
service/web created

NAME                  READY   STATUS    RESTARTS   AGE
api-5c8d7f9b6-2kqxz   1/1     Running   0          9s
api-5c8d7f9b6-7hwmt   1/1     Running   0          9s
api-5c8d7f9b6-vp4nr   1/1     Running   0          9s
web-6f7b9c5d8-5tqbn   1/1     Running   0          8s
web-6f7b9c5d8-m8zrd   1/1     Running   0          8s
```

Si alguno dice `ContainerCreating`, espera unos segundos y vuelve a preguntar.

**Por qué:** no le diste órdenes una por una: le **describiste** lo que quieres, tres copias de la API y dos de la página, y Kubernetes las creó.

Mira también la IP de cada pod y en qué nodo corre:

```powershell
kubectl get pods -o wide
```

En la columna `IP` cada pod tiene la suya, como `10.244.0.5`, y en `NODE` todos dicen `cafe-nube-control-plane`.

---

## Prueba 4. Abre la página

`kubectl port-forward` abre un túnel desde tu computadora hasta el Service `web`, como `-p` en Docker. **La terminal queda ocupada** mientras el túnel está abierto:

```powershell
kubectl port-forward service/web 8080:80
```

```text
Forwarding from 127.0.0.1:8080 -> 80
```

Abre una **segunda ventana de PowerShell** y pide el menú:

```powershell
curl.exe localhost:8080/api/menu
```

**Qué deberías ver:**

```text
[{"nombre":"Americano","precio":8},{"nombre":"Capuchino","precio":10},{"nombre":"Latte","precio":12}]
```

Abre también **http://localhost:8080** en el navegador: ves **Café Nube** y el menú, ahora en Kubernetes.

**Por qué:** el pedido entra por el túnel al Service `web`, que lo pasa a uno de los dos pods de Nginx. Nginx le pasa `/api/menu` al Service `api`, que lo reparte entre los tres pods de la API.

Deja el túnel abierto y sigue en la segunda ventana.

---

## Prueba 5. Borra un pod y mira cómo vuelve

Copia el nombre de uno de tus pods `api-…` de la Prueba 3 y bórralo:

```powershell
kubectl delete pod TU-POD
kubectl get pods
```

**Qué deberías ver:**

```text
pod "api-5c8d7f9b6-7hwmt" deleted

NAME                  READY   STATUS    RESTARTS   AGE
api-5c8d7f9b6-2kqxz   1/1     Running   0          2m
api-5c8d7f9b6-h6wcs   1/1     Running   0          3s
api-5c8d7f9b6-vp4nr   1/1     Running   0          2m
web-6f7b9c5d8-5tqbn   1/1     Running   0          2m
web-6f7b9c5d8-m8zrd   1/1     Running   0          2m
```

Vuelve a pedir el menú: sigue respondiendo.

```powershell
curl.exe localhost:8080/api/menu
```

**Por qué:** el Deployment pide tres pods con `app: api`. Vio que había dos y **creó otro**, con un nombre nuevo (fíjate en el `AGE` de `3s`) y una IP nueva. El Service lo sumó solo, por su label: Nginx no tuvo que cambiar nada.

---

## Prueba 6. Pide más copias

```powershell
kubectl scale deployment api --replicas=5
kubectl get deployment api
```

**Qué deberías ver:**

```text
deployment.apps/api scaled

NAME   READY   UP-TO-DATE   AVAILABLE   AGE
api    5/5     5            5           3m
```

**Por qué:** `kubectl scale` cambia cuántas copias pide el Deployment. Ojo: si vuelves a aplicar `deployment.yaml`, que dice `replicas: 3`, vuelven a ser tres. Para que dure, cámbialo en el archivo.

---

## Resumen

| Prueba | Pregunta | Resultado |
| --- | --- | --- |
| 1 | ¿Qué es un nodo en kind? | Un contenedor de Docker: `cafe-nube-control-plane` |
| 2 | ¿Cómo llegan tus imágenes al clúster? | `kind load docker-image` |
| 3 | ¿Cómo se le pide algo a Kubernetes? | Con manifiestos y `kubectl apply -f` |
| 4 | ¿Cómo entras desde tu computadora? | `kubectl port-forward service/web 8080:80` |
| 5 | ¿Qué pasa si se borra un pod? | El Deployment crea otro y el Service lo suma |
| 6 | ¿Cómo pides más copias? | `kubectl scale deployment api --replicas=5` |

---

## Si algo falla

| Lo que ves | Qué hacer |
| --- | --- |
| `kind` o `kubectl` no se reconoce | Cierra PowerShell y vuelve a abrirlo después de instalarlos |
| `ErrImagePull` o `ImagePullBackOff` | El nodo no tiene la imagen: repite el `kind load docker-image` de la Prueba 2 |
| `address already in use` en el 8080 | Sigue corriendo Café Nube de la Sesión 29: `docker compose down` en su carpeta |
| `502 Bad Gateway` | La API todavía arranca: espera unos segundos y vuelve a pedir |

---

## Reto

Haz que la **página** corra en **tres** copias, cambiando **una sola línea** de un archivo. ¿Qué comando usas para entregarle el cambio al clúster? ¿Tienes que tocar algo de la API?

---

## Apagar todo

En la primera ventana, pulsa **Ctrl+C** para cerrar el túnel. Después borra el clúster entero, con todos sus pods:

```powershell
kind delete cluster --name cafe-nube
```

---

## Si usas macOS o Linux

Con Docker Desktop abierto, instala kind y kubectl: en Mac, con `brew install kind kubectl`; en Linux, con las guías de `kind.sigs.k8s.io` y `kubernetes.io`. Los comandos son los mismos; solo cambia `curl.exe` por `curl`.
