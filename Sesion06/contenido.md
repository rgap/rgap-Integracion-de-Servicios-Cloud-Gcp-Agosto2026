# Sesión 06 — Permisos, servicios, automatización con IA y acceso remoto en Linux

## Requisito previo

Cada estudiante debe contar con Ubuntu Desktop operativo dentro de la máquina virtual, acceso a una cuenta con `sudo`, conectividad de red y los materiales en `~/Escritorio/curso_cloud/sesion06/demo`. Para el ejercicio remoto se requiere un segundo terminal que pueda alcanzar la IP de la MV.

## Logro

Al finalizar, el estudiante administra permisos de archivos, diferencia servicios activos de servicios habilitados al arranque, supervisa servicios mediante un script creado con apoyo de IA, relaciona una aplicación Node con MySQL mediante `systemd` y reconoce SSH como mecanismo de administración remota.

## Secuencia diapositiva por diapositiva

1. Portada de la Sesión 06.
2. Revisión del propósito de `systemctl`, de la diferencia entre `start` y `enable`, y verificación de la instalación de Warp y Antigravity CLI.
3. Logro de la sesión mediante acciones observables.
4. Saberes previos sobre servidores creados con Node.js y la práctica de acceso desde la red local usando `curl`.
5. Utilidad de la sesión para una MV y un servidor cloud.
6. Separador: ayuda con IA en la terminal.
7. Instalación de Visual Studio Code en Ubuntu.
8. Uso e instalación de Warp en Ubuntu.
9. Uso e instalación de Antigravity CLI mediante `agy`.
10. Práctica de red: el estudiante averigua los comandos que entregan `VM_IP`, `ROUTER_IP`, `PUBLIC_IP`, `DEST_NAME` y `DEST_IP`.
11. Obtención de `HOST_IP`, verificación del modo `Bridged` y observación del tráfico al abrir Google en Firefox para deducir `PROTOCOL` y `PORT`.
12. Ficha de placeholders y prompt para visualizar la secuencia del tráfico.
13. Separador: gestión de permisos.
14. Propietario, grupo y otros; permisos `r`, `w` y `x`.
15. Lectura guiada del resultado de `ls -l`.
16. Script Python con *shebang* y primer intento sin permiso `x`.
17. Demostración `Permission denied` → `chmod u+x` → ejecución correcta.
18. Forma simbólica, forma numérica y advertencia sobre `777`.
19. Práctica 1: asignar ejecución a `saludo.py`.
20. Separador: servicios al iniciar Ubuntu.
21. Relación entre servicio, archivo de unidad, `systemd` y `systemctl`.
22. Listado con `sudo systemctl list-unit-files --type service --all`.
23. Lectura de `enabled`, `disabled`, `static`, `masked` y `PRESET`.
24. Diferencia entre servicios activos y habilitados al arranque.
25. Solicitud segura a `agy` para crear un monitor de solo lectura.
26. Ejecución y lectura de `monitor_servicios.py`.
27. Separador: Node y MySQL como servicios.
28. Responsabilidades de Node y MySQL; instalación de paquetes.
29. API Node que comprueba disponibilidad de MySQL en el puerto `3306`.
30. Unidad `mi-api.service` con dependencia y orden respecto a MySQL.
31. Instalación de la unidad y uso de `enable --now`.
32. Diagnóstico mediante estado, registro, puertos y dependencias.
33. Separador: introducción a SSH.
34. Definición, usos, componentes y puerto habitual de SSH.
35. Instalación de OpenSSH Server y primera conexión remota.
36. Autenticación mediante claves SSH y administración de la MV.
37. Práctica 2 integrada: permisos, servicios, monitor y SSH.
38. Cierre.
39. Referencias.

## Práctica de descubrimiento del tráfico

Antes de trabajar permisos, el estudiante abre `google.com` en Firefox y reúne evidencia para describir el recorrido de red. Las diapositivas no entregan los comandos: cada estudiante debe averiguarlos, apoyándose en Warp o en `agy` si lo necesita, y anotar el que usó para cada dato.

- `VM_IP`: IPv4 activa de la VM.
- `ROUTER_IP`: puerta de enlace por la que sale el tráfico de la VM.
- `PUBLIC_IP`: dirección con la que Internet ve la salida.
- `DEST_IP`: una IPv4 de Google; `DEST_NAME` es `Google`.
- En la Mac, `HOST_IP`: IPv4 de la interfaz Wi-Fi, que primero debe identificarse.
- `PROTOCOL` y `PORT`: se deducen capturando el tráfico hacia `DEST_IP` mientras Firefox abre el sitio (resultado esperado: HTTPS y 443).
- `MODE=Bridged` se confirma en la configuración de red del hipervisor; no existe un comando dentro de Ubuntu que lo demuestre de forma fiable.
- En modo puente, `HOST_IP` se registra como contexto, pero la Mac no se representa como un salto entre la VM y el router.

Cada estudiante entrega la ficha completa, el comando o evidencia usado para cada dato y el prompt que solicita visualizar DNS, salida por el router, traducción a la IP pública, conexión HTTPS y respuesta.

## Demostración de permisos

- `saludo.py` incluye `#!/usr/bin/env python3` para indicar el intérprete.
- Antes de los cambios, el archivo se ve así:
  ```
  rgap@ubuntu:~/Desktop$ ls -l saludo.py
  -rw-rw-r-- 1 rgap rgap 0 Aug 27 15:34 saludo.py
  ```
- `chmod u-x saludo.py` permite reproducir el error de ejecución directa.
- `./saludo.py` falla sin `x`; `python3 saludo.py` puede funcionar porque se está ejecutando el intérprete.
- `chmod u+x saludo.py` agrega únicamente el permiso necesario al propietario.
- `ls -l saludo.py` debe mostrar `-rwx` al inicio después del cambio.
- No se utiliza `chmod 777`, porque concede lectura, escritura y ejecución a todos.

## Inventario y arranque de servicios

- `systemctl list-unit-files --type service --all` muestra archivos de unidad y su estado de habilitación.
- `systemctl list-units --type=service --state=running` muestra servicios activos ahora.
- `systemctl list-unit-files --type=service --state=enabled` muestra servicios preparados para iniciar con Ubuntu.
- `systemctl is-active SERVICIO` y `systemctl is-enabled SERVICIO` responden preguntas distintas.
- Una unidad `static` puede iniciarse mediante otra unidad aunque no se habilite directamente.

## Monitor creado con apoyo de `agy`

La solicitud exige que `monitor_servicios.py`:

- consulte únicamente `systemctl is-active` y `systemctl is-enabled`;
- revise `mysql.service` y `mi-api.service`;
- muestre fecha y hora;
- use una lista de argumentos, sin `shell=True`;
- no ejecute `sudo`, no reinicie y no modifique servicios.

Después de revisar el código, se utiliza `chmod u+x monitor_servicios.py` y `./monitor_servicios.py`.

## Node y MySQL

- `mysql-server` suele proporcionar `mysql.service` en Ubuntu; otro paquete puede usar un nombre distinto.
- Node.js no crea una unidad genérica `node.service`; el laboratorio define `mi-api.service`.
- `app.js` publica una respuesta de salud en `127.0.0.1:8000` y comprueba si MySQL acepta conexiones en `127.0.0.1:3306`.
- `Requires=mysql.service` declara la dependencia y `After=mysql.service` ordena el inicio.
- `After=` no prueba que MySQL ya esté listo; la comprobación del puerto hace visible ese estado.
- La carpeta de trabajo se ubica en `/home/rgap/Escritorio/curso_cloud/sesion06/demo`; antes de instalar la unidad se deben adaptar `User=` y `WorkingDirectory=` a la cuenta de la MV.
- `sudo systemctl enable --now mysql.service mi-api.service` inicia ambos servicios y los habilita para el siguiente arranque.

## Introducción a SSH

- SSH permite ejecutar comandos remotos mediante una conexión cifrada.
- La MV instala `openssh-server` y administra el servidor como `ssh.service`.
- El cliente se conecta mediante `ssh usuario@IP` y verifica la huella en el primer acceso.
- Una clave Ed25519 se crea con `ssh-keygen -t ed25519` y su parte pública se instala con `ssh-copy-id`.
- Al habilitar SSH se abre un servicio de red; se debe revisar la red virtual y el firewall.

## Archivos de demostración

- `demo/saludo.py`: práctica de permiso de ejecución.
- `demo/monitor_servicios.py`: monitor de solo lectura.
- `demo/app.js`: API Node con comprobación del puerto de MySQL.
- `demo/mi-api.service`: unidad de `systemd` para la API.

## Fuentes técnicas

- GNU Coreutils y páginas de manual de `ls`, `chmod`, `env`, `ip`, `getent`, `curl` y `tcpdump`.
- Documentación de systemd: `systemctl`, `systemd.unit` y `systemd.service`.
- Documentación de Ubuntu Server para OpenSSH y MySQL.
- Documentación de Node.js para los módulos `http` y `net`.
- Documentación oficial de Warp para Linux.
- Documentación oficial de Visual Studio Code para Linux.
- Documentación oficial de Google Antigravity CLI.
- Material proporcionado: *Fundamentos de Linux — Programa completo* y estructura docente de la Sesión 05.
