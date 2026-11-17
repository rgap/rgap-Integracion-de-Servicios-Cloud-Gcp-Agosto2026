import os

import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)
db = psycopg.connect(os.environ["DATABASE_URL"], autocommit=True)
db.execute(
    "CREATE TABLE IF NOT EXISTS producto ("
    "id SERIAL PRIMARY KEY, nombre TEXT NOT NULL UNIQUE, precio INTEGER NOT NULL)"
)
db.execute(
    "CREATE TABLE IF NOT EXISTS pedido ("
    "id SERIAL PRIMARY KEY, producto_id INTEGER NOT NULL REFERENCES producto (id), "
    "precio INTEGER NOT NULL, hora TIMESTAMP DEFAULT now())"
)
# El menú de partida, en soles. Si ya está en la base, no lo repite.
db.execute(
    "INSERT INTO producto (nombre, precio) VALUES ('Americano', 8), ('Capuchino', 10), ('Latte', 12) "
    "ON CONFLICT (nombre) DO NOTHING"
)


@app.get("/menu")
def menu():
    filas = db.execute("SELECT nombre, precio FROM producto ORDER BY id").fetchall()
    return jsonify([{"nombre": n, "precio": p} for n, p in filas])


@app.post("/pedidos")
def crear_pedido():
    fila = db.execute(
        "INSERT INTO pedido (producto_id, precio) SELECT id, precio FROM producto WHERE nombre = %s RETURNING id",
        [request.form["producto"]],
    ).fetchone()
    if fila is None:
        return {"error": "No está en el menú"}, 400
    return {"ok": True}, 201


@app.get("/pedidos")
def pedidos():
    filas = db.execute(
        "SELECT pedido.id, producto.nombre, pedido.precio, pedido.hora "
        "FROM pedido JOIN producto ON producto.id = pedido.producto_id ORDER BY pedido.id"
    ).fetchall()
    return jsonify([{"id": i, "producto": n, "precio": p, "hora": h.strftime("%H:%M")} for i, n, p, h in filas])


app.run(host="0.0.0.0", port=8080)
