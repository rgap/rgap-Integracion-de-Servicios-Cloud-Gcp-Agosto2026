# ecommerce_webapp — Landing "en construcción"

## Correr

```bash
cd ecommerce_webapp
python server.py
```

Abre http://127.0.0.1:8000

## Configuración (variables de entorno)

| Variable           | Default                                             | Descripción                                     |
| ------------------ | --------------------------------------------------- | ----------------------------------------------- |
| `PORT`             | `8000`                                              | Puerto del servidor                             |
| `HOST`             | `127.0.0.1`                                         | Host de escucha                                 |
| `WHATSAPP_NUMBER`  | `51999999999`                                       | Número en formato internacional, solo dígitos   |
| `WHATSAPP_MESSAGE` | `Hola, vengo de la web y quisiera una cotización.`  | Texto que se autocompleta en el chat            |

Ejemplo:

```bash
WHATSAPP_NUMBER=51987654321 PORT=3000 python server.py
```

### Archivo `.env`

Si colocas un archivo `.env` junto a `server.py`, el servidor lo carga
automáticamente al arrancar (formato `CLAVE=valor`, una por línea; `#` para
comentarios). Las variables ya presentes en el entorno tienen prioridad y no se
sobrescriben.

```dotenv
HOST=127.0.0.1
PORT=8000
WHATSAPP_NUMBER=51987654321
WHATSAPP_MESSAGE=Hola, vengo de la web y quisiera una cotización.
```

## Estructura

```
ecommerce_webapp/
├── server.py           # http.server (BaseHTTPRequestHandler, HTTPServer)
├── .env                # opcional: configuración local (no versionar con datos reales)
├── static/
│   ├── index.html      # el landing page "en construcción"
│   └── style.css       # mismos estilos/colores del sitio Estampa
└── README.md
```

El `style.css` es una copia del sistema de diseño de `2_sistema_sqlite/public/style.css`
(paleta morada, tipografía Archivo Black / Inter, bordes y sombras duras), para que
la portada se vea igual que el resto del sitio.

> Cuando toque conectar la base de datos / catálogo, este proyecto se reemplaza
> por la app completa. Por ahora es solo la portada.
