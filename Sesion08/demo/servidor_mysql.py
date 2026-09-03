#!/usr/bin/env python3
"""Servidor de base de datos simulado, construido con sockets.

Material didáctico de la Sesión 07: mismo esqueleto que servidor_http.py,
pero en vez de responder páginas responde filas. Sirve para ver que una
base de datos también es un programa escuchando en un puerto.

Usa el 3307 para no chocar con un MySQL real, que ocupa el 3306.
"""

import socket

HOST = "127.0.0.1"
PUERTO = 3307

TABLA = [
    (1, "Ana", "ana@utp.edu.pe"),
    (2, "Luis", "luis@utp.edu.pe"),
    (3, "Sara", "sara@utp.edu.pe"),
]


def responder(consulta: str) -> str:
    consulta = consulta.strip().rstrip(";").upper()
    if consulta == "SELECT * FROM USUARIOS":
        filas = [f"{id} | {nombre} | {correo}" for id, nombre, correo in TABLA]
        return "\n".join(filas) + "\n"
    return "ERROR: solo se admite SELECT * FROM usuarios\n"


def main() -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)
    print(f"Base de datos escuchando en {HOST}:{PUERTO} (Ctrl+C para detener)")

    while True:
        cliente, direccion = servidor.accept()
        consulta = cliente.recv(1024).decode("utf-8", "replace")
        print(f"{direccion[0]} consultó -> {consulta.strip()}")
        cliente.sendall(responder(consulta).encode())
        cliente.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido")
