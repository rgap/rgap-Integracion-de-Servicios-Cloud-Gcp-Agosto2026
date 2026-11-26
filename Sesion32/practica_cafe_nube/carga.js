// Prueba de carga: 20 usuarios a la vez durante 30 segundos.
// Cada usuario pide el menú, espera 1 segundo y vuelve a pedirlo.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 20,
  duration: '30s',
  // La meta: si no se cumple, k6 marca la prueba como fallida.
  thresholds: {
    http_req_duration: ['p(95)<300'], // 95 de cada 100 peticiones en menos de 300 ms
    http_req_failed: ['rate<0.01'],   // menos del 1 % de peticiones con error
  },
};

export default function () {
  const res = http.get(`${__ENV.URL}/menu`);
  check(res, { 'responde 200': (r) => r.status === 200 });
  sleep(1);
}
