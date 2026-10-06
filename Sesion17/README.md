# Sesión 17 — Ruta Associate Cloud Engineer: la consola de Google Cloud y Cloud Shell

Presentación de **37 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion16](../Sesion16/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. El tono es **intuitivo y progresivo**: cada término se define en la misma diapositiva, con una comparación cotidiana y una **alternativa popular fuera de Google** (GitHub, Drive, Codespaces, S3, VirtualBox…).

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Aplicativo: consola y Cloud Shell](apps/consola/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## La ruta que seguimos

Ruta **Certificación de Associate Cloud Engineer** en Google Skills (`skills.google/paths/11`), en orden:

| # | Actividad | En esta sesión |
| --- | --- | --- |
| 1 | Recorrido por los labs prácticos de Google Cloud (GSP282) | **Revisión de la sesión anterior**, en 3 diapositivas |
| 2 | Crea una guía de estudio para el examen de la certificación ACE | **1 diapositiva**: qué trae por dentro (NotebookLM, fuentes, instrucciones, modos de estudio). Queda de tarea |
| 3 | Infraestructura esencial de Google Cloud: conceptos básicos | **Lo principal**: la introducción con las imágenes del curso y el primer lab, tarea por tarea |

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 10 | Revisión (el recorrido por los labs, 3 diapositivas), logro, saberes previos, utilidad |
| Guía de estudio ACE | 8 | 2 | Qué hay dentro del curso |
| Infraestructura esencial | 9–18 | 20 | Mapa del curso, qué es la nube, ecosistema, regiones y zonas, opciones de cómputo, las cuatro formas de interactuar, consola, `gcloud` y Cloud Shell |
| El lab, tarea por tarea | 19–32 | 25 | Bucket, las 6 tareas del lab, vocabulario de terminal, variables, `.profile` y errores frecuentes |
| Práctica | 33–34 | 15 | Simulador de Cloud Shell e inicio del lab real |
| Cierre | 35–37 | 8 | Preguntas para comprobar y referencias |

## Las imágenes

Las siete capturas del curso están en `slides/assets/` y aparecen en este orden:

| Diapositiva | Archivo | Qué muestra |
| --- | --- | --- |
| 12 | `gc-ecosistema.png` | Las tres capas: Google Cloud, productos de Google y ecosistema |
| 13 | `gc-mapa-regiones.png` | Regiones, puntos de presencia y red |
| 14 | `gc-opciones-computo.png` | Compute Engine, GKE, App Engine, Cloud Functions y Cloud Run |
| 15 | `gc-cuatro-formas.png` | Consola, Cloud Shell y CLI, API REST y app móvil |
| 16 | `gc-consola.png` | La lista de VMs en la consola |
| 17 | `gc-cli.png` | La misma lista con `gcloud compute instances list` |
| 18 | `gc-cloud-shell.png` | Cloud Shell abierto desde la consola |

## El aplicativo

`apps/consola/index.html` es una sola página, sin dependencias, que se abre con doble clic:

1. **Repaso:** cinco preguntas de verdadero o falso sobre el recorrido por los labs y la sesión anterior.
2. **Simulador de Cloud Shell:** una terminal de mentira que entiende los comandos del lab (`gcloud storage buckets create`, `gcloud storage cp`, variables, `mkdir`, `touch`, `echo >>`, `source`, `nano .profile`). Tiene un botón para **cerrar y volver a abrir** la sesión, que muestra qué se pierde y qué no, y seis misiones que se marcan solas.
3. **¿Consola o Cloud Shell?:** casos para elegir la herramienta.
4. **¿A qué se parece?:** cada pieza de Google Cloud con su parecido fuera de Google.

## Criterio de redacción

Nivel principiante: ningún término se usa sin definir (servidor, nube, región, zona, punto de presencia, contenedor, CLI, API, bucket, objeto, terminal, shell, variable de entorno, `.profile`). Las comparaciones se repiten a propósito para dar continuidad: la **cabina de Internet** explica primero la plataforma de labs y luego Cloud Shell. Los nombres de las actividades, las duraciones y qué alternativas tienen plan gratuito son **datos que cambian**: conviene revisarlos antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex`, agrega `listings` con el estilo de la Sesión 11 y busca las imágenes primero en `slides/assets/`.
