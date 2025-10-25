import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_failed: ['rate<0.01'],   // <1% errors
    http_req_duration: ['p(95)<300'], // p95 < 300ms
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL || 'http://localhost:8000'}/users`);
  check(res, {
    'status is 200': r => r.status === 200,
  });
  sleep(1);
}