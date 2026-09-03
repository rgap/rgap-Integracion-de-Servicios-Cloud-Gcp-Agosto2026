#!/usr/bin/env python3
"""Sitio de la práctica: un servidor HTTP en Python que sirve una página.

Material didáctico de la Sesión 08. Escucha en 127.0.0.1:3000, es decir, solo
acepta conexiones de la propia máquina. Quien lo publica hacia afuera es nginx,
que recibe en el puerto 80 y reenvía aquí (proxy_pass). Por eso el 3000 nunca
necesita abrirse en el firewall.

    $ ./iniciar.sh          o bien   $ python3 sitio.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"  # solo local: nginx es quien atiende desde fuera
PUERTO = 3000

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Laboratorio Python</title>
</head>
<body>
    <h1>Hola desde Python 🧪</h1>
    <p>Este HTML está siendo renderizado por un servidor HTTP en Python.</p>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    """Un método por cada verbo HTTP que se quiera atender."""

    def do_GET(self):
        # do_GET se ejecuta en cada petición GET que llegue.
        self.send_response(200)                                   # línea de estado
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()                                        # cierra las cabeceras

        self.wfile.write(HTML.encode("utf-8"))                    # y ahora el cuerpo
        # Todo viaja en bytes, igual que con los sockets de la Sesión 07:
        # la diferencia es que aquí la librería ya armó las cabeceras por ti.


server = HTTPServer((HOST, PUERTO), Handler)

print(f"Servidor corriendo en http://{HOST}:{PUERTO}")
server.serve_forever()  # el bucle infinito lo pone la librería
