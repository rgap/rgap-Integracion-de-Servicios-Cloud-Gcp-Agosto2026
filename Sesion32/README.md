# Sesión 32 — Pruebas de rendimiento: carga, estrés y red

Presentación de **24 diapositivas** para una clase de 80 minutos: revisión, logro, saberes previos, utilidad, teoría, cierre y referencias. Las diapositivas **no tienen práctica**; la guía de la carpeta `practica_cafe_nube/` queda aparte. Es una **introducción**: una idea por diapositiva.

La revisión resume la Sesión 31 en tres diapositivas:

1. **App Engine y Cloud Run.** Qué se sube en cada uno, con qué comando y qué URL devuelve; los dos son sin servidores y `--max-instances` pone un tope.
2. **Revisiones y tráfico.** Una revisión por cambio, `--no-traffic` y un canary del 10 %.
3. **Apache Bench.** `ab -n 200 -c 20` y cómo leer `Failed requests`, `Requests per second` y `95%`. Termina con las tres preguntas del día.

Los saberes previos preguntan definiciones (prueba de carga, instancia, IP interna, zona y región, Cloud Monitoring) y qué hacen `ab`, `ping`, `--max-instances` y una regla de firewall.

1. **Funcionales y no funcionales.** `curl $CR/menu` responde «¿hace lo que debe?» con sí o no. Las no funcionales responden «¿qué tan bien lo hace?» con un número y una meta: rendimiento, disponibilidad y seguridad. Hoy, rendimiento.
2. **Carga y estrés.** Dos gráficos de usuarios en el tiempo: la carga que se espera y una carga que sube hasta romper.
3. **Los tres números.** Pedidos por segundo, tiempo de respuesta y errores. Por qué el p95 y no el promedio, con 100 pedidos ordenados.
4. **Prueba de carga: primero, la meta.** Café Nube con 20 usuarios; la meta y una tabla con ✓.
5. **Prueba de estrés: el punto de quiebre.** Una tabla de 20 a 200 usuarios: los pedidos por segundo dejan de subir, el p95 se dispara y aparecen errores 429.
6. **Cuatro herramientas.** `ab`, k6, `ping` e iperf3: qué pregunta responde cada una y cuáles miden la aplicación o la red.
7. **k6.** El guion de carga (`vus`, `duration`, `thresholds`, `check`, `sleep`), cómo correrlo con Docker y leer ✓ y ✗, y el guion de estrés con `stages`.
8. **Los mismos números en `ab`, k6 y Cloud Run > Métricas.** Desde afuera y desde adentro, con Cloud Monitoring.
9. **Rendimiento de red.** Una diapositiva que solo dice «Rendimiento de red» abre el tema. Después: ancho de banda, latencia y pérdida de paquetes; bits y bytes.
10. **iperf3.** Servidor y cliente, el puerto 5201 y cómo leer `Bitrate` y `Retr`.
11. **La red en Google Cloud.** Misma zona y otra región: la latencia sube y, con una conexión, el ancho de banda baja. La regla `default-allow-internal` y el tope de una `e2-medium`.
12. **Performance Dashboard.** La latencia y la pérdida de paquetes que mide Google entre sus zonas, y cómo verla.

- [Diapositivas PDF](slides/build/S32.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Guía aparte: ¿cuánto aguanta Café Nube? Carga, estrés y red

No se presenta en las diapositivas. La guía completa está en [`practica_cafe_nube/README.md`](practica_cafe_nube/README.md). Los estudiantes suben la API de Café Nube de la Sesión 31 a Cloud Run con una sola instancia, la prueban con `ab` y k6, buscan su punto de quiebre y miden con `ping` e iperf3 la red entre tres VMs.

Se hace en **Cloud Shell**, en un proyecto de Google Cloud. k6 corre con Docker, que Cloud Shell ya trae.

```bash
docker run --rm -i grafana/k6 run -e URL=$CR - < carga.js     # prueba de carga
docker run --rm -i grafana/k6 run -e URL=$CR - < estres.js    # prueba de estrés
iperf3 -s                                                      # en la VM servidor
iperf3 -c 10.128.0.2                                           # en las VMs cliente
```

| Archivo | Qué contiene |
| --- | --- |
| [`carga.js`](practica_cafe_nube/carga.js) | Guion de k6: 20 usuarios durante 30 s, con la meta p95 < 300 ms y menos de 1 % de errores |
| [`estres.js`](practica_cafe_nube/estres.js) | Guion de k6: los usuarios suben de 0 a 200, sin pausa, con la misma meta |

La API no cambia: se construye desde [`../Sesion31/practica_cafe_nube/cloudrun/`](../Sesion31/practica_cafe_nube/cloudrun).

| Prueba | Qué se hace | Qué se ve |
| --- | --- | --- |
| 1 | `gcloud run deploy` con `--max-instances 1` y `curl` | El menú: una prueba funcional |
| 2 | `ab -n 1000 -c 20` y k6 con `carga.js` | Los mismos números en las dos, y ✓ en la meta |
| 3 | k6 con `estres.js` | ✗ en la meta, errores 429 y los gráficos de **Cloud Run > Métricas** |
| 4 | `ping` e `iperf3` entre `servidor`, `cliente-cerca` y `cliente-lejos` | Latencia y ancho de banda en la misma zona y en otra región |
| 5 | **Performance Dashboard**, pestaña **Google Cloud** | La latencia que mide Google entre `us-central1` y `southamerica-west1` |

Termina con un reto: repetir la prueba de estrés con `--max-instances 3`. La solución está en [respuestas.md](respuestas.md).

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–4 | 8 |
| Logro, saberes previos y utilidad | 5–7 | 7 |
| Teoría: funcionales, no funcionales, carga y estrés | 8–12 | 20 |
| Teoría: herramientas y k6 | 13–17 | 20 |
| Teoría: rendimiento de red | 18–22 | 20 |
| Cierre | 23–24 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S32.pdf
```
