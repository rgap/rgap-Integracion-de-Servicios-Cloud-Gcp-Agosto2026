#!/usr/bin/env python3
"""Servidor HTTP mínimo construido con sockets.

Material didáctico de la Sesión 07: muestra que un servidor HTTP es un
programa que escucha en un socket TCP y responde texto con un formato
acordado. No usa frameworks ni la librería http.server a propósito.
"""

import socket

HOST = "127.0.0.1"
PUERTO = 8080

CUERPO = "Hola desde un servidor hecho con sockets\n"
RESPUESTA = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain; charset=utf-8\r\n"
    f"Content-Length: {len(CUERPO.encode())}\r\n"
    "Connection: close\r\n"
    "\r\n" + CUERPO
)


def main() -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)
    print(f"Escuchando en http://{HOST}:{PUERTO} (Ctrl+C para detener)")

    while True:
        cliente, direccion = servidor.accept()
        peticion = cliente.recv(1024).decode("utf-8", "replace")
        primera_linea = peticion.splitlines()[0] if peticion else "(sin datos)"
        print(f"{direccion[0]}:{direccion[1]} pidió -> {primera_linea}")
        cliente.sendall(RESPUESTA.encode())
        cliente.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido")
