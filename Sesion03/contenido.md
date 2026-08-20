# Sesión 03 — Linux, terminal e interfaces de red

## Requisito previo

Cada estudiante debe contar con **Ubuntu Desktop** operativo, instalado directamente o dentro de una máquina virtual. Para una MV se sugieren 4 GB de RAM, 2 núcleos asignados, 25 GB de disco y un adaptador con salida a internet.

El laboratorio está listo cuando Ubuntu muestra el escritorio, la aplicación Terminal abre, el estudiante conoce su contraseña y la MV tiene conexión de red.

## Logro

Al finalizar, el estudiante utiliza la aplicación Terminal de Ubuntu para identificar el sistema, desplazarse entre carpetas, consultar la configuración básica de red y reutilizar instrucciones, comprobando el resultado de cada acción.

## Criterio didáctico

Cada tema sigue esta secuencia:

1. Definición de todos los términos nuevos.
2. Ejemplo o ilustración directamente relacionada.
3. Resultado completo esperado.
4. Comprobación que permite decidir si la actividad se realizó correctamente.

## Secuencia diapositiva por diapositiva

1. Relación entre anfitrión, hipervisor y máquina virtual.
2. Preparación de Ubuntu Desktop y resultado esperado del laboratorio.
3. Logro expresado mediante acciones observables.
4. Definición de sistema operativo, kernel, Linux, Unix y distribución.
5. Ilustración de las capas: hardware, kernel y aplicaciones de Ubuntu.
6. Comparación entre Unix y Linux.
7. Definición de paquete y gestor de paquetes; ejemplo de la familia Debian.
8. Representación visual de un archivo `.deb`: nombre, versión, arquitectura, metadatos, dependencias y contenido.
9. Inicio de la MV, definición del índice local y presentación de la primera tarea después de arrancar Ubuntu.
10. Ejemplo inicial en Ubuntu: definición de repositorio y `sudo`; actualización del índice con `apt` y comprobación del resultado.
11. Explicación de por qué se actualiza el índice primero; instalación de Node.js y npm en una instancia de MV preparada para una API.
12. Separación visual y definición de prompt, comando, opción y argumento.
13. Definición de Terminal y shell; ilustración del flujo entrada → interpretación → resultado, con salida de `whoami`.
14. Definición de sistema de archivos, directorio, raíz y rutas.
15. Ilustración del árbol de directorios y función de sus ramas principales.
16. Definición y ejemplo completo de `pwd`, `ls`, `mkdir`, `cd` y `cat`.
17. Definición y ejemplo de `whoami`, `hostname`, `cat /etc/os-release`, `uname -a` y redirección.
18. Práctica 1A: identificación del sistema y creación de la ruta del laboratorio.
19. Práctica 1B: creación y comprobación de `evidencia.txt`.
20. Definición de interfaz, adaptador virtual, dirección IP, prefijo, estado, loopback y router.
21. Ilustración del recorrido MV → adaptador → router → internet.
22. Ejemplos completos de una MV con una y dos interfaces.
23. Definición de ruta, puerta de enlace y DNS.
24. Definición de puerto, TCP, servicio en escucha y SSH.
25. Ejecución e interpretación completa de los cinco comandos de red.
26. Definición visual de alias y función, incluida su duración temporal.
27. Definición de variable de entorno y comparación completa entre Bash y Zsh.
28. Práctica 2: creación, ejecución y comprobación de `listar` e `info`.

Las diapositivas restantes corresponden a cierre y referencias. No se incluyen monitoreo ni troubleshooting; esos temas pertenecen a la sesión 04.

## Resultados completos de las prácticas

### Práctica 1

- `whoami` devuelve el usuario actual.
- `hostname` devuelve el nombre de la MV.
- `/etc/os-release` identifica Ubuntu y su versión.
- `~/curso-cloud/sesion03` existe y es la ruta actual.
- `evidencia.txt` contiene la salida de `uname -a`.

### Práctica 2

- `listar` produce el mismo listado que `ls -a`.
- `info` devuelve usuario, nombre del equipo y ruta actual, en ese orden.
- El alias y la función desaparecen al cerrar la terminal porque todavía no se guardan en la configuración de la shell.

## Ilustraciones incorporadas

- `linux-capas.png`: relación entre hardware, kernel y aplicaciones.
- `terminal-flujo.png`: entrada, interpretación y resultado.
- `sistema-archivos.png`: árbol de directorios.
- `mv-red.png`: recorrido de la conexión de una MV.
- `alias-funcion.png`: agrupación de instrucciones repetidas.
- `paquete-deb.png`: contenido visual de un paquete de software.

## Fuentes técnicas

- Debian Administrator's Handbook y páginas de manual de los comandos utilizados.
- Documentación del hipervisor utilizado en el laboratorio.
- Material proporcionado: *Fundamentos de Linux — Programa completo*.
