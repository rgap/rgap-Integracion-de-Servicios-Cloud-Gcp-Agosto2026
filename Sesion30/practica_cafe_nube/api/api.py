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


app.run(host="0.0.0.0", port=8080)
