# Sesión 18 — Ruta Associate Cloud Engineer: Marketplace, pila LAMP y redes VPC

Presentación de **45 diapositivas** para una clase de **80 minutos**, nivel principiante, con la estructura docente de la [Sesion17](../Sesion17/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias. La diferencia es que esta sesión tiene **dos labs**, así que la teoría va en dos partes, cada una seguida de su lab.

El criterio fue **lo más introductorio posible, aunque no entren todos los temas**: cada diapositiva tiene una idea, una comparación cotidiana y poco texto.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Aplicativo: Marketplace y redes VPC](apps/redes/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## Qué parte del curso cubre

Curso **Infraestructura esencial de Google Cloud: conceptos básicos** (`skills.google/paths/11/course_templates/50`), en el orden de la plataforma:

| Parte | Elementos del curso | En la presentación |
| --- | --- | --- |
| 1. Teoría | *Introducción al lab: Vista previa de la infraestructura* | Jenkins explicado desde cero y qué es Marketplace |
| **Lab 1** | *Implementa una pila LAMP con Google Cloud Marketplace* | Qué es LAMP y el lab, tarea por tarea |
| 2. Teoría | Módulo *Redes virtuales*: *Descripción general del módulo*, *Nube privada virtual*, *Proyectos, redes y subredes*, *Demostración: Expande una subred*, *Direcciones IP*, *Demostración: IP interna y externa*, *Cómo asignar direcciones IP*, *Rutas y reglas de firewall*, *Precios*, *Introducción al lab: Herramientas de redes de VPC* | Solo las ideas base de cada video |
| **Lab 2** | *Crea y configura redes de VPC* | El lab, tarea por tarea |

### Jenkins en el video, LAMP en el lab

El video de introducción es antiguo y muestra la instalación de **Jenkins** (certificado por Bitnami, con Deployment Manager). El lab se actualizó y hoy instala una **pila LAMP** de Google Click to Deploy. La diapositiva 9 lo aclara para que nadie se confunda; la idea que enseñan ambos es la misma: una solución que a mano toma horas, con Marketplace toma minutos.

### Lo que se dejó fuera a propósito

Para mantener el nivel introductorio no se explican: los nombres DNS internos y Cloud DNS, los rangos de alias de IP, IPv6, las reglas finas de los rangos CIDR (RFC 1918, superposición), la prioridad y el estado de las reglas de firewall, las tablas de enrutamiento por instancia, ni la tabla completa de precios. Tampoco el documento *Direcciones IP para dominios predeterminados*. Todo eso está en los videos del curso para quien quiera profundizar.

## Tiempos (80 min)

| Bloque | Diapositivas | Minutos | Contenido |
| --- | --- | --- | --- |
| Inicio | 1–7 | 8 | Revisión de la Sesión 17, logro, saberes previos, utilidad y plan |
| Parte 1: soluciones listas | 8–13 | 10 | La aclaración Jenkins/LAMP, qué es Jenkins, a mano o con Marketplace, la tienda |
| Lab 1, paso a paso | 14–19 | 10 | Qué es LAMP, cómo viaja una visita, las tareas y qué hizo Marketplace |
| Parte 2: redes virtuales | 20–31 | 22 | Palabras de redes, la red de Google, VPC, proyecto/red/subred, tipos de red, misma red u otra, rangos, IP, rutas, firewall y precios |
| Lab 2, paso a paso | 32–40 | 12 | Mapa, dibujo final, las cuatro tareas y errores frecuentes de los dos labs |
| Práctica | 41–42 | 12 | Aplicativo e inicio del lab 1 |
| Cierre | 43–45 | 6 | Preguntas para comprobar y referencias |

Los dos labs reales **no caben** en la clase: el lab 1 se inicia en clase y el lab 2 queda de tarea.

## La palabra «objeto»

Aparece por primera vez en la diapositiva 23 (*¿Qué es una VPC?*), donde el curso describe la VPC como «un conjunto de objetos de red». Ahí mismo va la definición: **objeto = una “cosa” identificable dentro del sistema, con propiedades y configuración propias.** En la revisión de la sesión anterior se evitó la palabra para que esa sea de verdad la primera vez.

## El aplicativo

`apps/redes/index.html` es una sola página, sin dependencias, que se abre con doble clic:

1. **Repaso:** cinco preguntas de verdadero o falso sobre la Sesión 17.
2. **Simulador de Marketplace:** los pasos del lab 1 (buscar LAMP, elegir la pila de Google Click to Deploy entre tres, aceptar los términos, configurar zona, serie y tipo, implementar y abrir la URL del sitio). A la derecha se marca lo que Marketplace va haciendo por ti. Reproduce los dos tropiezos típicos: elegir otra pila y abrir el sitio antes de tiempo.
3. **Laboratorio de ping:** las tres redes y las cuatro VMs del lab 2. Se elige origen, destino e IP interna o externa, se adivina el resultado y se comprueba. Cada red tiene una casilla para quitar la regla de firewall que deja entrar el ping.
4. **¿A qué se parece?:** cada pieza de hoy con su comparación.

## La imagen

La única captura es el mapa de regiones del curso, que ya estaba en `Sesion17/slides/assets/gc-mapa-regiones.png`; `header.tex` la busca ahí. Los demás dibujos (el recorrido de Jenkins, la pila LAMP, las redes del lab 2) están hechos con TikZ y se editan en `slides.tex`.

## Datos que cambian

Los pasos de los labs, los nombres de los botones, la zona y las regiones que asigna cada lab, y los precios **cambian con el tiempo**. Los pasos de esta sesión se tomaron de la plataforma en octubre de 2026; conviene revisarlos antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
