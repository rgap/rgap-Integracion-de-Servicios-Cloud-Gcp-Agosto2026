# Sesión 21 — De una idea a una webapp

Presentación de **20 diapositivas** para una clase de 80 minutos, con la estructura docente de la Sesión 20: revisión de laboratorios, logro, saberes previos, utilidad, dos partes de teoría, práctica, cierre y referencias.

La sesión presenta lo básico de una webapp: frontend, backend, base de datos, archivos, secretos y seguridad. Conecta cada bloque con los laboratorios que ya debieron terminarse: buckets y Cloud Shell (Lab 01), LAMP (Lab 02), VPC y conectividad privada (Labs 03 y 04), VMs (Lab 05) y el servidor de Minecraft con disco, firewall, copias y scripts (Lab 06).

- [Diapositivas PDF](slides/build/S21.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Respuestas para el docente](respuestas.md)

## Distribución sugerida

| Bloque | Diapositivas | Minutos |
| --- | --- | ---: |
| Inicio y repaso | 1–7 | 12 |
| Parte 1: piezas de una webapp | 8–13 | 25 |
| Parte 2: decisiones de arquitectura | 14–17 | 18 |
| Práctica y cierre | 18–20 | 25 |

## Compilar

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
cp build/slides.pdf build/S21.pdf
```
