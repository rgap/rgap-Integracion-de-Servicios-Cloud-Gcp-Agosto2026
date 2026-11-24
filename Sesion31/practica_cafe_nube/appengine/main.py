from flask import Flask, jsonify

app = Flask(__name__)

MENU = [
    {"nombre": "Americano", "precio": 8},
    {"nombre": "Capuchino", "precio": 10},
    {"nombre": "Latte", "precio": 12},
]


@app.get("/menu")
def menu():
    return jsonify(MENU)
