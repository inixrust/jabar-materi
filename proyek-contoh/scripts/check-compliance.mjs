#!/usr/bin/env node
// Pemeriksa kepatuhan: menjaga agar kode, spec, dan plan tetap terhubung ke PRD, ARD, dan standar.
// Dijalankan dari root: npm run check:compliance
//
// Yang DIPERIKSA (mekanis):
//  1. Semua ID (REQ, NFR, ADR, SC) yang disebut di spec, plan, kode, tes, dan dokumen benar-benar ada.
//  2. Setiap spec punya baris `Mengacu:` dengan minimal satu REQ. Setiap plan mengacu ke minimal satu ADR.
//  3. Bagian "Penyimpangan dari PRD/ARD" di spec dan plan berisi "Tidak ada". Jika tidak, gagal sampai
//     manusia memutuskan dan mengubah PRD/ARD.
//  4. Persyaratan berstatus Selesai punya tes yang menyebut ID-nya.
//  5. Dependensi hanya yang ada di docs/dependencies.json.
//  6. Pola rahasia yang jelas (heuristik) tidak ada di kode.
//  7. Dokumen sumber kebenaran dan konfigurasi penegakan tidak berubah sejak disetujui manusia
//     (docs/persetujuan.sha256, diperbarui oleh manusia lewat `npm run docs:setujui`).
//
// Yang TIDAK bisa diperiksa skrip ini: apakah isi kode benar-benar sesuai MAKSUD PRD/ARD.
// Itu tugas tinjauan (subagent compliance-reviewer dan manusia).

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DILINDUNGI, hashBerkas } from './setujui-dokumen.mjs';

const root = join(fileURLToPath(new URL('.', import.meta.url)), '..');
const rel = (p) => relative(root, p).split(sep).join('/');
const read = (p) => readFileSync(p, 'utf8');
const problems = [];
const fail = (where, msg) => problems.push(`${where}: ${msg}`);

const SKIP_DIRS = new Set(['node_modules', '.next', '.git', 'coverage']);
function walk(dir, filter = () => true, out = []) {
  if (!existsSync(dir)) return out;
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, filter, out);
    else if (filter(p)) out.push(p);
  }
  return out;
}

// ---------- 0. Dokumen sumber ----------
const docs = {
  prd: join(root, 'docs/prd.md'),
  ard: join(root, 'docs/ard.md'),
  std: join(root, 'docs/standar-secure-coding.md'),
  deps: join(root, 'docs/dependencies.json'),
};
for (const [k, p] of Object.entries(docs)) {
  if (!existsSync(p)) fail(rel(p), `dokumen sumber kebenaran tidak ditemukan (${k})`);
}
if (problems.length) finish();

// ---------- 1. Kumpulkan ID yang terdefinisi ----------
const defined = new Set();
const reqStatus = new Map(); // REQ -> status

const prd = read(docs.prd);
for (const line of prd.split('\n')) {
  const m = line.match(/^\|\s*((?:REQ|NFR)-\d{3})\s*\|(.*)\|\s*$/);
  if (!m) continue;
  defined.add(m[1]);
  if (m[1].startsWith('REQ')) {
    const cells = m[2].split('|').map((c) => c.trim());
    reqStatus.set(m[1], cells[cells.length - 1]);
  }
}
for (const m of read(docs.ard).matchAll(/^###\s+(ADR-\d{3})\b/gm)) defined.add(m[1]);
for (const m of read(docs.std).matchAll(/^\|\s*(SC-\d{2})\s*\|/gm)) defined.add(m[1]);

const ID_RE = /\b(?:REQ|NFR|ADR)-\d{3}\b|\bSC-\d{2}\b/g;

// ---------- 2. ID yang disebut harus ada ----------
const scanFiles = [
  ...walk(join(root, 'docs'), (p) => p.endsWith('.md')),
  ...walk(join(root, 'specs'), (p) => p.endsWith('.md') && !/\/_template\./.test(rel(p))),
  ...walk(join(root, 'api/src'), (p) => p.endsWith('.js')),
  ...walk(join(root, 'api/tests'), (p) => p.endsWith('.js')),
  ...walk(join(root, 'web/app')),
  ...walk(join(root, 'web/components')),
  ...walk(join(root, 'web/lib')),
];
for (const f of scanFiles) {
  const text = read(f);
  for (const id of new Set(text.match(ID_RE) ?? [])) {
    if (!defined.has(id)) fail(rel(f), `${id} tidak ada di PRD, ARD, atau standar (ID karangan atau salah ketik)`);
  }
}

// ---------- 3. Spec dan plan ----------
function section(text, headingPattern) {
  const lines = text.split('\n');
  const start = lines.findIndex((l) => /^##\s/.test(l) && headingPattern.test(l));
  if (start === -1) return null;
  const body = [];
  for (let i = start + 1; i < lines.length && !/^##\s/.test(lines[i]); i++) body.push(lines[i]);
  return body;
}
function deviationOk(body) {
  const first = body
    .map((l) => l.trim())
    .find((l) => l && !l.startsWith('>') && !l.startsWith('<!--'));
  return Boolean(first && /^[-*]?\s*\**\s*tidak ada\b/i.test(first));
}

const specFiles = walk(join(root, 'specs'), (p) => p.endsWith('.spec.md') && !/\/_template\./.test(rel(p)));
const planFiles = walk(join(root, 'specs'), (p) => p.endsWith('.plan.md') && !/\/_template\./.test(rel(p)));

for (const kind of [
  { files: specFiles, need: /\b(?:REQ|NFR)-\d{3}\b/, needMsg: 'baris `Mengacu:` dengan minimal satu REQ atau NFR dari docs/prd.md' },
  { files: planFiles, need: /\bADR-\d{3}\b/, needMsg: 'baris `Mengacu:` dengan minimal satu ADR dari docs/ard.md' },
]) {
  for (const f of kind.files) {
    const text = read(f);
    const ref = text.split('\n').find((l) => /^\*{0,2}Mengacu\*{0,2}\s*:/i.test(l.replace(/^[>\s-]+/, '')));
    if (!ref || !kind.need.test(ref)) fail(rel(f), `tidak punya ${kind.needMsg}`);
    const dev = section(text, /Penyimpangan dari PRD\/ARD/i);
    if (!dev) fail(rel(f), 'tidak punya bagian "Penyimpangan dari PRD/ARD"');
    else if (!deviationOk(dev)) {
      fail(rel(f), 'ada penyimpangan dari PRD/ARD yang belum selesai. Berhenti: manusia memutuskan, mengubah PRD/ARD bila disetujui, lalu bagian ini diisi "Tidak ada".');
    }
  }
}

// ---------- 4. Persyaratan Selesai harus punya tes ----------
const testFiles = [
  ...walk(join(root, 'api/tests'), (p) => p.endsWith('.js')),
  ...walk(join(root, 'web'), (p) => /\.(test|spec)\.[jt]sx?$/.test(p)),
];
const testText = testFiles.map(read).join('\n');
for (const [id, status] of reqStatus) {
  if (/^selesai$/i.test(status) && !testText.includes(id)) {
    fail('docs/prd.md', `${id} berstatus Selesai tetapi tidak ada tes yang menyebut ID-nya (tulis [${id}] di nama tes, atau ubah status).`);
  }
}

// ---------- 5. Allowlist dependensi ----------
const allow = JSON.parse(read(docs.deps)).packages;
for (const scope of ['api', 'web']) {
  const pj = join(root, scope, 'package.json');
  if (!existsSync(pj)) continue;
  const pkg = JSON.parse(read(pj));
  const allowed = new Set(allow.filter((a) => a.scope === scope).map((a) => a.name));
  for (const field of ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies']) {
    for (const name of Object.keys(pkg[field] ?? {})) {
      if (!allowed.has(name)) {
        fail(`${scope}/package.json`, `paket "${name}" tidak ada di docs/dependencies.json (ADR-007, SC-11). Minta manusia menambahkannya setelah plan disetujui.`);
      }
    }
  }
}
const rootPkg = JSON.parse(read(join(root, 'package.json')));
for (const field of ['dependencies', 'devDependencies']) {
  for (const name of Object.keys(rootPkg[field] ?? {})) {
    if (!allow.some((a) => a.scope === 'root' && a.name === name)) {
      fail('package.json', `paket "${name}" di root tidak ada di docs/dependencies.json (scope "root").`);
    }
  }
}

// ---------- 6. Pola rahasia (heuristik) ----------
// Bisa meleset (positif palsu dan negatif palsu). Ini jaring tambahan, bukan pengganti tinjauan.
// Untuk positif palsu yang sah, tambahkan komentar `compliance-ignore: alasan` pada baris yang sama.
const SECRET_PATTERNS = [
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, 'kunci privat'],
  [/\bAKIA[0-9A-Z]{16}\b/, 'kunci akses AWS'],
  [/\bgh[pousr]_[A-Za-z0-9]{36,}\b/, 'token GitHub'],
  [/\bsk-[A-Za-z0-9_-]{20,}\b/, 'kunci API bergaya sk-'],
  [/\b(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['"][^'"\s]{8,}['"]/i, 'rahasia yang ditulis langsung'],
];
const codeFiles = [
  ...walk(join(root, 'api/src'), (p) => p.endsWith('.js')),
  ...walk(join(root, 'api/tests'), (p) => p.endsWith('.js')),
  ...walk(join(root, 'web/app')),
  ...walk(join(root, 'web/components')),
  ...walk(join(root, 'web/lib')),
];
for (const f of codeFiles) {
  read(f)
    .split('\n')
    .forEach((line, i) => {
      if (line.includes('compliance-ignore')) return;
      for (const [re, label] of SECRET_PATTERNS) {
        if (re.test(line)) fail(`${rel(f)}:${i + 1}`, `dicurigai ${label} (SC-07). Pindahkan ke variabel lingkungan lewat src/config/.`);
      }
    });
}
if (existsSync(join(root, '.gitignore')) && !/^\.env$/m.test(read(join(root, '.gitignore')))) {
  fail('.gitignore', '`.env` belum diabaikan Git (SC-07).');
}

// ---------- 7. Berkas yang dilindungi tidak berubah tanpa persetujuan ----------
const approvalPath = join(root, 'docs/persetujuan.sha256');
if (!existsSync(approvalPath)) {
  fail('docs/persetujuan.sha256', 'catatan persetujuan tidak ada. Manusia menjalankan `npm run docs:setujui`.');
} else {
  const tercatat = new Map(
    read(approvalPath)
      // \r?\n: berkas bisa ber-CRLF bila Git di Windows memakai core.autocrlf=true.
      .split(/\r?\n/)
      .map((l) => l.trim())
      .filter(Boolean)
      .map((l) => {
        const [hash, ...path] = l.split(/\s+/);
        return [path.join(' '), hash];
      }),
  );
  for (const path of DILINDUNGI) {
    if (!existsSync(join(root, path))) fail(path, 'berkas yang dilindungi tidak ada.');
    else if (tercatat.get(path) !== hashBerkas(root, path)) {
      fail(path, 'berubah sejak persetujuan terakhir. Jika perubahan ini disetujui manusia, MANUSIA menjalankan `npm run docs:setujui`. Claude tidak menjalankannya.');
    }
  }
}

finish();

function finish() {
  if (problems.length) {
    console.error(`Pemeriksaan kepatuhan GAGAL (${problems.length} masalah):\n`);
    for (const p of problems) console.error(` - ${p}`);
    console.error('\nJangan melonggarkan pemeriksaan ini. Perbaiki kodenya, atau minta manusia mengubah PRD/ARD/standar.');
    process.exit(1);
  }
  console.info(
    `Kepatuhan OK: ${defined.size} ID terdefinisi, ${specFiles.length} spec, ${planFiles.length} plan, ` +
      `${[...reqStatus.values()].filter((s) => /^selesai$/i.test(s)).length} persyaratan Selesai bertes.`,
  );
}
