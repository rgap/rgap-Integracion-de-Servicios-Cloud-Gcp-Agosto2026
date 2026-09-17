# Sesión 12 — Computación en la nube, modelos de servicio y despliegue de aplicaciones

Presentación de **31 diapositivas** con la estructura docente de la [Sesion09](../Sesion09/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica y referencias.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas de todas las preguntas](respuestas.md)

## Idea de la sesión

La teoría se cuenta como una sola historia: un **clipero** —alguien que corta transmisiones largas de streamers en clips cortos— resuelve el mismo trabajo cuatro veces, y cada solución tiene nombre propio.

| Etapa | Cómo trabaja | Modelo | Por qué cambia |
| --- | --- | --- | --- |
| 1 | Edita en su laptop: busca, corta, subtitula, exporta | **On-premise** | Tarda, es repetitivo, no escala y es frágil |
| 2 | Sube el video a una web que genera los clips sola | **SaaS** | No controla el criterio ni el estilo, y depende del proveedor |
| 3 | Escribe su programa y lo sube a una plataforma | **PaaS** | Necesita `ffmpeg`, GPU y más tiempo por ejecución |
| 4 | Alquila una máquina virtual con GPU y la administra | **IaaS** | Vuelve todo el trabajo de administración del servidor |

Recién después de la historia aparecen el cuadro de los cuatro modelos con ejemplos conocidos por un desarrollador y la tabla de **quién administra cada capa**.

La segunda mitad baja a la práctica: se pregunta al grupo con qué han desplegado **frontend, backend, base de datos y almacenamiento**, y luego cada pieza tiene su diapositiva con las opciones reales y su modelo.

## Orden de la teoría

1. El trabajo del clipero y la pregunta que guía la sesión.
2. Etapa 1 en la laptop, y definición de on-premise con sus problemas.
3. Qué es la computación en la nube.
4. Etapa 2 con una web, y definición de SaaS con sus problemas.
5. Etapa 3 con su propio código en una plataforma, y definición de PaaS con sus problemas.
6. Etapa 4 con una máquina virtual, y definición de IaaS con sus problemas.
7. Los cuatro modelos, sus ejemplos clásicos y la tabla de capas.
8. Frontend, backend, base de datos y almacenamiento: qué necesita cada pieza y con qué se resuelve.

## Criterio de redacción

Nivel intuitivo y sin términos usados antes de definirse. El orden exacto de las definiciones está al final de [respuestas.md](respuestas.md). Los conceptos de administración de servidores —`systemd`, `nginx` como proxy inverso, permisos— aparecen solo como el ejemplo concreto de "lo que administras tú" en IaaS.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex`.
