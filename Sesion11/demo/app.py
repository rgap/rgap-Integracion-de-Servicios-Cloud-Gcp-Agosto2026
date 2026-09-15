"""Servidor didáctico de Sesion11. http.server no es para producción."""
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))
HOST = os.environ["APP_HOST"]
PORT = int(os.environ["APP_PORT"])
MESSAGE = os.environ["APP_MESSAGE"]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (MESSAGE + "\n").encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(f"Solicitud GET {self.path}", flush=True)


if __name__ == "__main__":
    with HTTPServer((HOST, PORT), Handler) as server:
        print(f"Escuchando en http://{HOST}:{PORT}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Servidor detenido", flush=True)
