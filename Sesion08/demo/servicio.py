#!/usr/bin/env python3
"""El servicio protegido: queda activo y atiende a quien logre llegar.

Material didáctico de la Sesión 08. Este programa no sabe nada del firewall,
igual que Apache o MySQL no saben nada de UFW: solo escucha y responde. Quien
decide si una conexión llega hasta aquí es servicio_firewall.py.

    Terminal 1:  python3 servicio.py            (este archivo)
    Terminal 2:  python3 servicio_firewall.py   (la puerta)
    Terminal 3:  python3 intento_1.py           (los intentos)

Se detiene con Ctrl+C.
"""

import socket
from datetime import datetime

# --------------------------------------------------------------------------
# 1. Dónde escucha
# --------------------------------------------------------------------------
HOST = "127.0.0.1"
PUERTO = 9001  # detrás del firewall, que atiende en el 9000

# --------------------------------------------------------------------------
# 2. El origen es simulado
# --------------------------------------------------------------------------
# Todos los intentos salen de esta misma máquina, así que para el sistema
# operativo siempre vienen de 127.0.0.1. Cada intento_N.py declara de qué IP
# y a qué puerto FINGE venir; el firewall razona sobre esos datos. Así se
# pueden probar orígenes de internet sin necesitar varias máquinas.


def main() -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PUERTO))
    servidor.listen(5)

    print(f"Servicio ACTIVO en {HOST}:{PUERTO} (Ctrl+C para detener)")
    print("Solo verás aquí los intentos que el firewall haya dejado pasar.\n")

    # ----------------------------------------------------------------------
    # 3. El servicio no termina: atiende y vuelve a esperar
    # ----------------------------------------------------------------------
    while True:
        cliente, _ = servidor.accept()  # se bloquea aquí hasta que llega alguien
        peticion = cliente.recv(1024).decode("utf-8", "replace").strip()
        origen, puerto = peticion.split()

        marca = datetime.now().strftime("%H:%M:%S")
        # flush: que la línea aparezca al instante aunque la salida se redirija
        print(f"[{marca}] atendiendo a {origen} (puerto {puerto})", flush=True)

        cliente.sendall(f"PERMITIDO. Servicio atendido a las {marca}\n".encode())
        cliente.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServicio detenido")
