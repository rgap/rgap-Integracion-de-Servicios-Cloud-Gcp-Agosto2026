# Sesión 19 — Ruta Associate Cloud Engineer: configuración de redes VPC

Presentación de **29 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion18](../Sesion18/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. La parte de Acceso privado a Google y Cloud NAT que estaba aquí pasó a la [Sesion20](../Sesion20/README.md).

El criterio fue **lo más básico e intuitivo posible**: cada diapositiva tiene una idea, una comparación cotidiana y poco texto. Del lab **no se detallan las tareas**: solo lo más importante, en tres diapositivas (el lab en una mirada, el resultado que importa y tres ideas para no perderse). Los pasos están en la guía del lab.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas de todas las preguntas](respuestas.md)

## Qué parte del curso cubre

Curso **Infraestructura esencial de Google Cloud: conceptos básicos** (`skills.google/paths/11/course_templates/50`), módulo *Redes virtuales*:

| Parte | Tema | En la presentación |
| --- | --- | --- |
| Teoría | Configuración de redes VPC | La jerarquía de Google Cloud; regiones y zonas, en corto y ligadas a la jerarquía; red local, subred y gateway; Google Cloud VPC, tipos de red, IP interna y externa, firewall |
| **Lab** | *Crea y configura redes de VPC* | Lo más importante: el dibujo de las tres redes, quién se puede hablar y tres ideas |

### El hilo de la teoría

Va de lo conocido a lo nuevo, en este orden:

1. **Jerarquía** (diapositiva 9): organización, carpeta, proyecto, recurso. Responde «¿de quién es?».
2. **Regiones y zonas** (10): global, regional y zonal, con un ejemplo de hoy para cada uno. Responde «¿dónde está?».
3. **Red local** (11) → **subred** (13) → **gateway** (14): lo que ya existe en una oficina.
4. **Google Cloud VPC** (15): la misma idea sin cables, en una tabla *en la oficina / en Google Cloud*. Ahí se dice que el gateway entre subredes lo pone Google.

Las comparaciones se mantienen a lo largo de la teoría: el **edificio** es la red, el **piso** es la subred y la **puerta del piso** es el gateway.

### Lo que se dejó fuera a propósito

Para mantener el nivel introductorio no se explican: las políticas de IAM y de la organización más allá de «lo que se decide arriba, baja», el detalle de los rangos CIDR, los precios de red, los nombres DNS internos, IPv6 ni la prioridad de las reglas de firewall. Las rutas se ven en la Sesion20.

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 8 | Revisión de la Sesión 18, logro, saberes previos, utilidad y plan |
| Configuración de redes VPC | 8–20 | 25 | Jerarquía, regiones y zonas, red local, palabras de redes, subred, gateway, VPC, proyecto/red/subred, tipos de red, misma red u otra, IP y firewall |
| El lab: lo más importante | 21–24 | 8 | El lab en una mirada, quién se puede hablar y tres ideas |
| Práctica | 25–26 | 32 | La pregunta del lab y el lab real |
| Cierre | 27–29 | 7 | Preguntas para comprobar y referencias |

Lo que no se termine del lab en clase queda de tarea.

## Los dibujos

No hay capturas: la jerarquía, la red local, las subredes, el gateway y las redes del lab están hechos con TikZ y se editan en `slides.tex`.

## Datos que cambian

Los pasos del lab, los nombres de los botones, la zona y las regiones que asigna **cambian con el tiempo**. Conviene revisar el lab antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
