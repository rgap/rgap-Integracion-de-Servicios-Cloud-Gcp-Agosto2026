# Sesión 20 — Ruta Associate Cloud Engineer: rutas en VPC, Acceso privado a Google y Cloud NAT

Presentación de **25 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion19](../Sesion19/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. La teoría va en **dos partes** y termina con un lab de Google Skills.

El criterio fue **lo más básico e intuitivo posible**: cada diapositiva tiene una idea, una comparación cotidiana y poco texto. Del lab **no se detallan las tareas**: solo lo más importante, en tres diapositivas (el lab en una mirada, la tabla de antes y después y tres ideas para no perderse). Los pasos están en la guía del lab.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas de todas las preguntas](respuestas.md)

## Qué parte del curso cubre

Curso **Infraestructura esencial de Google Cloud: conceptos básicos** (`skills.google/paths/11/course_templates/50`), módulo *Redes virtuales*:

| Parte | Tema | En la presentación |
| --- | --- | --- |
| 1. Teoría | Las redes VPC, en corto | Qué es una red VPC (diapositiva 9), las redes VPC en cinco ideas (10) y qué es una ruta (11) |
| 2. Teoría | Acceso privado a Google y Cloud NAT | El problema de una VM sin IP externa (13), Acceso privado a Google (14), Cloud NAT (15) y cuál usar (16) |
| **Lab** | *Implementa el Acceso privado a Google y Cloud NAT* | Lo más importante: los tres momentos de la VM, la tabla de antes y después y tres ideas |

La parte 2 y el lab vienen de la Sesion19, donde eran su «Parte 2». La parte 1 es un repaso corto de la Sesion19 con una idea nueva: la **ruta**.

### El hilo de la sesión

1. **Repaso de VPC:** la red es mundial, la subred es de una región, misma red se hablan, dos direcciones, el firewall decide.
2. **Ruta:** el letrero de la carretera. Toda red trae una por cada subred y una hacia Internet (`0.0.0.0/0`). La diapositiva cierra con «la ruta no basta»: para salir a Internet la máquina necesita una IP externa… o lo que viene.
3. **Parte 2:** qué pasa con una máquina que **no** tiene IP externa, y los dos servicios que le abren un camino de salida sin abrirle uno de entrada.

### Lo que se dejó fuera a propósito

Para mantener el nivel introductorio no se explican: las rutas personalizadas, su prioridad y los tipos de siguiente salto; cómo funciona Cloud NAT por dentro (puertos, Cloud Router); Private Service Connect ni los nombres de dominio de las API de Google. Tampoco los comandos del lab: están en su guía.

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 8 | Revisión de la Sesión 19, logro, saberes previos, utilidad y plan |
| Parte 1: las redes VPC, en corto | 8–11 | 12 | Qué es una red VPC, cinco ideas y qué es una ruta |
| Parte 2: Acceso privado a Google y Cloud NAT | 12–16 | 15 | La VM sin IP externa, las dos soluciones y cuál usar |
| El lab: lo más importante | 17–20 | 8 | El lab en una mirada, la tabla de antes y después y tres ideas |
| Práctica | 21–22 | 30 | El lab real, anotando cada prueba |
| Cierre | 23–25 | 7 | Preguntas para comprobar y referencias |

Lo que no se termine del lab en clase queda de tarea.

## Los dibujos

No hay capturas: el dibujo de proyecto, red y subred y los diagramas de Acceso privado, Cloud NAT y los tres momentos del lab están hechos con TikZ y se editan en `slides.tex`.

## Datos que cambian

Los pasos del lab, los nombres de los botones, la zona y la región que asigna **cambian con el tiempo**. Lo que se cuenta del lab se tomó de `skills.google/catalog_lab/2526` en octubre de 2026 (la versión del curso, que entra a la VM con IAP; existe otra versión suelta, GSP459, que usa un host de bastión). Conviene revisar el lab antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
