#!/usr/bin/env node
// Dijalankan MANUSIA setelah menyetujui perubahan pada dokumen sumber kebenaran atau konfigurasi penegakan.
// Menulis ulang docs/persetujuan.sha256. `npm run check:compliance` gagal bila salah satu berkas
// berubah tanpa langkah ini, sehingga perubahan yang tidak disengaja (termasuk lewat skrip) ketahuan.
//
// Ini jaring pengaman terhadap kelalaian, bukan penghalang mutlak: siapa pun yang bisa menjalankan
// perintah ini bisa menyetujui. Karena itu perintah ini tidak boleh dijalankan oleh Claude.
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const DILINDUNGI = [
  'docs/prd.md',
  'docs/ard.md',
  'docs/standar-secure-coding.md',
  'docs/dependencies.json',
  'api/eslint.config.js',
  'web/eslint.config.mjs',
  'web/scripts/check-tokens.mjs',
  'scripts/check-compliance.mjs',
  '.claude/settings.json',
  'scripts/setujui-dokumen.mjs',
];

// Akhir baris CRLF dan LF dianggap sama agar hash stabil di Windows dan Linux.
export function hashBerkas(root, path) {
  const isi = readFileSync(join(root, path), 'utf8').replace(/\r\n/g, '\n');
  return createHash('sha256').update(isi).digest('hex');
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const root = join(fileURLToPath(new URL('.', import.meta.url)), '..');
  const baris = DILINDUNGI.map((p) => `${hashBerkas(root, p)}  ${p}`);
  writeFileSync(join(root, 'docs/persetujuan.sha256'), baris.join('\n') + '\n');
  console.info(`Persetujuan dicatat untuk ${DILINDUNGI.length} berkas (docs/persetujuan.sha256).`);
}
