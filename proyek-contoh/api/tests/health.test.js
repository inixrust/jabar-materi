import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createApp } from '../src/app.js';

let server;
let baseUrl;

before(async () => {
  server = createApp().listen(0);
  await once(server, 'listening');
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(() => {
  server.closeAllConnections();
  server.close();
});

test('[REQ-001] GET /api/health mengembalikan status ok', async () => {
  const res = await fetch(`${baseUrl}/api/health`);
  const body = await res.json();

  assert.equal(res.status, 200);
  assert.equal(body.data.status, 'ok');
});

test('[NFR-002] rute yang tidak ada mengembalikan 404 dengan format error standar', async () => {
  const res = await fetch(`${baseUrl}/api/tidak-ada`);
  const body = await res.json();

  assert.equal(res.status, 404);
  assert.equal(body.error.code, 'NOT_FOUND');
});

test('[NFR-002][SC-09] JSON rusak mengembalikan 400 tanpa membocorkan stack trace', async () => {
  const res = await fetch(`${baseUrl}/api/health`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: '{rusak',
  });
  const text = await res.text();

  assert.equal(res.status, 400);
  assert.equal(JSON.parse(text).error.code, 'INVALID_JSON');
  assert.ok(!text.includes('stack'), 'respons tidak boleh memuat stack trace');
});

test('[SC-08] header keamanan terpasang dan x-powered-by tidak dikirim', async () => {
  const res = await fetch(`${baseUrl}/api/health`);

  assert.equal(res.headers.get('x-content-type-options'), 'nosniff');
  assert.equal(res.headers.get('x-powered-by'), null);
});
