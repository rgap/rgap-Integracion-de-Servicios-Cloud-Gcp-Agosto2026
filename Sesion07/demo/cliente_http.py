#!/usr/bin/env python3
"""Cliente HTTP mínimo construido con sockets.

Material didáctico de la Sesión 07: hace a mano lo mismo que `curl`.
Muestra que el cliente sigue una secuencia más corta que el servidor:
no necesita bind() ni listen(), porque no espera a nadie.

Requiere que servidor_http.py esté ejecutándose.
"""

import socket

# --------------------------------------------------------------------------
# 1. A quién se conecta: el cliente sí necesita saber la IP y el puerto del otro
# --------------------------------------------------------------------------
HOST = "127.0.0.1"
PUERTO = 8080

# --------------------------------------------------------------------------
# 2. Qué pide: la petición HTTP escrita a mano, como la que manda el navegador
# --------------------------------------------------------------------------
PETICION = (
    "GET / HTTP/1.1\r\n"          # método, ruta y versión
    f"Host: {HOST}:{PUERTO}\r\n"  # obligatoria en HTTP/1.1: dice a qué sitio se pide
    "Connection: close\r\n"       # pide cerrar al terminar: así sabemos dónde acaba la respuesta
    "\r\n"                        # línea en blanco: marca el fin de las cabeceras
)


def main() -> None:
    # ----------------------------------------------------------------------
    # 3. Los pasos del cliente: socket, connect, sendall, recv
    # ----------------------------------------------------------------------
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket(): IPv4 + TCP, igual que el servidor
    cliente.connect((HOST, PUERTO))                              # connect(): busca al servidor (no hay bind ni listen)
    cliente.sendall(PETICION.encode())                           # sendall(): por el socket viajan bytes, por eso .encode()

    # ----------------------------------------------------------------------
    # 4. Leer hasta el final: TCP entrega la respuesta por trozos, no de golpe
    # ----------------------------------------------------------------------
    respuesta = b""
    while True:
        trozo = cliente.recv(1024)  # recv(): devuelve como máximo 1024 bytes por vuelta
        if not trozo:               # bytes vacíos = el servidor cerró: fin de la respuesta
            break
        respuesta += trozo
    cliente.close()

    print(respuesta.decode("utf-8", "replace"))  # se ven las cabeceras Y el cuerpo, como en `curl -i`


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:  # nadie escucha en ese puerto: el error más común de la sesión
        print(f"No hay nadie escuchando en {HOST}:{PUERTO}")
        print("Inicia primero servidor_http.py")
