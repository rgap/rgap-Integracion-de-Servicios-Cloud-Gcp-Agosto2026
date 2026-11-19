# Sesión 30 — Redes, volúmenes y una introducción a Kubernetes

Presentación de **18 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, teoría, cierre y referencias. Las diapositivas **no tienen práctica**; la guía de la carpeta `practica_cafe_nube/` queda aparte. Es una **introducción**: una idea por diapositiva.

La revisión retoma la Sesión 29 (Compose, redes y volúmenes) y termina con Café Nube en una sola computadora: ¿y si se apaga?, ¿y si llegan diez veces más pedidos? De ahí salen las tres preguntas del día (redes y volúmenes, clúster y Kubernetes).

La teoría sigue los cursos **Varios contenedores con Compose** y **Kubernetes desde cero** (ruta *Despliegue con Docker*); el detalle se ve en la plataforma:

1. **Redes.** Cada contenedor tiene su IP (`172.24.0.3`), que se ve con `docker inspect`. La IP cambia al recrearlo; por eso se usa el nombre del servicio.
2. **¿Dónde quedan los archivos que copias?** `COPY` los mete en una capa de la imagen; `docker cp`, en la capa del contenedor, que `docker rm` borra. Todo vive en `/var/lib/docker`.
3. **¿`COPY` es lo mismo que un volumen?** No: una tabla los compara, y `docker volume inspect` muestra dónde está el volumen.
4. **Clúster y nodo: ¿de dónde vienen?** El origen de *cluster*, *nodo* y *Kubernetes*, y un clúster con su plano de control y tres nodos.
5. **Kubernetes: ¿por qué?** Lo que Compose no resuelve en una computadora, y qué es un orquestador.
6. **Pods y manifiestos.** Se describe lo que se quiere en YAML y se entrega con `kubectl apply -f`.
7. **Deployment.** Réplicas, labels y selector: si se borra un pod, aparece otro.
8. **Service.** Un nombre fijo, `api`, para pods que cambian de IP.
9. **kind y kubectl.** Un clúster dentro de Docker y los comandos de la guía.
10. **Google Cloud.** Cloud Build construye la imagen, Artifact Registry la guarda y GKE la corre.

- [Diapositivas PDF](slides/build/S30.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Guía aparte: Café Nube en Kubernetes con kind

No se presenta en las diapositivas. La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Son los archivos del escenario «Café Nube en Kubernetes» del curso. Los estudiantes crean un clúster de kind, despliegan la página y la API con tres réplicas, borran un pod para ver cómo vuelve y piden más copias.

Se hace en **Windows con PowerShell** y **Docker Desktop**, con `kind` y `kubectl`.

```powershell
kind create cluster --name cafe-nube                              # crea el clúster
kubectl apply -f deployment.yaml -f service.yaml -f web.yaml      # entrega los manifiestos
kubectl port-forward service/web 8080:80                          # abre la página en localhost:8080
```

| Archivo | Qué contiene |
| --- | --- |
| [`deployment.yaml`](practica_cafe_nube/deployment.yaml) | El Deployment `api`: tres réplicas de `cafe-api:1` |
| [`service.yaml`](practica_cafe_nube/service.yaml) | El Service `api`, en el 8080 |
| [`web.yaml`](practica_cafe_nube/web.yaml) | La página: dos réplicas de `cafe-web:1` y su Service `web` |
| [`api/`](practica_cafe_nube/api) | La API de Café Nube con el menú en el código (`GET /menu`) |
| [`web/`](practica_cafe_nube/web) | La página y Nginx, iguales a los de la Sesión 29 |

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `kind create cluster` y `kubectl get nodes` | Un nodo, `cafe-nube-control-plane`, que también aparece en `docker ps` |
| 2 | `docker build` y `kind load docker-image` | Las dos imágenes cargadas en el nodo |
| 3 | `kubectl apply` y `kubectl get pods -o wide` | Tres pods `api` y dos `web`, cada uno con su IP |
| 4 | `kubectl port-forward` y `curl.exe` | El menú, por la página y por `/api/menu` |
| 5 | `kubectl delete pod` | Aparece otro pod `api` con otro nombre |
| 6 | `kubectl scale deployment api --replicas=5` | `5/5` |

Termina con un reto: que la página corra en tres copias cambiando una línea. La solución está en [respuestas.md](respuestas.md).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 8 |
| Logro, saberes previos y utilidad | 4–6 | 5 |
| Teoría: redes y volúmenes | 7–9 | 15 |
| Teoría: clúster y Kubernetes | 10–15 | 37 |
| Teoría: Google Cloud | 16 | 10 |
| Cierre | 17–18 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S30.pdf
```
