#!/usr/bin/env python3
"""Cliente de base de datos construido con sockets.

Material didáctico de la Sesión 08: mismos pasos que el cliente_http.py
de la Sesión 07. Lo único que cambia es el puerto y el texto que se envía.

Requiere que servidor_mysql.py esté ejecutándose.
"""

import socket

# --------------------------------------------------------------------------
# 1. A dónde y qué: frente a cliente_http.py
# --------------------------------------------------------------------------
HOST = "127.0.0.1"
PUERTO = 3307                          # antes 8080; el mecanismo es el mismo
CONSULTA = "SELECT * FROM usuarios"    # antes una petición HTTP; ahora texto SQL


def main() -> None:
    # ----------------------------------------------------------------------
    # 2. La misma secuencia del cliente: socket, connect, sendall, recv
    # ----------------------------------------------------------------------
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 + TCP
    cliente.connect((HOST, PUERTO))     # connect(): el cliente busca; nunca espera
    cliente.sendall(CONSULTA.encode())  # todo viaja como bytes
    respuesta = cliente.recv(4096)      # una sola lectura basta: la respuesta es corta
    cliente.close()

    print(f"Consulta enviada: {CONSULTA}")
    print(respuesta.decode("utf-8", "replace"), end="")
    # Un cliente MySQL real (mysql, DBeaver) hace esto mismo, pero hablando
    # un protocolo binario con autenticación en vez de texto plano.


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:  # el servidor no está levantado
        print(f"No hay nadie escuchando en {HOST}:{PUERTO}")
        print("Inicia primero servidor_mysql.py")
