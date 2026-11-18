import { test } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createApp } from '../src/app.js';

// Setiap tes memakai instance aplikasi sendiri, sehingga penghitung rate limit tidak saling
// memengaruhi (penyimpanan rate limit dibuat per createApp()).
async function startApp(t) {
  const server = createApp().listen(0);
  await once(server, 'listening');
  t.after(() => {
    server.closeAllConnections();
    server.close();
  });
  return `http://127.0.0.1:${server.address().port}`;
}

test('isi permintaan lebih dari 100 KB ditolak 413 dengan format error standar', async (t) => {
  const baseUrl = await startApp(t);
  const res = await fetch(`${baseUrl}/api/health`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ isi: 'a'.repeat(110 * 1024) }),
  });
  const body = await res.json();

  assert.equal(res.status, 413);
  assert.equal(body.error.code, 'PAYLOAD_TOO_LARGE');
});

test('permintaan ke-101 dalam satu menit ditolak 429 dengan format error standar', async (t) => {
  const baseUrl = await startApp(t);
  for (let i = 0; i < 100; i++) {
    const ok = await fetch(`${baseUrl}/api/health`);
    assert.equal(ok.status, 200, `permintaan ke-${i + 1} seharusnya masih diterima`);
    await ok.arrayBuffer();
  }

  const res = await fetch(`${baseUrl}/api/health`);
  const body = await res.json();

  assert.equal(res.status, 429);
  assert.equal(body.error.code, 'RATE_LIMITED');
  assert.equal(res.headers.get('ratelimit-limit'), '100', 'header RateLimit standar dikirim');
});
