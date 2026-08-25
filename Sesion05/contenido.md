# Sesión 05 — Interfaces de red, servicios, alias y herramientas de IA en Linux

## Requisito previo

Cada estudiante debe contar con Ubuntu Desktop operativo dentro de la máquina virtual, poder abrir la aplicación Terminal y disponer de conectividad mediante el adaptador virtual en modo puente utilizado en el laboratorio.

## Logro

Al finalizar, el estudiante interpreta las interfaces y direcciones mostradas por `ip a`, relaciona una IP con el puerto de un servicio, controla servicios con `systemctl`, conserva atajos mediante `.bashrc` y reconoce Warp y Antigravity CLI como herramientas de ayuda en Ubuntu.

## Secuencia diapositiva por diapositiva

1. Portada de la Sesión 05.
2. Revisión de la sesión anterior mediante comandos básicos de Ubuntu.
3. Logro de la sesión expresado mediante acciones observables.
4. Saberes previos sobre IP, servicios, escucha y comandos repetidos.
5. Utilidad de la sesión para el laboratorio y el trabajo posterior.
6. Separador: interfaces de red.
7. Definición de interfaz de red y ejemplo con `enp0s1`.
8. Direcciones de `lo` y `enp0s1` adaptadas a la MV del laboratorio.
9. Ejemplo completo de un servidor HTTP mínimo con Node.js.
10. Ejecución y acceso local o por red según la dirección de escucha.
11. Recorrido entre la MV, el adaptador virtual y la red externa.
12. Lectura guiada del resultado de `ip a`.
13. Diferencias entre `lo` y `enp0s1`.
14. Definición de ruta, puerta de enlace y DNS.
15. Recorrido de la MV hacia internet mediante el adaptador en modo puente y el router local.
16. Separador: servicios en Linux.
17. Concepto de servicio y función de `systemd` y `systemctl`.
18. Estado y acciones disponibles para `apache2.service` en Ubuntu.
19. Separador: alias y funciones.
20. Diferencia entre alias y función.
21. Comparación entre Bash y Zsh mediante `$SHELL`.
22. Uso de `xdg-open .` para abrir el directorio actual.
23. Práctica 2 integrada: controlar Apache, volver al servidor Node y crear un alias y una función.
24. Uso de `.bashrc` para conservar alias y funciones.
25. Práctica 3: persistencia de los atajos en `.bashrc`.
26. Separador: ayuda con IA en la terminal.
27. Uso e instalación de Warp en Ubuntu mediante un paquete `.deb`.
28. Uso e instalación de Antigravity CLI mediante el comando `agy`.
29. Cierre.
30. Referencias.

## Comprobación sencilla de IP y puerto

- `ip -br addr` muestra `127.0.0.1/8` en `lo` y `192.168.100.158/24` en `enp0s1`.
- `server.js` crea un servidor con el módulo nativo `http` de Node.js, escucha en `0.0.0.0:8000` y responde `Hola desde Ubuntu`.
- `node server.js` inicia el servidor sin instalar paquetes adicionales.
- Dentro de la MV se puede probar `http://127.0.0.1:8000`.
- Mediante la interfaz de red se utiliza `http://192.168.100.158:8000`.
- Si funciona con `localhost` pero no con la IP, se revisan primero la dirección de escucha y el firewall.

## Control de servicios en la MV

- En Ubuntu, Apache se administra como `apache2.service`; `httpd.service` corresponde a otras distribuciones.
- `systemctl status apache2` muestra si el servicio está activo y si arranca automáticamente.
- `start` y `stop` actúan en la sesión actual; `enable` y `disable` controlan el arranque automático.
- Después de la práctica, Apache queda detenido y deshabilitado, y el laboratorio vuelve a usar `node server.js` en el puerto `8000`.

## Resultados completos de las prácticas

### Práctica 2

- Si Apache no está instalado, se agrega con `sudo apt install apache2 -y`.
- `sudo systemctl start apache2` inicia el servidor y `sudo systemctl enable apache2` activa su arranque automático.
- La página se comprueba en `http://192.168.100.158`.
- `sudo systemctl stop apache2` lo detiene y `sudo systemctl disable apache2` elimina el arranque automático.
- `systemctl is-active apache2` y `systemctl is-enabled apache2` deben devolver `inactive` y `disabled` al finalizar.
- `node server.js` vuelve a publicar el ejemplo del laboratorio en `http://192.168.100.158:8000`.
- `echo $SHELL` permite reconocer la shell configurada.
- El alias `o='xdg-open .'` abre el directorio actual en la aplicación **Archivos**.
- La función `info() { whoami; hostname; pwd; }` devuelve usuario, equipo y ruta actual, en ese orden.
- El alias y la función creados directamente en la terminal son temporales.

### Práctica 3

- El alias y la función quedan escritos al final de `~/.bashrc`.
- `source ~/.bashrc` vuelve a leer el archivo sin cerrar la terminal.
- Al abrir una terminal nueva, `o` e `info` continúan disponibles.

## Ayuda con Warp y Antigravity

- Warp es una terminal gráfica con ayuda de IA; en Ubuntu puede seguir usando Bash.
- `dpkg --print-architecture` permite elegir el paquete `.deb` correcto de Warp: `amd64` o `arm64`.
- El paquete descargado se instala con `sudo apt install ./warp-terminal_*.deb` y se inicia con `warp-terminal`.
- Antigravity CLI se instala con el script oficial y crea el ejecutable `~/.local/bin/agy`.
- `agy` se ejecuta dentro de la carpeta del proyecto para explicar archivos, revisar código o proponer cambios.
- Toda sugerencia debe revisarse antes de permitir cambios o ejecutar comandos.

## Ilustraciones incorporadas

- `mv-red.png`: recorrido de la conexión de una máquina virtual.
- `alias-funcion.png`: diferencia entre un alias y una función.

## Fuentes técnicas

- Debian Administrator's Handbook y páginas de manual de `bash`, `ip`, `systemctl`, `systemd.service`, `xdg-open` y `nano`.
- Documentación de Node.js del módulo nativo `http` y `server.listen`.
- Documentación del hipervisor utilizada para el modo de red puente del laboratorio.
- Documentación oficial de Warp para la instalación y configuración en Linux.
- Documentación oficial de Google Antigravity CLI para la instalación, autenticación y solución de problemas.
- Material proporcionado: *Fundamentos de Linux — Programa completo*.
- Capturas de referencia proporcionadas en `Sesion05/diapos-imagenes`, simplificadas para la VM del laboratorio.
