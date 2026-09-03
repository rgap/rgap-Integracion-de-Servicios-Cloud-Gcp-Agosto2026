#!/usr/bin/env python3
"""Intento 2: una IP de internet busca la base de datos. Se espera DENEGAR.

Requiere servicio.py y servicio_firewall.py corriendo en otras terminales.
"""

import socket

FIREWALL = ("127.0.0.1", 9000)  # toda conexión entra por el firewall

ORIGEN = "203.0.113.9"      # una IP cualquiera de internet
PUERTO = 3306               # MySQL

# La única regla del 3306 exige origen 192.168.100.158 (la propia VM):
# ninguna coincide y manda la política por defecto. La base de datos no se
# expone a internet.


def main() -> None:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(FIREWALL)
    cliente.sendall(f"{ORIGEN} {PUERTO}".encode())  # declara de dónde finge venir
    respuesta = cliente.recv(1024)
    cliente.close()

    print(f"Intento desde {ORIGEN} al puerto {PUERTO}")
    print(respuesta.decode("utf-8", "replace"), end="")


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("El firewall no está activo. Inicia primero servicio_firewall.py")
