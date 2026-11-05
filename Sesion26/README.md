# Sesión 26 — Balanceo de carga, CDN y contenedores

Presentación de **26 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 25: revisión, logro, saberes previos, utilidad, tres partes de teoría, dos prácticas, cierre y referencias. Es una **introducción**: una idea por diapositiva, sin detalles de configuración.

La revisión retoma la Sesión 25 (supervisión y alta disponibilidad) y termina con tres servidores `web-1`, `web-2` y `web-3`: de ahí salen las tres preguntas del día. La teoría tiene tres partes cortas:

1. **Balanceo de carga:** un solo servidor forma una cola (6 reportes de 5 s: el último espera 30 s); el balanceador recibe a todos en una sola dirección y reparte; *round robin* (30 s → 10 s con tres servidores); qué pasa si un servidor se cae.
2. **CDN:** copias de los archivos cerca del cliente (primera vez y siguientes veces) y qué va en la CDN y qué no. Cloud CDN en una línea.
3. **Contenedores:** el problema de preparar cada servidor, imagen y contenedor, el `Dockerfile` de la tienda, Docker Compose (un archivo, un comando), Kubernetes («quiero 3 copias») y una tabla final: Docker empaqueta, Compose junta y Kubernetes mantiene.

Hay dos prácticas, las dos en la carpeta [`practica_balanceo/`](practica_balanceo/) y en la computadora del estudiante:

- **Práctica 1: balanceo con Nginx.** Tres servidores Node.js detrás de Nginx con *round robin* y seis pruebas guiadas.
- **Práctica 2: la misma tienda con Docker Compose.** Los mismos cuatro programas, ahora como contenedores que se encienden con un solo comando.

- [Diapositivas PDF](slides/build/S26.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Práctica 1: balanceo con Nginx

La guía completa está en [`practica_balanceo/README.md`](practica_balanceo/README.md). Pedidos Express prepara su tienda online para el Cyber Day con tres copias del servidor (`node server.js 3001`, `3002` y `3003`) detrás de Nginx en `localhost:8080`. El script `prueba.js` simula clientes y muestra qué servidor respondió a cada uno y cuánto tardó.

| Prueba | Comando | Qué se ve |
| --- | --- | --- |
| 1 | `node prueba.js / 6 --en-fila` | Turnos 3001 → 3002 → 3003 → 3001… |
| 2 | `node prueba.js /productos 6 --directo 3001` | 6 consultas en 2 s con un solo servidor (solo espera) |
| 3 | `node prueba.js /reporte 6 --directo 3001` | Cola de CPU: el sexto cliente espera 30 s |
| 4 | `node prueba.js /reporte 6` | Con Nginx y tres servidores: 10 s |
| 5 | `/reporte 1` y, en otra terminal, `/ 6` | Las visitas que le tocan al servidor ocupado esperan |
| 6 | Apagar el 3002 y `node prueba.js / 6 --en-fila` | Nginx reparte entre los que quedan; nadie ve un error |

Solo se usan módulos de Node.js (`import` de `node:http`, `node:timers/promises` y `node:process`), sin `npm install`. Requiere Node.js 18 o más nuevo y Nginx (macOS: `brew install nginx`; Ubuntu: `apt install nginx`; Windows: el `.zip` de nginx.org). Las seis pruebas se verificaron con Node.js 22 y Nginx 1.27; los tiempos de las pruebas 3 y 4 suponen al menos 3 núcleos de CPU. Si falta tiempo en clase, las pruebas 5 y 6 quedan para casa.

## Práctica 2: la misma tienda con Docker Compose

Usa tres archivos de la misma carpeta:

| Archivo | Qué contiene |
| --- | --- |
| [`Dockerfile`](practica_balanceo/Dockerfile) | La imagen de la tienda: `node:22-alpine` + `server.js` |
| [`compose.yaml`](practica_balanceo/compose.yaml) | `tienda1`, `tienda2` y `tienda3` (la misma imagen, puertos 3001–3003) y `nginx` (imagen `nginx:1.27-alpine`, puerto 8080) |
| [`nginx-docker.conf`](practica_balanceo/nginx-docker.conf) | El `nginx.conf` de la Práctica 1 con los nombres de servicio (`tienda1:3001`…) en lugar de `127.0.0.1` |

```bash
docker compose up --build -d
docker compose ps
node prueba.js / 6 --en-fila
docker compose down
```

Requiere Docker Desktop. Si los estudiantes no lo tienen instalado, el docente la hace como demostración. Se verificó con Docker 29: las pruebas dan los mismos resultados que en la Práctica 1. La guía de la carpeta trae además cómo repetir la prueba 6 apagando un contenedor.

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 5 |
| Logro, saberes previos y utilidad | 4–6 | 4 |
| Parte 1: balanceo de carga | 7–11 | 10 |
| Parte 2: CDN | 12–14 | 6 |
| Parte 3: contenedores | 15–21 | 12 |
| Práctica 1: balanceo con Nginx | 22–23 | 28 |
| Práctica 2: Docker Compose | 24 | 10 |
| Cierre | 25–26 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S26.pdf
```
