// Prueba de estrés: sube de 0 a 200 usuarios a la vez, hasta ver dónde se rompe.
// Sin pausa: cada usuario vuelve a pedir el menú apenas recibe la respuesta.
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  // Cada etapa lleva los usuarios, poco a poco, hasta el número de target.
  stages: [
    { duration: '30s', target: 20 },
    { duration: '30s', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 200 },
    { duration: '10s', target: 0 },
  ],
  // La misma meta que en la prueba de carga.
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${__ENV.URL}/menu`);
  check(res, { 'responde 200': (r) => r.status === 200 });
}
