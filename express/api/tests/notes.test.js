import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { once } from 'node:events';
import { randomUUID } from 'node:crypto';
import { createApp } from '../src/app.js';

// Tes diturunkan dari kriteria selesai di specs/catatan.spec.md (bagian 5 dan 7).
// Penyimpanan berbagi satu proses: setiap tes membuat catatannya sendiri.

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

function request(method, path, body) {
  return fetch(`${baseUrl}${path}`, {
    method,
    headers: body === undefined ? {} : { 'content-type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

async function createNote(body = { title: 'Rapat pagi', body: 'Bahas rencana sprint.' }) {
  const res = await request('POST', '/api/notes', body);
  assert.equal(res.status, 201);
  return (await res.json()).data;
}

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

// ---------- Membuat ----------

test('membuat catatan valid mengembalikan 201 dengan id dan createdAt dari server', async () => {
  const sebelum = Date.now();
  const res = await request('POST', '/api/notes', { title: 'Rapat pagi', body: 'Bahas sprint.' });
  const { data } = await res.json();

  assert.equal(res.status, 201);
  assert.equal(data.title, 'Rapat pagi');
  assert.equal(data.body, 'Bahas sprint.');
  assert.match(data.id, UUID_RE);
  assert.ok(Date.parse(data.createdAt) >= sebelum - 1000, 'createdAt berupa waktu ISO dari server');
  assert.deepEqual(Object.keys(data).sort(), ['body', 'createdAt', 'id', 'title']);
});

test('body yang dihilangkan saat membuat dianggap teks kosong', async () => {
  const note = await createNote({ title: 'Tanpa isi' });
  assert.equal(note.body, '');
});

test('judul tidak dipangkas atau diubah server', async () => {
  const note = await createNote({ title: '  Judul berspasi  ' });
  assert.equal(note.title, '  Judul berspasi  ');
});

test('judul tepat 100 karakter dan isi tepat 5000 karakter diterima', async () => {
  const note = await createNote({ title: 'a'.repeat(100), body: 'b'.repeat(5000) });
  assert.equal(note.title.length, 100);
  assert.equal(note.body.length, 5000);
});

for (const [kasus, payload] of [
  ['judul kosong', { title: '' }],
  ['judul hanya spasi', { title: '   ' }],
  ['judul tidak dikirim', { body: 'isi saja' }],
  ['judul lebih dari 100 karakter', { title: 'a'.repeat(101) }],
  ['isi lebih dari 5000 karakter', { title: 'Judul', body: 'b'.repeat(5001) }],
  ['judul bukan teks', { title: 123 }],
]) {
  test(`menolak ${kasus} dengan 400`, async () => {
    const res = await request('POST', '/api/notes', payload);
    const body = await res.json();

    assert.equal(res.status, 400);
    assert.equal(body.error.code, 'VALIDATION_ERROR');
  });
}

test('menolak kolom tak dikenal, termasuk id dan createdAt, saat membuat', async () => {
  for (const extra of [{ id: randomUUID() }, { createdAt: '2000-01-01T00:00:00.000Z' }, { owner: 'x' }]) {
    const res = await request('POST', '/api/notes', { title: 'Judul', ...extra });
    assert.equal(res.status, 400, `kolom ${Object.keys(extra)[0]} harus ditolak`);
  }
});

// ---------- Melihat ----------

test('daftar catatan memuat catatan yang baru dibuat', async () => {
  const note = await createNote();
  const res = await request('GET', '/api/notes');
  const { data } = await res.json();

  assert.equal(res.status, 200);
  assert.ok(Array.isArray(data));
  assert.ok(data.some((n) => n.id === note.id));
});

test('mengambil satu catatan berdasarkan id', async () => {
  const note = await createNote();
  const res = await request('GET', `/api/notes/${note.id}`);

  assert.equal(res.status, 200);
  assert.deepEqual((await res.json()).data, note);
});

test('id yang bukan UUID mengembalikan 400', async () => {
  const res = await request('GET', '/api/notes/bukan-uuid');
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error.code, 'VALIDATION_ERROR');
});

test('id valid yang tidak ada mengembalikan 404 NOTE_NOT_FOUND', async () => {
  const res = await request('GET', `/api/notes/${randomUUID()}`);
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error.code, 'NOTE_NOT_FOUND');
});

// ---------- Mengubah ----------

test('mengubah sebagian hanya mengubah kolom yang dikirim', async () => {
  const note = await createNote({ title: 'Lama', body: 'Isi tetap' });
  const res = await request('PATCH', `/api/notes/${note.id}`, { title: 'Baru' });
  const { data } = await res.json();

  assert.equal(res.status, 200);
  assert.equal(data.title, 'Baru');
  assert.equal(data.body, 'Isi tetap');
  assert.equal(data.id, note.id);
  assert.equal(data.createdAt, note.createdAt);
});

test('mengubah body saja tidak mengubah judul', async () => {
  const note = await createNote({ title: 'Judul tetap', body: 'Lama' });
  const { data } = await (await request('PATCH', `/api/notes/${note.id}`, { body: 'Baru' })).json();
  assert.equal(data.title, 'Judul tetap');
  assert.equal(data.body, 'Baru');
});

test('PATCH tanpa kolom ({}) ditolak 400', async () => {
  const note = await createNote();
  const res = await request('PATCH', `/api/notes/${note.id}`, {});
  assert.equal(res.status, 400);
});

test('PATCH dengan judul hanya spasi ditolak 400', async () => {
  const note = await createNote();
  const res = await request('PATCH', `/api/notes/${note.id}`, { title: '   ' });
  assert.equal(res.status, 400);
});

test('id dan createdAt tidak bisa ditimpa lewat PATCH', async () => {
  const note = await createNote();
  const res = await request('PATCH', `/api/notes/${note.id}`, { title: 'X', id: randomUUID() });
  assert.equal(res.status, 400);

  const after = (await (await request('GET', `/api/notes/${note.id}`)).json()).data;
  assert.deepEqual(after, note);
});

test('PATCH pada catatan yang tidak ada mengembalikan 404', async () => {
  const res = await request('PATCH', `/api/notes/${randomUUID()}`, { title: 'X' });
  assert.equal(res.status, 404);
});

// ---------- Menghapus ----------

test('menghapus mengembalikan 204 dan GET setelahnya 404', async () => {
  const note = await createNote();
  const res = await request('DELETE', `/api/notes/${note.id}`);

  assert.equal(res.status, 204);
  assert.equal(await res.text(), '');
  assert.equal((await request('GET', `/api/notes/${note.id}`)).status, 404);
});

test('menghapus catatan yang sudah terhapus mengembalikan 404', async () => {
  const note = await createNote();
  await request('DELETE', `/api/notes/${note.id}`);
  const res = await request('DELETE', `/api/notes/${note.id}`);
  assert.equal(res.status, 404);
});

// ---------- Keamanan respons ----------

test('respons error tidak memuat stack trace atau detail internal', async () => {
  const responses = [
    await request('POST', '/api/notes', { title: '' }),
    await request('GET', '/api/notes/bukan-uuid'),
    await request('GET', `/api/notes/${randomUUID()}`),
  ];
  for (const res of responses) {
    const text = await res.text();
    assert.ok(!/stack|\bat .+\.js:\d+/i.test(text), `tidak boleh ada stack trace: ${text}`);
    assert.ok(JSON.parse(text).error.message);
  }
});
