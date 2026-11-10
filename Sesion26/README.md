# Sesión 26 — Balanceo de carga, CDN y contenedores

Presentación de **19 diapositivas** de teoría, con la estructura docente de la Sesión 25: revisión, logro, saberes previos, utilidad, tres partes de teoría, cierre y referencias. Es una **introducción**: una idea por diapositiva, sin detalles de configuración. No tiene práctica.

La revisión retoma la Sesión 25 (supervisión y alta disponibilidad) y termina con tres servidores `web-1`, `web-2` y `web-3`: de ahí salen las tres preguntas del día. La teoría tiene tres partes cortas:

1. **Balanceo de carga:** un solo servidor forma una cola (6 reportes de 5 s: el último espera 30 s); el balanceador recibe a todos en una sola dirección y reparte; *round robin* (30 s → 10 s con tres servidores); qué pasa si un servidor se cae.
2. **CDN:** copias de los archivos cerca del cliente (primera vez y siguientes veces) y qué va en la CDN y qué no. Cloud CDN en una línea.
3. **Contenedores:** el problema de preparar cada servidor (`web-1`, `web-2` y `web-3` con la misma versión de todo) e imagen y contenedor.

El `Dockerfile`, Docker Compose y Kubernetes siguen en la [Sesión 27](../Sesion27/), que empieza otra vez por imagen y contenedor.

- [Diapositivas PDF](slides/build/S26.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Revisión | 1–3 | 5 |
| Logro, saberes previos y utilidad | 4–6 | 4 |
| Parte 1: balanceo de carga | 7–11 | 10 |
| Parte 2: CDN | 12–14 | 6 |
| Parte 3: contenedores | 15–17 | 5 |
| Cierre | 18–19 | 5 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S26.pdf
```
