# Sesión 04 — Monitoreo y troubleshooting en Linux

## Requisito previo

Cada estudiante debe contar con Ubuntu Desktop operativo y poder abrir una terminal. Se utilizarán los comandos de interfaces de red revisados en la sesión 03.

## Logro

Al finalizar, el estudiante monitorea CPU, memoria, disco y procesos, y aplica un proceso básico de troubleshooting para delimitar una falla de conectividad mediante evidencia.

## Secuencia

1. Monitoreo de CPU, memoria, disco, procesos, red, servicios y logs.
2. Interpretación de mediciones y relación con síntomas.
3. Troubleshooting: síntoma, alcance, hipótesis, prueba, corrección y verificación.
4. Verificación de red con `ip`, `ping`, `getent` y `curl`.

## Prácticas

1. Interpretación de evidencia con `uptime`, `free -h`, `df -h` y `ps`.
2. Diagnóstico de conectividad por capas, desde la interfaz hasta el servicio.

## Respuestas esperadas al cierre

1. **¿Qué comandos podemos utilizar para monitorear los recursos de un SO Linux?** `uptime` para carga, `free -h` para memoria, `df -h` para disco y `top` o `ps` para procesos.
2. **¿Qué entiendes por troubleshooting?** Es un proceso ordenado para observar una falla, reunir evidencia, comprobar una posible causa, corregirla y verificar el resultado.
3. **¿Cómo se diagnostica una falla de red?** Se comprueba la interfaz, la dirección IP, la ruta, el gateway, la salida por IP, la resolución DNS y finalmente el servicio.
4. **¿Cómo se valida una corrección?** Se repite la prueba que evidenció la falla y se confirma el resultado esperado.

## Fuentes técnicas

- Debian Administrator's Handbook y páginas de manual de los comandos utilizados.
- Material proporcionado: *Fundamentos de Linux — Programa completo*, utilizado como base para reorganizar monitoreo y troubleshooting.
