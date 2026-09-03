#!/usr/bin/env python3
"""Intento 3: la IP baneada toca un puerto abierto a todos. Se espera DENEGAR.

Requiere servicio.py y servicio_firewall.py corriendo en otras terminales.
"""

import socket

FIREWALL = ("127.0.0.1", 9000)  # toda conexión entra por el firewall

ORIGEN = "203.0.113.66"     # la IP baneada en servicio_firewall.py
PUERTO = 80                 # HTTP: abierto a 0.0.0.0/0, o sea a todo internet

# Aquí está la idea de la demo: la regla 1 banea esa IP SIN IMPORTAR EL PUERTO
# y va primero en la lista, así que gana antes de que se mire la regla del 80.
# El mismo puerto que atiende a todo internet queda cerrado solo para ella.


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
