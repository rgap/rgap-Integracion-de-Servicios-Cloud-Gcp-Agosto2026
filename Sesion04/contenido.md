# Sesión 04 — Linux, terminal y sistema de archivos

## Requisito previo

Cada estudiante debe contar con **Ubuntu Desktop** operativo, instalado directamente o dentro de una máquina virtual. Para una MV se sugieren 4 GB de RAM, 2 núcleos asignados, 25 GB de disco y un adaptador con salida a internet.

El laboratorio está listo cuando Ubuntu muestra el escritorio, la aplicación Terminal abre, el estudiante conoce su contraseña y la MV tiene conexión de red.

## Logro

Al finalizar, el estudiante utiliza la aplicación Terminal de Ubuntu para identificar el sistema, instalar programas, desplazarse entre carpetas y guardar evidencias, comprobando el resultado de cada acción.

## Criterio didáctico

Cada tema sigue esta secuencia:

1. Definición de todos los términos nuevos.
2. Ejemplo o ilustración directamente relacionada.
3. Resultado completo esperado.
4. Comprobación que permite decidir si la actividad se realizó correctamente.

## Secuencia diapositiva por diapositiva

1. Portada de la Sesión 04.
2. Relación entre anfitrión, hipervisor y máquina virtual.
3. Preparación de Ubuntu Desktop y resultado esperado del laboratorio.
4. Logro expresado mediante acciones observables.
5. Definición de sistema operativo, kernel, Linux, Unix y distribución.
6. Ilustración de las capas: hardware, kernel y aplicaciones de Ubuntu.
7. Comparación entre Unix y Linux.
8. Definición de paquete y gestor de paquetes; ejemplo de la familia Debian.
9. Representación visual de un archivo `.deb`.
10. Inicio de la MV y definición del índice local.
11. Actualización del índice con `apt` y comprobación del resultado.
12. Instalación y comprobación de Node.js y npm.
13. Separador: ejecutando comandos.
14. Definición de Terminal y shell; flujo entrada → interpretación → resultado.
15. Diferencia entre prompt, comando, opción y argumento.
16. Definición de sistema de archivos, directorio, raíz y rutas.
17. Ilustración del árbol de directorios y función de sus ramas principales.
18. Uso de `pwd` para mostrar la ubicación actual.
19. Uso de `ls -a` para mostrar elementos ocultos.
20. Uso de `mkdir` para crear directorios.
21. Uso de `cd` para cambiar de ubicación.
22. Uso de `cat` para mostrar el contenido de un archivo.
23. Identificación del usuario, equipo, distribución y kernel.
24. Práctica 1A: identificación del sistema y creación de la ruta del laboratorio.
25. Práctica 1B: creación y comprobación de `evidencia.txt`.
26. Cierre.
27. Referencias.

## Resultados completos de las prácticas

### Práctica 1

- `whoami` devuelve el usuario actual.
- `hostname` devuelve el nombre de la MV.
- `/etc/os-release` identifica Ubuntu y su versión.
- `~/curso_cloud/sesion04` existe y es la ruta actual.
- `evidencia.txt` contiene la salida de `uname -a`.

## Ilustraciones incorporadas

- `linux-capas.png`: relación entre hardware, kernel y aplicaciones.
- `terminal-flujo.png`: entrada, interpretación y resultado.
- `sistema-archivos.png`: árbol de directorios.
- `paquete-deb.png`: contenido visual de un paquete de software.

## Fuentes técnicas

- Debian Administrator's Handbook y páginas de manual de los comandos utilizados.
- Documentación del hipervisor utilizado en el laboratorio.
- Material proporcionado: *Fundamentos de Linux — Programa completo*.
