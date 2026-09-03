#!/usr/bin/env python3
"""Servidor de base de datos simulado, construido con sockets.

Material didáctico de la Sesión 08: mismo esqueleto que el servidor_http.py
de la Sesión 07, pero en vez de responder páginas responde filas. Sirve
para ver que una base de datos también es un programa escuchando en un puerto.

Usa el 3307 para no chocar con un MySQL real, que ocupa el 3306.
"""

import socket

# --------------------------------------------------------------------------
# 1. El socket se define igual que en HTTP
# --------------------------------------------------------------------------
HOST = "127.0.0.1"
PUERTO = 3307  # 3306 es el puerto oficial de MySQL: no se toca para no chocar

# --------------------------------------------------------------------------
# 2. "La base de datos": una lista en memoria, sin disco ni SQL de verdad
# --------------------------------------------------------------------------
TABLA = [
    (1, "Ana", "ana@utp.edu.pe"),
    (2, "Luis", "luis@utp.edu.pe"),
    (3, "Sara", "sara@utp.edu.pe"),
]
# Al no guardar nada en disco, los datos se pierden al detener el programa.
# Un MySQL real los conserva: esa es una de las diferencias clave.


def responder(consulta: str) -> str:
    """Interpreta el texto recibido: es el 'motor SQL' del ejemplo."""
    consulta = consulta.strip().rstrip(";").upper()  # tolera espacios sobrantes, ; final y minúsculas
    if consulta == "SELECT * FROM USUARIOS":
        filas = [f"{id} | {nombre} | {correo}" for id, nombre, correo in TABLA]
        return "\n".join(filas) + "\n"
    return "ERROR: solo se admite SELECT * FROM usuarios\n"  # cualquier otra consulta se rechaza


def main() -> None:
    # ----------------------------------------------------------------------
    # 3. Los mismos cuatro pasos: socket, bind, listen, accept
    # ----------------------------------------------------------------------
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 + TCP
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)
    print(f"Base de datos escuchando en {HOST}:{PUERTO} (Ctrl+C para detener)")

    # ----------------------------------------------------------------------
    # 4. Bucle idéntico al del servidor HTTP: cambia lo que se responde, no el mecanismo
    # ----------------------------------------------------------------------
    while True:
        cliente, direccion = servidor.accept()  # espera bloqueado a que llegue un cliente
        consulta = cliente.recv(1024).decode("utf-8", "replace")  # aquí llega texto SQL, antes llegaba HTTP
        print(f"{direccion[0]} consultó -> {consulta.strip()}")
        cliente.sendall(responder(consulta).encode())  # en vez de una página, filas de una tabla
        cliente.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido")
