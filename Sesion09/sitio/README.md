# Práctica — un sitio en Python publicado con nginx

Diapositiva 34 de la Sesión 08. El objetivo es doble: entender el **proxy
inverso** (nginx delante, Python detrás) y corregir los **permisos** de los
archivos del proyecto.

## Archivos

| Archivo | Para qué |
| --- | --- |
| `sitio.py` | El servidor en Python, escuchando en `127.0.0.1:3000`. |
| `iniciar.sh` | Lo arranca. Empieza sin permiso `x`: hay que dárselo. |
| `.env` | Configuración con una clave de mentira. Empieza legible por todos. |
| `nginx-sitio.conf` | El bloque `server` que hay que poner en nginx. |

## 1. Probar el sitio solo

```text
$ python3 sitio.py
Servidor corriendo en http://127.0.0.1:3000
$ curl 127.0.0.1:3000
<h1>Hola desde Python 🧪</h1>
```

Desde el host, `http://VM_IP:3000` **no** responde: el servidor escucha en
`127.0.0.1`, no en todas las interfaces.

## 2. Publicarlo con nginx

```text
$ sudo cp nginx-sitio.conf /etc/nginx/sites-available/default
$ sudo nginx -t
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ sudo systemctl reload nginx
$ sudo ufw allow 80/tcp
```

Ahora `http://VM_IP` sí muestra la página, **con el 3000 cerrado**. Quien
atiende desde fuera es nginx; Python solo habla con él.

Se usa `reload` y no `restart` porque solo cambió la configuración: el servicio
no se corta. Es la distinción de la diapositiva 8.

## 3. Corregir los permisos

```text
$ ls -la
-rw-rw-r-- 1 usuario usuario   63 .env
-rw-rw-r-- 1 usuario usuario  138 iniciar.sh

$ ./iniciar.sh
bash: ./iniciar.sh: Permiso denegado

$ chmod u+x iniciar.sh     # solo el propietario necesita ejecutarlo
$ chmod 600 .env           # nadie más debe leer la clave
$ ls -l iniciar.sh .env
-rwxrw-r-- 1 usuario usuario  138 iniciar.sh
-rw------- 1 usuario usuario   63 .env
```

## Qué hay que poder explicar

- **Por qué el 3000 no necesita abrirse:** nginx llega a él desde la propia
  máquina, por `127.0.0.1`. Abrirlo solo agregaría una puerta de más, y la
  regla es abrir lo mínimo.
- **Por qué `u+x` y no `777`:** basta con que el propietario pueda ejecutar el
  script. `777` no arregla nada y amplía quién puede provocar problemas.
- **Por qué `600` en el `.env`:** contiene una credencial, y en un servidor hay
  otros usuarios y otros servicios.

## Volver al estado inicial

```text
$ chmod 664 iniciar.sh .env
```
