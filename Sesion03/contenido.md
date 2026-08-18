# Sesión 03 — Linux, interfaces de red y troubleshooting

## Requisito previo

Cada estudiante debe tener instalado **Ubuntu Desktop** (Ubuntu con entorno gráfico), ya sea directamente en el equipo o dentro de una máquina virtual. Para una VM se sugieren 4 GB de RAM, 2 vCPU, 25 GB de disco y un adaptador con salida a internet.

## Logro

Al finalizar, el estudiante reconoce Linux y su terminal, configura interfaces de red, monitorea recursos del sistema y aplica un proceso básico de troubleshooting sustentado en evidencia.

## Secuencia

1. Unix, Linux y distribuciones Linux.
2. Familia Debian, terminal, Bash, Zsh, rutas y comandos iniciales.
3. Interfaces de red físicas y virtuales en Linux.
4. Creación temporal de alias y funciones en la shell.
5. Verificación de red con `ip`, `ping`, `getent`, `ss` y `curl`.
6. Monitoreo de CPU, memoria, disco, procesos, red, servicios y logs.
7. Troubleshooting: síntoma, alcance, hipótesis, prueba, corrección y verificación.

## Aplicativos HTML

- `1_interfaces-virtuales.html`: compara el alcance de los modos comunes de una interfaz virtual.

## Respuestas esperadas al cierre

1. **¿Cuántas interfaces de red podemos configurar para una MV?** La cantidad depende del programa utilizado para crear la máquina virtual. Cada programa establece su propio límite. En esta sesión comenzaremos con una interfaz.
2. **¿Qué opciones tenemos para configurar una interfaz de red virtual?** Configuración automática, donde la red entrega los datos, o manual, donde se escriben la dirección IP, la puerta de enlace y el DNS.
3. **¿Qué comandos podemos utilizar para monitorear los recursos de un SO Linux?** `uptime` para carga, `free -h` para memoria, `df -h` para disco y `top` o `ps` para procesos.
4. **¿Qué entiendes por Troubleshooting?** Es un proceso ordenado para observar una falla, reunir evidencia, comprobar una posible causa, corregirla y verificar el resultado.

## Fuentes técnicas

- Documentación del hipervisor o plataforma utilizada.
- Material proporcionado: *Fundamentos de Linux — Programa completo*, utilizado como base para reorganizar la introducción.
