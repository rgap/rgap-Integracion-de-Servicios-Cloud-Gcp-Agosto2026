import os

from flask import Flask, jsonify

app = Flask(__name__)

MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Mocaccino", "precio": 12},
]


@app.get("/menu")
def menu():
    return jsonify(MENU)


puerto = int(os.environ.get("PUERTO", 8080))
app.run(host="0.0.0.0", port=puerto)
