// Simula varios clientes que entran a la tienda.
//
//   node prueba.js /productos 6                 6 clientes a la vez, por Nginx
//   node prueba.js / 6 --en-fila                6 clientes, uno detrás de otro
//   node prueba.js /reporte 6 --directo 3001    6 clientes al servidor 3001,
//                                               sin pasar por Nginx

import { argv } from "node:process";

// 1. Leer lo que se escribió en la terminal.
const [ruta = "/", cantidadTexto = "1", ...opciones] = argv.slice(2);

const cantidad = Number(cantidadTexto);
const enFila = opciones.includes("--en-fila");
const posDirecto = opciones.indexOf("--directo");
const puerto = posDirecto === -1 ? 8080 : Number(opciones[posDirecto + 1]);
const metodo = ruta === "/comprar" ? "POST" : "GET";

// 2. Enviar una solicitud y anotar qué servidor respondió y cuánto tardó.
async function pedir(numero) {
  const inicio = Date.now();
  let servidor;

  try {
    const url = `http://127.0.0.1:${puerto}${ruta}`;
    const respuesta = await fetch(url, { method: metodo });
    const numeroServidor = respuesta.headers.get("x-servidor");
    servidor = numeroServidor ?? `error ${respuesta.status}`;
    await respuesta.text();
  } catch {
    servidor = "sin respuesta";
  }

  const segundos = (Date.now() - inicio) / 1000;
  return { numero, servidor, segundos };
}

// 3. Enviar todas las solicitudes.
const destino = puerto === 8080 ? "Nginx (puerto 8080)" : `servidor ${puerto}`;
console.log(`\n${cantidad} × ${metodo} ${ruta}  →  ${destino}\n`);

const inicioTotal = Date.now();
const resultados = [];

if (enFila) {
  // Una detrás de otra: espera cada respuesta antes de enviar la siguiente.
  for (let n = 1; n <= cantidad; n++) {
    resultados.push(await pedir(n));
  }
} else {
  // Todas a la vez.
  const pendientes = [];
  for (let n = 1; n <= cantidad; n++) {
    pendientes.push(pedir(n));
  }
  resultados.push(...(await Promise.all(pendientes)));
}

const total = (Date.now() - inicioTotal) / 1000;

// 4. Mostrar el resultado.
console.log("  #   servidor        tardó");
for (const r of resultados) {
  const numero = String(r.numero).padEnd(3);
  const servidor = r.servidor.padEnd(13);
  const segundos = r.segundos.toFixed(1).padStart(5);
  console.log(`  ${numero} ${servidor} ${segundos} s`);
}

const reparto = {};
for (const r of resultados) {
  reparto[r.servidor] = (reparto[r.servidor] || 0) + 1;
}

const textoReparto = Object.entries(reparto)
  .sort()
  .map(([servidor, veces]) => `${servidor}: ${veces}`)
  .join("   ");

console.log(`\nReparto: ${textoReparto}`);
console.log(`Tiempo total: ${total.toFixed(1)} s\n`);
