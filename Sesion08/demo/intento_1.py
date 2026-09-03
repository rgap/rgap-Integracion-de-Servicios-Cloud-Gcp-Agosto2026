#!/usr/bin/env python3
"""Intento 1: tu equipo entra por SSH desde la red local. Se espera PERMITIR.

Requiere servicio.py y servicio_firewall.py corriendo en otras terminales.
"""

import socket

FIREWALL = ("127.0.0.1", 9000)  # toda conexión entra por el firewall

ORIGEN = "192.168.100.161"  # tu equipo, dentro de la red local 192.168.100.0/24
PUERTO = 22                 # SSH

# La regla 2 permite toda la red 192.168.100.0/24 en el puerto 22: el intento pasa.


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
