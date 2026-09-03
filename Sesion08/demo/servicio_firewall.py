#!/usr/bin/env python3
"""El firewall como servicio: queda activo y filtra todo lo que entra.

Material didáctico de la Sesión 08. Un firewall no es un servidor al que uno
se conecta para pedirle algo: es un servicio que se queda corriendo y revisa
el tráfico que pasa, dejándolo seguir o descartándolo.

Aquí es la puerta de la máquina: los intento_N.py llegan a él, y solo los
permitidos se reenvían al servicio real (servicio.py). Los denegados nunca
llegan a tocarlo.

    Terminal 1:  python3 servicio.py            (el servicio protegido)
    Terminal 2:  python3 servicio_firewall.py   (la puerta, este archivo)
    Terminal 3:  python3 intento_1.py           (los intentos)

Se detiene con Ctrl+C.
"""

import ipaddress
import socket
from datetime import datetime

# --------------------------------------------------------------------------
# 1. Las direcciones de nuestro escenario
# --------------------------------------------------------------------------
RED_LOCAL = "192.168.100.0/24"   # la red de casa o del aula
IP_VM = "192.168.100.158"        # la máquina virtual: aquí corre el servicio
IP_BANEADA = "203.0.113.66"      # origen abusivo: se le cierra la máquina entera

# --------------------------------------------------------------------------
# 2. Política por defecto: qué pasa cuando NINGUNA regla coincide
# --------------------------------------------------------------------------
POLITICA_POR_DEFECTO = "DENEGAR"  # cerrar todo y abrir solo lo necesario

# --------------------------------------------------------------------------
# 3. Las reglas: se revisan EN ORDEN y gana la primera que coincide
# --------------------------------------------------------------------------
CUALQUIER_PUERTO = "cualquiera"

REGLAS = [
    # El baneo va PRIMERO, y sin puerto: bloquea a esa IP en TODA la máquina.
    # Si estuviera al final nunca se aplicaría al puerto 80, porque la regla
    # de más abajo ya habría permitido el paso. El orden es la regla del juego.
    {"origen": f"{IP_BANEADA}/32", "puerto": CUALQUIER_PUERTO, "accion": "DENEGAR"},
    {"origen": RED_LOCAL, "puerto": 22, "accion": "PERMITIR"},       # SSH solo desde la red local
    {"origen": "0.0.0.0/0", "puerto": 80, "accion": "PERMITIR"},     # web HTTP abierta a todo internet
    {"origen": "0.0.0.0/0", "puerto": 443, "accion": "PERMITIR"},    # web HTTPS abierta a todo internet
    {"origen": f"{IP_VM}/32", "puerto": 3306, "accion": "PERMITIR"}, # MySQL solo desde la propia VM
]
# El número tras la barra indica el tamaño de la red:
# /24 = las 256 IPs de esa red, /0 = cualquier IP de internet, /32 = una sola IP.

# --------------------------------------------------------------------------
# 4. Dónde escucha el firewall y dónde vive el servicio que protege
# --------------------------------------------------------------------------
PUERTA = ("127.0.0.1", 9000)    # aquí llegan los intentos: es la puerta de la máquina
SERVICIO = ("127.0.0.1", 9001)  # detrás del firewall, solo alcanzable si la regla lo permite


def coincide(regla: dict, direccion, puerto: int) -> bool:
    """¿Esta regla aplica a este intento? Deben coincidir origen Y puerto."""
    if direccion not in ipaddress.ip_network(regla["origen"]):
        return False
    return regla["puerto"] == CUALQUIER_PUERTO or regla["puerto"] == puerto


def evaluar(origen: str, puerto: int) -> tuple[str, str]:
    """Devuelve la acción y el motivo, para poder explicar la decisión."""
    direccion = ipaddress.ip_address(origen)
    for numero, regla in enumerate(REGLAS, start=1):  # recorre en orden, como un firewall real
        if coincide(regla, direccion, puerto):        # primera coincidencia: decide y sale
            return regla["accion"], f"regla {numero}"
    return POLITICA_POR_DEFECTO, "política por defecto"


def reenviar(peticion: str) -> str:
    """Pasa la petición al servicio protegido y devuelve su respuesta."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(SERVICIO)
        s.sendall(peticion.encode())
        respuesta = s.recv(1024).decode("utf-8", "replace")
        s.close()
        return respuesta
    except ConnectionRefusedError:
        # El firewall dejó pasar, pero detrás no hay nadie escuchando.
        # Es el otro motivo por el que un servicio "no responde".
        return "El firewall permitió el paso, pero el servicio no está activo\n"


def filtrar(peticion: str) -> str:
    """Decide qué hacer con un intento y lo registra."""
    origen, puerto = peticion.split()
    accion, motivo = evaluar(origen, int(puerto))

    marca = datetime.now().strftime("%H:%M:%S")
    # flush: que la línea aparezca al instante aunque la salida se redirija
    print(f"[{marca}] {origen:15} -> puerto {puerto:<5} {accion:9} ({motivo})", flush=True)

    if accion == "PERMITIR":
        return reenviar(peticion)
    return f"DENEGADO por el firewall ({motivo})\n"
    # Un firewall real con deny no respondería nada: dejaría la conexión
    # colgada. Aquí sí se contesta para que en clase se vea qué regla decidió.


def mostrar_politica() -> None:
    print(f"FIREWALL ACTIVO en {PUERTA[0]}:{PUERTA[1]}, protegiendo la VM {IP_VM}")
    print(f"Política por defecto: {POLITICA_POR_DEFECTO}")
    for numero, regla in enumerate(REGLAS, start=1):
        puerto = regla["puerto"]
        puerto = "cualquiera" if puerto == CUALQUIER_PUERTO else str(puerto)
        print(f"  regla {numero}  {regla['accion']:9} origen {regla['origen']:18} puerto {puerto}")
    print("\nEsperando intentos... (Ctrl+C para detener)\n")


def main() -> None:
    firewall = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    firewall.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    firewall.bind(PUERTA)
    firewall.listen(5)
    mostrar_politica()

    # ----------------------------------------------------------------------
    # 5. El servicio no termina: filtra un intento y vuelve a esperar
    # ----------------------------------------------------------------------
    while True:
        conexion, _ = firewall.accept()  # se bloquea aquí hasta que llega un intento
        peticion = conexion.recv(1024).decode("utf-8", "replace").strip()
        conexion.sendall(filtrar(peticion).encode())
        conexion.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nFirewall detenido")
