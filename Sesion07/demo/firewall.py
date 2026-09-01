#!/usr/bin/env python3
"""Firewall simulado: aplica una política de reglas a intentos de conexión.

Reproduce la lógica que usa un firewall real como UFW: se recorre la lista
de reglas en orden y, si ninguna coincide, se aplica la política por defecto.
No modifica el sistema; solo imprime la decisión.
"""

import ipaddress

POLITICA_POR_DEFECTO = "DENEGAR"

REGLAS = [
    {"origen": "192.168.1.0/24", "puerto": 22, "accion": "PERMITIR"},
    {"origen": "0.0.0.0/0", "puerto": 80, "accion": "PERMITIR"},
    {"origen": "0.0.0.0/0", "puerto": 443, "accion": "PERMITIR"},
    {"origen": "127.0.0.1/32", "puerto": 3306, "accion": "PERMITIR"},
]

INTENTOS = [
    ("192.168.1.45", 22),
    ("203.0.113.9", 22),
    ("203.0.113.9", 80),
    ("203.0.113.9", 3306),
    ("127.0.0.1", 3306),
]


def decidir(origen: str, puerto: int) -> str:
    direccion = ipaddress.ip_address(origen)
    for regla in REGLAS:
        red = ipaddress.ip_network(regla["origen"])
        if puerto == regla["puerto"] and direccion in red:
            return regla["accion"]
    return POLITICA_POR_DEFECTO


def main() -> None:
    print(f"Política por defecto: {POLITICA_POR_DEFECTO}\n")
    for origen, puerto in INTENTOS:
        print(f"{origen:15} -> puerto {puerto:<5} {decidir(origen, puerto)}")


if __name__ == "__main__":
    main()
