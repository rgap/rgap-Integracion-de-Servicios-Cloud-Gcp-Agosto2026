#!/usr/bin/env python3
"""Cliente de base de datos construido con sockets.

Material didáctico de la Sesión 07: mismos pasos que cliente_http.py.
Lo único que cambia es el puerto y el texto que se envía.

Requiere que servidor_mysql.py esté ejecutándose.
"""

import socket

HOST = "127.0.0.1"
PUERTO = 3307
CONSULTA = "SELECT * FROM usuarios"


def main() -> None:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PUERTO))
    cliente.sendall(CONSULTA.encode())
    respuesta = cliente.recv(4096)
    cliente.close()

    print(f"Consulta enviada: {CONSULTA}")
    print(respuesta.decode("utf-8", "replace"), end="")


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print(f"No hay nadie escuchando en {HOST}:{PUERTO}")
        print("Inicia primero servidor_mysql.py")
