# Sesión 25 — Supervisión, alta disponibilidad y balanceo de carga

Presentación de **31 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 24: revisión, logro, saberes previos, utilidad, tres partes de teoría, dos prácticas, cierre y referencias.

La revisión retoma BigQuery con la práctica **BigQuery sin BigQuery**: los estudiantes repiten con Python y DuckDB las consultas del lab de la sesión anterior y comparan sus resultados. La teoría tiene tres partes cortas para principiantes:

1. **Supervisar recursos:** métricas, registros y alertas; las métricas que más se revisan; cómo leer una gráfica de uso de CPU; los problemas que ocurren seguido; Google Cloud Observability (Cloud Monitoring y Cloud Logging) y cómo funciona una política de alertas.
2. **Alta disponibilidad:** qué significa 99 %, 99.9 % y 99.99 %, el punto único de falla y cómo se evita en Google Cloud (grupo de instancias administrado en varias zonas, Cloud SQL con alta disponibilidad y Cloud Storage).
3. **Balanceo de carga y CDN:** el balanceador con una sola IP, la verificación de estado, los balanceadores de aplicaciones y de red, el autoescalado, Cloud CDN y un diagrama final con todo junto.

Hay dos prácticas:

- **Práctica 1: balanceo con Nginx** (carpeta [`practica_balanceo/`](practica_balanceo/)). Es un caso de estudio en la computadora del estudiante: tres servidores Node.js detrás de Nginx con *round robin* y seis pruebas guiadas.
- **Práctica 2:** el laboratorio **[Supervisa recursos con Google Cloud Observability](https://www.skills.google/catalog_lab/1785)**.

- [Diapositivas PDF](slides/build/S25.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Revisión: BigQuery sin BigQuery

En la carpeta [`practica/`](practica/) está el notebook [`practica_bigquery_python.ipynb`](practica/practica_bigquery_python.ipynb). Repite las consultas del lab de la Sesión 24 con Python y DuckDB sobre 1.2 millones de pedidos de Pedidos Express (2023–2025), sin usar Google Cloud.

- Se abre en Google Colab (*Archivo → Subir cuaderno*) o en Jupyter / VS Code.
- **De dónde salen los datos:** no se descargan. La primera celda del notebook escribe y ejecuta [`generar_ventas.py`](practica/generar_ventas.py), que crea `ventas.csv` (1.2 millones de filas, unos 105 MB). Los datos usan una semilla fija, así que todos obtienen los mismos resultados.
- Para abrirlo desde Colab: *Archivo → Abrir cuaderno → GitHub*, pegar `github.com/rgap/rgap-Integracion-de-Servicios-Cloud-Gcp-Agosto2026` y elegir `Sesion25/practica/practica_bigquery_python.ipynb`.
- Termina con cinco retos; las soluciones están en [respuestas.md](respuestas.md).

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

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión: BigQuery sin BigQuery | 1–4 | 12 |
| Logro, saberes previos y utilidad | 5–7 | 3 |
| Parte 1: supervisar recursos | 8–15 | 10 |
| Parte 2: alta disponibilidad | 16–19 | 5 |
| Parte 3: balanceo de carga y CDN | 20–26 | 8 |
| Práctica 1: balanceo con Nginx | 27–28 | 14 |
| Práctica 2: laboratorio | 29 | 24 |
| Cierre | 30–31 | 4 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S25.pdf
```
