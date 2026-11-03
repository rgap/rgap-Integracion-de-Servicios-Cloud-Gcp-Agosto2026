// Servidor de la tienda de Pedidos Express.
//
// Se ejecuta tres veces, una por puerto:
//   node server.js 3001
//   node server.js 3002
//   node server.js 3003

import http from "node:http";
import { setTimeout as esperar } from "node:timers/promises";

const puerto = Number(process.argv[2] || 3001);

// La CPU trabaja sin parar durante los milisegundos indicados.
function calcular(milisegundos) {
  const fin = Date.now() + milisegundos;
  while (Date.now() < fin) {
    Math.sqrt(Math.random());
  }
}

// Atiende cada solicitud y devuelve el texto de la respuesta.
async function atender(metodo, ruta) {
  if (ruta === "/") {
    return "Bienvenido a la tienda";
  }

  if (ruta === "/productos") {
    await esperar(2000); // espera a la base de datos
    return "Productos obtenidos de la BD";
  }

  if (ruta === "/comprar" && metodo === "POST") {
    await esperar(5000); // espera al banco
    return "Compra procesada correctamente";
  }

  if (ruta === "/reporte") {
    calcular(5000); // la CPU trabaja: nadie más es atendido
    return "Reporte generado";
  }

  return null; // ruta que no existe
}

const servidor = http.createServer(async (req, res) => {
  console.log(`[${puerto}] INICIO ${req.method} ${req.url}`);
  const inicio = Date.now();

  const operacion = await atender(req.method, req.url);

  if (operacion === null) {
    res.writeHead(404);
    res.end("No encontrado\n");
    return;
  }

  const duracion = Date.now() - inicio;

  res.writeHead(200, {
    "Content-Type": "application/json; charset=utf-8",
    "X-Servidor": String(puerto),
  });
  res.end(JSON.stringify({ servidor: puerto, operacion, duracion }) + "\n");

  console.log(`[${puerto}] FIN    ${req.method} ${req.url} (${duracion} ms)`);
});

servidor.listen(puerto, () => {
  console.log(`Servidor de la tienda escuchando en el puerto ${puerto}`);
});
