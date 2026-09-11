"""Servidor mínimo del landing page "en construcción".

Solo sirve una página estática. No hay catálogo, no hay admin, no hay base
de datos. La única acción es contactar por WhatsApp para cotizar.

Uso:
    python server.py
    PORT=3000 WHATSAPP_NUMBER=51987654321 python server.py

La configuración se toma de variables de entorno. Si existe un archivo .env
junto a server.py, se carga automáticamente al arrancar; las variables que ya
estén definidas en el entorno tienen prioridad y no se sobrescriben.
"""

import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"


def load_dotenv(path: Path) -> None:
    """Carga un archivo .env sencillo (CLAVE=valor por línea) al entorno.

    No pisa variables ya definidas, ignora líneas vacías y comentarios (#),
    y quita comillas envolventes del valor.
    """
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


load_dotenv(BASE_DIR / ".env")

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

# Número de WhatsApp en formato internacional, solo dígitos (sin +, sin espacios).
WHATSAPP_NUMBER = os.environ.get("WHATSAPP_NUMBER", "51999999999")
WHATSAPP_MESSAGE = os.environ.get(
    "WHATSAPP_MESSAGE",
    "Hola, vengo de la web y quisiera una cotización.",
)

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
}


def render_index() -> bytes:
    """Lee el HTML y reemplaza los marcadores de WhatsApp."""
    from urllib.parse import quote

    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(WHATSAPP_MESSAGE)}"
    html = html.replace("{{WHATSAPP_LINK}}", wa_link)
    html = html.replace("{{WHATSAPP_NUMBER}}", WHATSAPP_NUMBER)
    return html.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "LandingEnConstruccion/1.0"

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (nombre requerido por la librería)
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html"):
            self._send(200, render_index(), CONTENT_TYPES[".html"])
            return

        # Servir archivos estáticos dentro de STATIC_DIR (sin salir de la carpeta).
        candidate = (STATIC_DIR / path.lstrip("/")).resolve()
        if STATIC_DIR in candidate.parents and candidate.is_file():
            content_type = CONTENT_TYPES.get(
                candidate.suffix.lower(), "application/octet-stream"
            )
            self._send(200, candidate.read_bytes(), content_type)
            return

        self._send(404, b"404 - No encontrado", "text/plain; charset=utf-8")

    do_HEAD = do_GET

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Landing en http://{HOST}:{PORT}")
    print(f"WhatsApp: +{WHATSAPP_NUMBER}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        server.server_close()


if __name__ == "__main__":
    main()
