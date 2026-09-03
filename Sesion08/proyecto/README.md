# Proyecto de ejemplo — permisos en Linux

Carpeta que aparece en las diapositivas 30, 31 y 32 de la Sesión 08. Sirve para
practicar `ls -l` y `chmod` sobre archivos reales.

## Qué hay aquí

| Archivo | Para qué |
| --- | --- |
| `servidor_http.py` | El servidor de la Sesión 07. Se usa para el caso del permiso `x`. |
| `.env` | Credenciales de mentira. Se usa para el caso del permiso `600`. |
| `.gitignore` | Explica por qué este `.env` es la excepción y no la regla. |

## Estado inicial

Los dos archivos empiezan sin proteger y sin permiso de ejecución, que es
justamente el problema a corregir:

```text
$ ls -l
-rw-rw-r-- 1 usuario usuario   79 .env
-rw-rw-r-- 1 usuario usuario 2845 servidor_http.py
```

## Ejercicio

**Caso 1 — el `.py` no se puede ejecutar directamente:**

```text
$ ./servidor_http.py
bash: ./servidor_http.py: Permiso denegado
$ chmod u+x servidor_http.py
$ ./servidor_http.py
Escuchando en http://127.0.0.1:8080 (Ctrl+C para detener)
```

Funciona porque el archivo tiene `x` **y** empieza con `#!/usr/bin/env python3`,
la línea que le dice a Ubuntu qué intérprete usar. Hacen falta las dos cosas.

**Caso 2 — el `.env` lo puede leer cualquiera:**

```text
$ chmod 600 .env
$ ls -l .env
-rw------- 1 usuario usuario 79 .env
```

`600`: el propietario lee y escribe, nadie más entra.

## Para volver al estado inicial

```text
$ chmod 664 .env servidor_http.py
```

## Advertencia

El `.env` de esta carpeta contiene valores inventados y viaja con el material de
clase a propósito. En un proyecto real un `.env` **nunca** se sube al
repositorio: se agrega a `.gitignore` y se comparte un `.env.ejemplo` sin
secretos. `chmod 600` protege el archivo en la máquina; `.gitignore` evita que
salga de ella. Son dos protecciones distintas y hacen falta las dos.
