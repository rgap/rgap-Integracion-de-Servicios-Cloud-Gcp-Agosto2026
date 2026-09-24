# Sesión 14 — WSL, sitios estáticos, IAM y servicios de Google Cloud

Presentación de **32 diapositivas**, nivel principiante, con la estructura docente de la [Sesion13](../Sesion13/slides/slides.tex): revisión de la sesión anterior, logro, saberes previos, utilidad, teoría con separadores de tema, práctica, cierre y referencias.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Landing para desplegar](apps/landing/index.html)
- [Respuestas de todas las preguntas](respuestas.md)

## Orden de la teoría

| Bloque | Diapositivas | Contenido |
| --- | --- | --- |
| WSL | 2 | Qué es, WSL 1 y WSL 2, `wsl --install`, usos realistas más allá de practicar Linux |
| Virtualización anidada | 2 | Una VM dentro de otra, VT-x/AMD-V, cuándo se usa (WSL 2 o Docker dentro de una VM) y Compute Engine |
| Sitios estáticos | 6 + práctica + 1 | Qué es un sitio estático, la landing Estampa sin Python, GitHub Pages, Vercel, comparación y Figma Education (Figma Make) para probar Supabase |
| Google Cloud IAM | 3 | Quién, qué rol, sobre qué recurso; roles básicos, predefinidos y personalizados; otorgar acceso en la consola |
| Habilitar servicios | 2 | Por qué las APIs vienen apagadas, consola y `gcloud services enable` |
| Google Skills: Crea una máquina virtual | 1 + práctica | Laboratorio `skills.google/focuses/3563`: VM desde la consola, NGINX y VM con `gcloud` |

## La landing

`apps/landing` es la landing "en construcción" de **Estampa** de la [Práctica Calificada 1](../Sesion10/Practica%20Calificada%201/ecommerce_webapp) convertida en sitio estático: sin `server.py`, solo `index.html`, `styles.css` y `script.js`.

| En la Sesión 10 | En la Sesión 14 |
| --- | --- |
| `server.py` reemplazaba `{{WHATSAPP_LINK}}` y `{{WHATSAPP_NUMBER}}` | `script.js` arma el enlace en el navegador; el número se cambia al inicio del archivo |
| `static/style.css` + estilos en `<style>` | Un solo `styles.css` |
| Rutas absolutas (`/style.css`, `href="/"`) | Rutas relativas (`styles.css`, `href="./"`) para que funcione en `usuario.github.io/repositorio/` |

Se abre con doble clic en `index.html` o se publica tal cual en GitHub Pages y en Vercel (Framework Preset: **Other**).

## Criterio de redacción

Nivel principiante: cada término (kernel, principal, rol, API) se explica en la misma diapositiva donde aparece, con una comparación cotidiana. Los límites de los planes gratuitos son solo ejemplos: cambian con frecuencia y conviene revisarlos antes de la clase.

## Compilar las diapositivas

```bash
cd slides
latexmk -xelatex -interaction=nonstopmode -output-directory=build slides.tex
```

El preámbulo reutiliza sin cambios la identidad visual UTP a través de `Sesion09/slides/header.tex` y agrega `listings` con el estilo de la Sesión 11.
