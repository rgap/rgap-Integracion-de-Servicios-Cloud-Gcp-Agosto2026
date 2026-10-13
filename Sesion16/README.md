# Sesión 16 — Ruta Associate Cloud Engineer: Infraestructura esencial de Google Cloud

Presentación de **32 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion15](../Sesion15/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. El tono es **intuitivo e introductorio**: cada concepto va con una comparación cotidiana y pocos comandos.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas de todas las preguntas](respuestas.md)

## La ruta que seguimos

Ruta **Certificación de Associate Cloud Engineer** en Google Skills (`skills.google/paths/11`), en orden:

| # | Actividad | En esta sesión |
| --- | --- | --- |
| 1 | Recorrido por los labs prácticos de Google Cloud (*A Tour of Google Cloud Hands-on Labs*, GSP282) | Rápido: está desactualizado (capturas de una consola anterior, nombres Qwiklabs / Cloud Skills Boost) |
| 2 | Crea una guía de estudio para el examen ACE (*Preparing for Your Associate Cloud Engineer Journey*) | **Se salta**: sus preguntas de diagnóstico suponen que ya estudiaste, no tiene labs y lo esencial ya se vio en la Sesión 15. Se retoma al final de la ruta |
| 3 | Infraestructura esencial de Google Cloud: conceptos básicos (*Essential Google Cloud Infrastructure: Foundation*) | **Lo principal** |

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–5 | 8 | Revisión de la Sesión 15, logro, saberes previos, utilidad |
| La ruta ACE | 6–8 | 4 | Las actividades de la ruta y el plan de hoy |
| Recorrido por los labs | 9–11 | 7 | Qué enseña, qué está desactualizado y qué sigue valiendo |
| Guía de estudio ACE | 12–13 | 3 | Qué es, por qué la saltamos y cuándo volver |
| Infraestructura esencial | 14–27 | 35 | Mapa del curso; módulo 1 (consola, Cloud Shell, `gcloud`, API, proyecto, Marketplace); módulo 2 (VPC, subredes, IPs, firewall, la casilla *Permitir tráfico HTTP*, Cloud NAT y costos de red); módulo 3 (tipos de máquina, encendida/detenida/borrada, formas de pago, discos, imágenes e instantáneas) |
| Práctica | 28–29 | 15 | Cálculo de subredes, reglas de firewall e inicio del primer lab del curso (*Explore the Google Cloud Console and Cloud Shell*) |
| Cierre | 30–32 | 8 | Preguntas para comprobar y referencias |

## Criterio de redacción

Nivel principiante: cada término (VPC, subred, IP interna/externa, firewall, VM Spot, instantánea) se explica en la misma diapositiva con una comparación cotidiana (condominio, anexo de oficina, portero con lista, lista de espera, molde de torta). El número de actividades de la ruta, sus nombres, las duraciones de los labs y los porcentajes de descuento son **ejemplos que cambian**: conviene revisarlos en `skills.google/paths/11` antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
