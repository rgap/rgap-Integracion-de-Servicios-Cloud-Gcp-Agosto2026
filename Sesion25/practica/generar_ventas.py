"""Genera ventas.csv: 1.2 millones de pedidos de Pedidos Express (2023-2025).

Los datos son inventados, pero siempre salen iguales (semilla fija),
asi todos en clase obtienen los mismos resultados.

Uso:
    python generar_ventas.py
"""

import csv
import random
from datetime import date, timedelta

FILAS = 1_200_000
ARCHIVO = "ventas.csv"

PRODUCTOS = {
    "Electronica": {"Audifonos": 89.0, "Cargador": 45.0, "Mouse": 59.0, "Teclado": 129.0, "Parlante": 199.0},
    "Hogar": {"Lampara": 79.0, "Sarten": 99.0, "Juego de sabanas": 149.0},
    "Supermercado": {"Arroz 5 kg": 24.0, "Aceite": 12.0, "Cafe": 32.0, "Leche x6": 28.0},
    "Moda": {"Polo": 49.0, "Zapatillas": 249.0, "Casaca": 189.0},
    "Farmacia": {"Paracetamol": 8.0, "Protector solar": 59.0, "Vitaminas": 69.0},
}
PESO_CATEGORIA = {"Electronica": 18, "Hogar": 14, "Supermercado": 38, "Moda": 16, "Farmacia": 14}

DISTRITOS = ["Miraflores", "San Isidro", "Surco", "La Molina", "San Borja",
             "Barranco", "Jesus Maria", "Lince", "Magdalena", "Pueblo Libre"]
PESO_DISTRITO = [14, 10, 18, 9, 9, 6, 9, 8, 8, 9]

PAGOS = ["Tarjeta", "Yape", "Efectivo", "Plin"]
PESO_PAGO = [45, 30, 15, 10]

# Diciembre y julio venden mas (fiestas y gratificacion).
PESO_MES = {1: 0.9, 2: 0.85, 3: 0.95, 4: 0.95, 5: 1.0, 6: 1.0,
            7: 1.25, 8: 1.0, 9: 0.95, 10: 1.0, 11: 1.1, 12: 1.45}


def main():
    random.seed(24)

    # Cada dia de 2023 a 2025 tiene un peso: la empresa crece con el tiempo.
    dias = []
    pesos_dia = []
    inicio, fin = date(2023, 1, 1), date(2025, 12, 31)
    total_dias = (fin - inicio).days + 1
    for i in range(total_dias):
        dia = inicio + timedelta(days=i)
        dias.append(dia.isoformat())
        pesos_dia.append((1 + i / total_dias) * PESO_MES[dia.month])

    fechas = sorted(random.choices(dias, weights=pesos_dia, k=FILAS))
    categorias = random.choices(list(PESO_CATEGORIA), weights=list(PESO_CATEGORIA.values()), k=FILAS)
    distritos = random.choices(DISTRITOS, weights=PESO_DISTRITO, k=FILAS)
    pagos = random.choices(PAGOS, weights=PESO_PAGO, k=FILAS)
    cantidades = random.choices([1, 2, 3, 4, 5], weights=[55, 25, 11, 6, 3], k=FILAS)
    cancelados = random.choices([False, True], weights=[92, 8], k=FILAS)

    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["pedido_id", "fecha", "cliente_id", "distrito", "categoria", "producto",
                           "cantidad", "precio_unitario", "monto", "metodo_pago", "estado"])
        for i in range(FILAS):
            categoria = categorias[i]
            producto = random.choice(list(PRODUCTOS[categoria]))
            precio = PRODUCTOS[categoria][producto]
            cancelado = cancelados[i]
            # Un pedido cancelado no se cobra: su monto es 0.
            monto = 0.0 if cancelado else round(precio * cantidades[i], 2)
            escritor.writerow([
                f"P-{i + 1:07d}", fechas[i], f"C-{random.randint(1, 50_000):05d}",
                distritos[i], categoria, producto, cantidades[i], precio, monto,
                pagos[i], "cancelado" if cancelado else "entregado",
            ])

    print(f"Listo: {ARCHIVO} con {FILAS:,} filas.")


if __name__ == "__main__":
    main()
