const http = require('http');
const net = require('net');

function mysqlDisponible(callback) {
  const socket = net.createConnection({ host: '127.0.0.1', port: 3306 });
  let respondio = false;

  const terminar = (disponible) => {
    if (respondio) return;
    respondio = true;
    socket.destroy();
    callback(disponible);
  };

  socket.setTimeout(1000);
  socket.once('connect', () => terminar(true));
  socket.once('timeout', () => terminar(false));
  socket.once('error', () => terminar(false));
}

const server = http.createServer((req, res) => {
  mysqlDisponible((mysqlOk) => {
    const estado = { node: 'activo', mysql: mysqlOk ? 'alcanzable' : 'sin respuesta' };
    res.writeHead(mysqlOk ? 200 : 503, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(estado));
  });
});

server.listen(8000, '127.0.0.1', () => {
  console.log('API lista en http://127.0.0.1:8000');
});

