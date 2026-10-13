# Sesión 19 — Ruta Associate Cloud Engineer: redes VPC, Acceso privado a Google y Cloud NAT

Presentación de **45 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion18](../Sesion18/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. Esta sesión tiene **dos partes**, y cada una termina con su lab de Google Skills.

El criterio fue **lo más básico e intuitivo posible**: cada diapositiva tiene una idea, una comparación cotidiana y poco texto.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Aplicativo: redes VPC, Acceso privado a Google y Cloud NAT](apps/redes/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## Qué parte del curso cubre

Curso **Infraestructura esencial de Google Cloud: conceptos básicos** (`skills.google/paths/11/course_templates/50`), módulo *Redes virtuales*:

| Parte | Tema | En la presentación |
| --- | --- | --- |
| 1. Teoría | Configuración de redes VPC | La jerarquía de Google Cloud; regiones y zonas, en corto y ligadas a la jerarquía; red local, subred y gateway; Google Cloud VPC, tipos de red, IP interna y externa, firewall |
| **Lab 1** | *Crea y configura redes de VPC* | El lab, tarea por tarea |
| 2. Teoría | Acceso privado a Google y Cloud NAT | Solo la introducción: el problema de una VM sin IP externa y las dos soluciones |
| **Lab 2** | *Implementa el Acceso privado a Google y Cloud NAT* | El lab, tarea por tarea, y una tabla de antes y después |

La teoría de redes VPC y el lab 1 vienen de la Sesion18, donde eran la «Parte 2». Aquí se les antepone lo que faltaba para un principiante: la jerarquía, la red local, la subred y el gateway.

### El hilo de la parte 1

Va de lo conocido a lo nuevo, en este orden:

1. **Jerarquía** (diapositiva 9): organización, carpeta, proyecto, recurso. Responde «¿de quién es?».
2. **Regiones y zonas** (10): global, regional y zonal, con un ejemplo de hoy para cada uno. Responde «¿dónde está?».
3. **Red local** (11) → **subred** (13) → **gateway** (14): lo que ya existe en una oficina.
4. **Google Cloud VPC** (15): la misma idea sin cables, en una tabla *en la oficina / en Google Cloud*. Ahí se dice que el gateway entre subredes lo pone Google.

Las comparaciones se mantienen a lo largo de la parte: el **edificio** es la red, el **piso** es la subred y la **puerta del piso** es el gateway.

### Lo que se dejó fuera a propósito

Para mantener el nivel introductorio no se explican: las políticas de IAM y de la organización más allá de «lo que se decide arriba, baja», el detalle de los rangos CIDR, las rutas, los precios de red, los nombres DNS internos, IPv6, la prioridad de las reglas de firewall, ni cómo funciona Cloud NAT por dentro (puertos, Cloud Router). Del Cloud Router solo se dice que es la pieza sobre la que trabaja Cloud NAT.

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 8 | Revisión de la Sesión 18, logro, saberes previos, utilidad y plan |
| Parte 1: configuración de redes VPC | 8–20 | 22 | Jerarquía, regiones y zonas, red local, palabras de redes, subred, gateway, VPC, proyecto/red/subred, tipos de red, misma red u otra, IP y firewall |
| Lab 1, paso a paso | 21–28 | 10 | Mapa, dibujo final y las cuatro tareas |
| Parte 2: Acceso privado a Google y Cloud NAT | 29–33 | 10 | La VM sin IP externa, las dos soluciones y cuál usar |
| Lab 2, paso a paso | 34–40 | 10 | Mapa, las tareas, la tabla de antes y después y errores frecuentes de los dos labs |
| Práctica | 41–42 | 14 | Aplicativo e inicio del lab 1 |
| Cierre | 43–45 | 6 | Preguntas para comprobar y referencias |

Los dos labs reales **no caben** en la clase: el lab 1 se inicia en clase y el lab 2 queda de tarea.

## El aplicativo

`apps/redes/index.html` es una sola página, sin dependencias, que se abre con doble clic:

1. **Repaso:** cinco preguntas de verdadero o falso sobre la Sesión 18.
2. **¿Dónde vive?:** seis preguntas sobre la jerarquía y sobre qué es global, regional o zonal.
3. **Laboratorio de ping:** las tres redes y las cuatro VMs del lab 1. Se elige origen, destino e IP interna o externa, se adivina el resultado y se comprueba. Cada red tiene una casilla para quitar la regla de firewall que deja entrar el ping.
4. **VM sin IP externa:** la máquina del lab 2 con dos interruptores (Acceso privado a Google y Cloud NAT) y tres pruebas: traer un archivo del bucket, `sudo apt-get update` y un intento de entrada desde Internet. Se adivina y se comprueba.
5. **¿A qué se parece?:** cada pieza de hoy con su comparación.

## Los dibujos

No hay capturas: la jerarquía, la red local, las subredes, el gateway, las redes del lab 1 y los diagramas de Acceso privado y Cloud NAT están hechos con TikZ y se editan en `slides.tex`.

## Datos que cambian

Los pasos de los labs, los nombres de los botones, la zona y las regiones que asigna cada lab **cambian con el tiempo**. Los pasos del lab 2 se tomaron de `skills.google/catalog_lab/2526` en octubre de 2026 (la versión del curso, que entra a la VM con IAP; existe otra versión suelta, GSP459, que usa un host de bastión). El tipo de máquina de `vm-internal` varía entre versiones del lab, por eso la diapositiva no lo fija. Conviene revisar los pasos antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
