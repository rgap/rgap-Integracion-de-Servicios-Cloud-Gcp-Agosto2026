# Sesión 13 — Dónde se despliega hoy, qué cobran y cómo empezar con Google Skills

Presentación de **20 diapositivas**, nivel principiante, con la estructura docente de la [Sesion12](../Sesion12/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas de todas las preguntas](respuestas.md)

## Orden de la teoría

| Bloque | Diapositivas | Contenido |
| --- | --- | --- |
| Servicios de despliegue en 2026 | 2 | Nubes grandes (AWS, Azure, Google Cloud, otros) y plataformas para desarrolladores (Vercel, Cloudflare Pages, Netlify, GitHub Pages, Firebase, Supabase, Render, Railway, Cloud Run), de más a menos usada |
| Qué cobran como límite al mes | 4 | Tiempo de cómputo, transferencia de datos, compilaciones y despliegues, almacenamiento y base de datos (más "se duerme" y "se pausa") |
| Google Skills | 1 | Qué es, qué tipos de contenido tiene y cómo funciona un laboratorio |
| De Qwiklabs a Google Skills | 1 | 2012 Qwiklabs, 2016 compra de Google, 2021 Cloud Skills Boost, 2025 Google Skills |
| Ruta Introducción a Google Cloud | 1 + práctica | Actividades de `skills.google/paths/8` y primer laboratorio en clase |

## Criterio de redacción

Nivel principiante: cada término (build, egress, vCPU-segundo, skill badge) se explica en la misma diapositiva donde aparece, con un ejemplo o una comparación cotidiana. Las cifras de los planes gratuitos son solo ejemplos: cambian con frecuencia y conviene revisarlas antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex`.
