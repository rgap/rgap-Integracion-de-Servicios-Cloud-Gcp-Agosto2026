#!/usr/bin/env python3
"""Servidor HTTP mínimo construido con sockets.

Material didáctico de la Sesión 07: muestra que un servidor HTTP es un
programa que escucha en un socket TCP y responde texto con un formato
acordado. No usa frameworks ni la librería http.server a propósito.
"""

import socket

# --------------------------------------------------------------------------
# 1. Dónde escucha: los dos datos que, junto al protocolo TCP, definen el socket
# --------------------------------------------------------------------------
HOST = "127.0.0.1"  # solo acepta clientes de esta misma máquina
PUERTO = 8080       # 80 exige permisos de administrador; 8080 no

# --------------------------------------------------------------------------
# 2. Qué responde: HTTP es texto plano, aquí se escribe a mano
# --------------------------------------------------------------------------
CUERPO = "Hola desde un servidor hecho con sockets\n"
RESPUESTA = (
    "HTTP/1.1 200 OK\r\n"                                # línea de estado
    "Content-Type: text/plain; charset=utf-8\r\n"        # cabecera: qué tipo de contenido viene
    f"Content-Length: {len(CUERPO.encode())}\r\n"        # cabecera: tamaño del cuerpo en bytes, no en letras
    "Connection: close\r\n"                             # cabecera: se cierra al terminar de responder
    "\r\n" + CUERPO                                      # línea en blanco: separa cabeceras del cuerpo
)
# Ojo: HTTP separa las líneas con \r\n (retorno de carro + salto), no solo con \n.


def main() -> None:
    # ----------------------------------------------------------------------
    # 3. Los cuatro pasos del servidor: socket, bind, listen, accept
    # ----------------------------------------------------------------------
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket(): AF_INET = IPv4, SOCK_STREAM = TCP
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # evita 'Address already in use' al reiniciar
    servidor.bind((HOST, PUERTO))                                 # bind(): reserva IP y puerto
    servidor.listen(5)                                            # listen(): abre la cola de espera (5 pendientes)
    print(f"Escuchando en http://{HOST}:{PUERTO} (Ctrl+C para detener)")

    # ----------------------------------------------------------------------
    # 4. El bucle eterno: un servidor nunca termina, espera y vuelve a esperar
    # ----------------------------------------------------------------------
    while True:
        cliente, direccion = servidor.accept()  # accept(): se BLOQUEA aquí hasta que alguien se conecte
        peticion = cliente.recv(1024).decode("utf-8", "replace")  # recv(): lee lo que envió el cliente
        primera_linea = peticion.splitlines()[0] if peticion else "(sin datos)"
        print(f"{direccion[0]}:{direccion[1]} pidió -> {primera_linea}")  # p. ej. GET / HTTP/1.1
        cliente.sendall(RESPUESTA.encode())  # sendall(): devuelve SIEMPRE la misma respuesta, sea cual sea la ruta
        cliente.close()                      # cierra ESTA conexión, no el servidor
        # Atiende de a uno: mientras responde, los demás esperan en la cola.
        # Un Apache real usa varios procesos o hilos para atender en paralelo.


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # Ctrl+C es la forma normal de detenerlo
        print("\nServidor detenido")
