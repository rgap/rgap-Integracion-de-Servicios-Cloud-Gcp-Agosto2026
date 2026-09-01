#!/usr/bin/env python3

from datetime import datetime
import subprocess
import sys


SERVICIOS_PREDETERMINADOS = ("mysql.service", "mi-api.service")


def consultar(accion: str, servicio: str) -> str:
    resultado = subprocess.run(
        ["systemctl", accion, servicio],
        capture_output=True,
        text=True,
        check=False,
    )
    salida = resultado.stdout.strip() or resultado.stderr.strip()
    return salida or "sin respuesta"


def main() -> None:
    servicios = tuple(sys.argv[1:]) or SERVICIOS_PREDETERMINADOS
    print(f"Monitoreo: {datetime.now():%Y-%m-%d %H:%M:%S}")
    for servicio in servicios:
        activo = consultar("is-active", servicio)
        habilitado = consultar("is-enabled", servicio)
        print(f"{servicio:20} activo={activo:10} inicio={habilitado}")


if __name__ == "__main__":
    main()

