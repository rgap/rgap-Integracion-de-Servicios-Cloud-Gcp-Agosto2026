# Sesión 15 — Repaso y ruta Cloud Engineer de Google Cloud

Presentación de **32 diapositivas**, nivel principiante, con la estructura docente de la [Sesion14](../Sesion14/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Aplicativo de repaso y avance en la ruta](apps/ruta/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## Orden de la teoría

| Bloque | Diapositivas | Contenido |
| --- | --- | --- |
| Repaso de la Sesión 14 | 1 + 4 | WSL y virtualización anidada, sitios estáticos (GitHub Pages y Vercel), IAM, habilitar servicios y la VM con NGINX |
| Ruta Cloud Engineer | 1 + 6 | Qué es una certificación y sus niveles, qué hace un Cloud Engineer, cómo es el examen Associate Cloud Engineer, sus 4 bloques, qué parte del temario ya se vio en el curso y la ruta en Google Skills |
| Primeros conceptos de la ruta | 1 + 8 | Jerarquía de recursos, regiones y zonas, consola / Cloud Shell / `gcloud`, mapa de servicios, Compute Engine vs Cloud Run vs GKE, Cloud Storage, costos y presupuestos, plan de estudio |
| Google Skills: primeros pasos | 1 + 1 + práctica | Labs *Getting Started with Cloud Shell and gcloud* (GSP002) y *Cloud Storage: Qwik Start - Cloud Console* (GSP073) |

## El aplicativo

`apps/ruta/index.html` es una sola página, sin dependencias, que se abre con doble clic:

1. **Repaso:** las seis preguntas de verdadero o falso de la Sesión 14, con explicación.
2. **¿Qué servicio uso?:** situaciones al estilo del examen para elegir entre Compute Engine, Cloud Run, Cloud Storage, Cloud SQL, Logging o un rol de IAM.
3. **Mi avance en la ruta:** lista de lo que se debe saber hacer en cada bloque del examen; lo marcado se guarda en el navegador.

## Criterio de redacción

Nivel principiante: cada término (certificación, proyecto, región, zona, bucket) se explica en la misma diapositiva donde aparece, con una comparación cotidiana. Los datos del examen (duración, cantidad de preguntas, costo, vigencia), el crédito de la prueba gratuita, los nombres de los cursos de la ruta y los códigos de los labs son **ejemplos que cambian**: conviene revisarlos en `cloud.google.com/learn/certification/cloud-engineer` y `skills.google` antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
