# Sesión 22 — IAM: quién puede hacer qué y sobre qué recurso

Presentación de **20 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 21: revisión, logro, saberes previos, utilidad, dos partes de teoría, práctica, cierre y referencias.

La sesión presenta IAM con el caso de facturación de Pedidos Express: identidades (personas y cuentas de servicio), roles, asignación en el proyecto o en un recurso y el principio de mínimo privilegio. Conecta cada idea con el laboratorio **[Explora IAM](https://www.cloudskillsboost.google/focuses/19082?locale=es&parent=catalog)**: quitar el rol `Viewer` del proyecto, conceder `Storage Object Viewer` y crear una VM con una cuenta de servicio.

- [Diapositivas PDF](slides/build/S22.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Inicio y repaso | 1–7 | 12 |
| Parte 1: identidad, rol y recurso | 8–13 | 25 |
| Parte 2: cuentas de servicio | 14–17 | 18 |
| Práctica y cierre | 18–20 | 25 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S22.pdf
```
