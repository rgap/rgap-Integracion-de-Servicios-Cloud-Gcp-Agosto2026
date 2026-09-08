#!/usr/bin/env python3
"""Servidor web del proyecto, escrito con la librería estándar.

Material didáctico de la Sesión 08. En la Sesión 07 el servidor se construyó
con sockets para ver el mecanismo por dentro; aquí se usa http.server, que es
lo que se escribe en la práctica: la librería ya se encarga de leer la
petición, separar las cabeceras y armar la respuesta.

Lee su configuración del archivo .env de esta misma carpeta, y por eso ese
archivo debe estar protegido con chmod 600.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PUERTO = 8080

ARCHIVO_ENV = Path(__file__).parent / ".env"


def cargar_env() -> dict:
    """Lee el .env línea por línea: CLAVE=valor."""
    config = {}
    if not ARCHIVO_ENV.exists():
        return config
    for linea in ARCHIVO_ENV.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):  # ignora vacías y comentarios
            continue
        clave, _, valor = linea.partition("=")
        config[clave.strip()] = valor.strip()
    return config


CONFIG = cargar_env()


class Manejador(BaseHTTPRequestHandler):
    """Una clase con un método por cada verbo HTTP que se quiera atender."""

    def do_GET(self) -> None:
        # do_GET se ejecuta en cada petición GET. self.path trae la ruta pedida.
        usuario = CONFIG.get("DB_USER", "(sin .env)")
        cuerpo = (
            "<h1>Proyecto de la Sesion 08</h1>"
            f"<p>Ruta pedida: {self.path}</p>"
            f"<p>Usuario de base de datos: {usuario}</p>"
        ).encode("utf-8")

        # Nunca se envía DB_PASSWORD ni API_KEY: el .env se lee en el servidor,
        # no se muestra al visitante. Proteger el archivo y no filtrar su
        # contenido son dos cuidados distintos, y hacen falta los dos.

        self.send_response(200)                                  # línea de estado
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()                                       # cierra las cabeceras
        self.wfile.write(cuerpo)                                 # y ahora el cuerpo

    def log_message(self, formato, *args) -> None:
        """Registro de accesos, como el access.log de nginx."""
        print(f"{self.client_address[0]} -> {formato % args}")


def main() -> None:
    servidor = HTTPServer((HOST, PUERTO), Manejador)
    print(f"Escuchando en http://{HOST}:{PUERTO} (Ctrl+C para detener)")
    print(f"Configuración leída de .env: {len(CONFIG)} variables")
    servidor.serve_forever()  # el bucle infinito lo pone la librería


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido")
