# Sesión 18 — Ruta Associate Cloud Engineer: Marketplace y pila LAMP

Presentación de **24 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion17](../Sesion17/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. La parte de redes VPC que estaba aquí pasó a la [Sesion19](../Sesion19/README.md).

El criterio fue **lo más introductorio posible, aunque no entren todos los temas**: cada diapositiva tiene una idea, una comparación cotidiana y poco texto.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Aplicativo: Marketplace y pila LAMP](apps/marketplace/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## Qué parte del curso cubre

Curso **Infraestructura esencial de Google Cloud: conceptos básicos** (`skills.google/paths/11/course_templates/50`), en el orden de la plataforma:

| Parte | Elementos del curso | En la presentación |
| --- | --- | --- |
| Teoría | *Introducción al lab: Vista previa de la infraestructura* | Jenkins explicado desde cero y qué es Marketplace |
| **Lab** | *Implementa una pila LAMP con Google Cloud Marketplace* | Qué es LAMP y el lab, tarea por tarea |

### Jenkins en el video, LAMP en el lab

El video de introducción es antiguo y muestra la instalación de **Jenkins** (certificado por Bitnami, con Deployment Manager). El lab se actualizó y hoy instala una **pila LAMP** de Google Click to Deploy. La diapositiva 9 lo aclara para que nadie se confunda; la idea que enseñan ambos es la misma: una solución que a mano toma horas, con Marketplace toma minutos.

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 8 | Revisión de la Sesión 17, logro, saberes previos, utilidad y plan |
| Soluciones listas | 8–13 | 15 | La aclaración Jenkins/LAMP, qué es Jenkins, a mano o con Marketplace, la tienda |
| El lab, paso a paso | 14–19 | 15 | Qué es LAMP, cómo viaja una visita, las tareas y qué hizo Marketplace |
| Práctica | 20–21 | 35 | Aplicativo y el lab real completo |
| Cierre | 22–24 | 7 | Preguntas para comprobar y referencias |

Con un solo lab, el lab real **sí cabe** en la clase; lo que no se termine queda de tarea.

## El aplicativo

`apps/marketplace/index.html` es una sola página, sin dependencias, que se abre con doble clic:

1. **Repaso:** cinco preguntas de verdadero o falso sobre la Sesión 17.
2. **Simulador de Marketplace:** los pasos del lab (buscar LAMP, elegir la pila de Google Click to Deploy entre tres, aceptar los términos, configurar zona, serie y tipo, implementar y abrir la URL del sitio). A la derecha se marca lo que Marketplace va haciendo por ti. Reproduce los dos tropiezos típicos: elegir otra pila y abrir el sitio antes de tiempo.
3. **¿A qué se parece?:** cada pieza de hoy con su comparación.

El laboratorio de ping que estaba aquí ahora está en el aplicativo de la Sesion19.

## Los dibujos

No hay capturas: el recorrido de Jenkins, la pila LAMP y lo que Marketplace crea por ti están hechos con TikZ y se editan en `slides.tex`.

## Datos que cambian

Los pasos de los labs, los nombres de los botones, la zona que asigna el lab y los precios **cambian con el tiempo**. Los pasos de esta sesión se tomaron de la plataforma en octubre de 2026; conviene revisarlos antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
