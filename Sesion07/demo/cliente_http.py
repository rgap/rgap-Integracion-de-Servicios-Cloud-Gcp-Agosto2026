#!/usr/bin/env python3
"""Cliente HTTP mínimo construido con sockets.

Material didáctico de la Sesión 07: hace a mano lo mismo que `curl`.
Muestra que el cliente sigue una secuencia más corta que el servidor:
no necesita bind() ni listen(), porque no espera a nadie.

Requiere que servidor_http.py esté ejecutándose.
"""

import socket

HOST = "127.0.0.1"
PUERTO = 8080

PETICION = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}:{PUERTO}\r\n"
    "Connection: close\r\n"
    "\r\n"
)


def main() -> None:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PUERTO))
    cliente.sendall(PETICION.encode())

    respuesta = b""
    while True:
        trozo = cliente.recv(1024)
        if not trozo:
            break
        respuesta += trozo
    cliente.close()

    print(respuesta.decode("utf-8", "replace"))


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print(f"No hay nadie escuchando en {HOST}:{PUERTO}")
        print("Inicia primero servidor_http.py")
