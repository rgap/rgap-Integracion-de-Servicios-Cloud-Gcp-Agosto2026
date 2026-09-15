# Sesión 11 — Configuración, servicios Linux y proxy inverso

Continuación de [Sesion10](../Sesion10/slides/slides.tex). Presentación de **30 diapositivas**, con seis separadores de tema de solo título. La teoría empieza con usuarios, grupos, permisos, `chown` y `chmod`. Después presenta Python y `.env`, y sigue un mismo programa hasta observar sus peticiones detrás de NGINX. Las diapositivas priorizan ejemplos y explicaciones breves; esta guía conserva la preparación y los comandos completos.

- [Diapositivas PDF](slides/build/slides.pdf)
- [Fuente editable LaTeX](slides/slides.tex)
- [Archivos del ejemplo](demo/)

## Orden de la teoría

1. Usuarios y grupos, lectura de permisos, `chown` y `chmod`.
2. Python, variables de entorno y `.env`.
3. Servidor HTTP, procesos y sockets. Lectura de `ss -ltnp`.
4. `systemd`, `systemctl`, `journalctl` y creación de un servicio.
5. NGINX, `sites-available`, `sites-enabled` y proxy inverso.
6. Captura de tráfico con tcpdump y TShark, la herramienta de consola de Wireshark.
7. Interpretación del recorrido y diagnóstico de fallos.

Las diapositivas desarrollan los conceptos y las opciones de los comandos. Esta guía reúne las instrucciones para reproducirlos. El ejemplo usa `http.server` con fines didácticos.

## 0. Usuarios, grupos y permisos

Un **usuario** es una cuenta de Linux. Un **grupo** reúne cuentas que pueden compartir acceso. Cada archivo tiene un usuario propietario y un grupo propietario. Un usuario tiene un grupo principal y puede pertenecer a grupos adicionales.

```bash
whoami
id
groups
```

`whoami` muestra tu usuario, `id` muestra sus identificadores y grupos, y `groups` lista sus grupos. `root` es la cuenta administradora; `sudo` permite ejecutar una orden con sus privilegios si tu cuenta está autorizada.

### Lectura de permisos

`ls -l mensaje.txt` muestra los permisos, propietario y grupo del archivo. Ejemplo ilustrativo:

```text
-rw-r----- 1 alumno curso 24 sep 15 10:00 mensaje.txt
```

- El primer `-` indica archivo. Una `d` indica directorio.
- `rw-`: el propietario `alumno` puede leer y escribir.
- `r--`: los miembros del grupo `curso` pueden leer.
- `---`: los demás no tienen acceso.

`r` significa leer, `w` escribir y `x` ejecutar. En un directorio, `r` permite listar nombres, `x` atravesarlo y `w`, junto con `x`, modificar sus entradas. Linux evalúa primero si eres el propietario; si no, si perteneces al grupo del archivo; si tampoco, usa los permisos de otros. No suma las tres categorías.

### chown y chmod

Ejemplo con el usuario `alumno`, grupo `curso` y archivo `mensaje.txt` **ya existentes**. Sustituye esos nombres por los de tu laboratorio:

```bash
sudo chown alumno:curso mensaje.txt
sudo chmod 640 mensaje.txt
ls -l mensaje.txt
```

`chown` cambia el usuario y grupo propietarios. No agrega miembros a un grupo. `chmod` cambia los permisos: cada cifra corresponde a propietario, grupo y otros, en ese orden. Leer vale 4, escribir 2 y ejecutar 1; por eso `640` representa `rw-r-----`.

Más adelante, tras crear la cuenta de servicio `sesion11`, aplicaremos la misma idea con `chown root:sesion11` y `chmod 640` a `/opt/sesion11/.env`: el administrador podrá editarlo y el servicio podrá leerlo.

## 1. Python y configuración

Usa una máquina de laboratorio Ubuntu Server 24.04 con systemd. Copia el contenido de `demo/`, incluidos los archivos ocultos, a `~/sesion11` en esa máquina. Trabaja desde esa carpeta. Los siguientes pasos modifican únicamente el entorno de laboratorio donde los ejecutes.

```bash
sudo apt update
sudo apt install python3-venv curl
cd ~/sesion11
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python configuracion.py
.venv/bin/python app.py
```

En otra terminal de la misma máquina:

```bash
curl http://127.0.0.1:8000/
sudo ss -ltnp
```

Resultado esperado: `Hola desde Sesion11` y una escucha Python en `127.0.0.1:8000`. Las opciones de `ss` son escucha (`-l`), TCP (`-t`), números (`-n`) y proceso (`-p`).

El programa localiza `.env` junto a `app.py`. Las variables que ya existen en el entorno tienen prioridad. `.env.example` contiene la configuración de muestra y `.gitignore` excluye la configuración local `.env` del historial.

## 2. El administrador y sus registros

```text
systemd    = el administrador
systemctl  = el comando para hablar con ese administrador
journalctl = el comando para consultar sus logs
```

`systemd-journald` recoge el registro central. Puedes consultarlo antes de crear nuestro servicio:

```bash
sudo journalctl -b -n 20 --no-pager
sudo journalctl -u systemd-journald -b --no-pager
```

`-b` limita al arranque actual, `-n` selecciona las últimas entradas y `-u` selecciona una unidad. `--no-pager` evita abrir el visor interactivo.

## 3. Instalación como servicio

Detén el programa manual con Ctrl+C en su terminal para liberar el puerto 8000. Crea la cuenta una vez y copia los archivos:

```bash
sudo useradd --system --user-group --no-create-home \
  --shell /usr/sbin/nologin sesion11
cd ~/sesion11
sudo mkdir -p /opt/sesion11
sudo cp app.py requirements.txt .env /opt/sesion11/
sudo python3 -m venv /opt/sesion11/.venv
sudo /opt/sesion11/.venv/bin/python -m pip install \
  -r /opt/sesion11/requirements.txt
sudo chown root:sesion11 /opt/sesion11/.env
sudo chmod 640 /opt/sesion11/.env
sudo cp sesion11.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start sesion11
sudo systemctl status sesion11 --no-pager
sudo systemctl enable sesion11
```

La unidad ejecuta Python con la cuenta dedicada `sesion11`. `ExecStart` usa el intérprete del entorno virtual mediante su ruta absoluta. Python lee `/opt/sesion11/.env`; editar el archivo de `~/sesion11` ya no cambia esta copia.

`start` solicita a systemd iniciar ahora. `enable` crea los enlaces para iniciar en futuros arranques. `daemon-reload` relee las definiciones de unidades. Ninguno sustituye la prueba HTTP:

```bash
curl http://127.0.0.1:8000/
sudo ss -ltnp
sudo journalctl -u sesion11 -b -n 30 --no-pager
sudo journalctl -u sesion11 -f
```

Con el seguimiento abierto, genera otra petición en una segunda terminal. Ctrl+C termina la consulta de logs. El servicio continúa.

Después de editar `/opt/sesion11/.env` o `app.py`, ejecuta `sudo systemctl restart sesion11`. Después de editar la unidad, ejecuta `daemon-reload` y luego `restart`. Si un fallo repetido agotó los intentos, corrige la causa, ejecuta `sudo systemctl reset-failed sesion11` y vuelve a iniciarlo.

## 4. Proxy inverso con NGINX

NGINX recibirá en 80 y reenviará a Python en 8000. El sitio de laboratorio usa `server_name sesion11.local`. La prueba envía ese nombre en la cabecera `Host`, por lo que puede convivir con el sitio predeterminado.

```bash
sudo apt install nginx
ls /etc/nginx/sites-available
ls -l /etc/nginx/sites-enabled
cd ~/sesion11
sudo cp nginx-sesion11.conf /etc/nginx/sites-available/sesion11
sudo ln -s /etc/nginx/sites-available/sesion11 \
  /etc/nginx/sites-enabled/sesion11
sudo nginx -t
```

Continúa cuando `nginx -t` confirme que la configuración es válida:

```bash
sudo systemctl enable --now nginx
sudo systemctl reload nginx
curl -i -H "Host: sesion11.local" http://127.0.0.1/
sudo ss -ltnp
```

El enlace se crea una sola vez. Si ya existe, revisa su destino con `ls -l`. `sites-available` y `sites-enabled` son carpetas de la organización del paquete Ubuntu. La configuración principal incluye los sitios habilitados.

`proxy_pass` apunta a Python. `proxy_set_header` establece las cabeceras que NGINX envía a la aplicación. El cliente se conecta con NGINX y este abre otra conexión con Python. No cambia la dirección del navegador.

Para una prueba desde otro equipo, usa la IP de la máquina en lugar de `127.0.0.1` y conserva la cabecera `Host`. Permite TCP 80 desde el equipo de prueba en las reglas de red aplicables de Ubuntu y GCP. El puerto 8000 permanece ligado a loopback.

## 6. Captura de tráfico

Instala los capturadores. Si la instalación de TShark pregunta por captura para usuarios no administradores, puedes elegir **No** y usar `sudo` en este laboratorio.

```bash
sudo apt install tcpdump tshark
```

En una terminal, inicia la captura sencilla:

```bash
sudo tcpdump -i lo -nn 'tcp port 8000'
```

En otra, genera la petición a través de NGINX:

```bash
curl -H "Host: sesion11.local" http://127.0.0.1/
```

El filtro muestra la conexión interna de NGINX a Python. Ctrl+C detiene cada captura antes de probar la siguiente variante:

```bash
# Mostrar texto HTTP de este laboratorio
sudo tcpdump -i lo -nn -s 0 -A 'tcp port 8000'
# Ver ambas conexiones en la prueba local
sudo tcpdump -i lo -nn 'tcp port 80 or tcp port 8000'
# Wireshark desde la consola
sudo tshark -i lo -n -f "tcp port 8000"
# Guardar paquetes para revisarlos despues
sudo tshark -i lo -f "tcp port 8000" -w /tmp/sesion11.pcapng
```

Genera peticiones mientras esté activa la captura elegida. Después de detener la última, lee el archivo:

```bash
sudo tshark -r /tmp/sesion11.pcapng -Y "http"
```

Si HTTP no se reconoce automáticamente en el puerto 8000:

```bash
sudo tshark -r /tmp/sesion11.pcapng \
  -d tcp.port==8000,http -Y "http"
```

`-f` decide qué capturar. `-Y` decide qué mostrar al analizar. `-d` indica cómo interpretar ese puerto. Wireshark con interfaz gráfica también puede abrir el archivo. Usa solo tráfico de prueba sin secretos. HTTPS cifra el contenido del tramo que protege.

## 6. Diagnóstico y cierre

| Evidencia | Siguiente revisión |
| --- | --- |
| No hay escucha en 8000 | Estado y journal de `sesion11` |
| Respuesta directa correcta, página predeterminada por 80 | Cabecera `Host` y enlace del sitio |
| Respuesta `502 Bad Gateway` | Destino del proxy, escucha Python y `error.log` |
| Captura vacía | Petición generada, interfaz y filtro |

```bash
sudo journalctl -u nginx -n 20 --no-pager
sudo tail -n 20 /var/log/nginx/access.log
sudo tail -n 20 /var/log/nginx/error.log
```

Cuando termines, puedes desactivar solo este sitio y servicio:

```bash
sudo unlink /etc/nginx/sites-enabled/sesion11
sudo nginx -t
# Solo si la validacion anterior es correcta:
sudo systemctl reload nginx
sudo systemctl disable --now sesion11
```

Los archivos originales permanecen disponibles para repetir el ejercicio.

## Compilación de las diapositivas

Desde `Sesion11/slides`, con XeLaTeX instalado:

```bash
mkdir -p build
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build slides.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build slides.tex
```

La plantilla y las imágenes UTP se comparten con las sesiones anteriores. Conserva la estructura del repositorio. Las referencias técnicas están enlazadas a continuación.

## Referencias técnicas

- Ubuntu: [chown](https://manpages.ubuntu.com/manpages/noble/man1/chown.1.html), [chmod](https://manpages.ubuntu.com/manpages/noble/man1/chmod.1.html), [id](https://manpages.ubuntu.com/manpages/noble/man1/id.1.html) y [ss](https://manpages.ubuntu.com/manpages/noble/man8/ss.8.html).
- [python-dotenv](https://bbc2.github.io/python-dotenv/) y [Python: http.server](https://docs.python.org/3/library/http.server.html).
- Ubuntu: [systemctl](https://manpages.ubuntu.com/manpages/noble/man1/systemctl.1.html), [systemd.service](https://manpages.ubuntu.com/manpages/noble/man5/systemd.service.5.html) y [journalctl](https://manpages.ubuntu.com/manpages/noble/man1/journalctl.1.html).
- [Configuración de NGINX en Ubuntu](https://ubuntu.com/server/docs/how-to/web-services/configure-nginx/) y [módulo proxy de NGINX](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
- [tcpdump](https://manpages.ubuntu.com/manpages/noble/man8/tcpdump.8.html) y [TShark](https://www.wireshark.org/docs/man-pages/tshark).
