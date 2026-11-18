#!/usr/bin/env node
// Hook PreToolUse untuk Bash (versi Node, tanpa jq, jalan di Windows/macOS/Linux).
// Jika perintah adalah pelari tes, keluarannya disaring agar hanya ringkasan dan kegagalan
// yang masuk ke konteks Claude. Mengurangi token tanpa menyembunyikan kegagalan.
//
// Disesuaikan untuk `node --test` (reporter spec: ✖ / ℹ, reporter TAP: not ok / #).
// Untuk pelari lain, ubah COMMAND_PATTERN dan FILTER di bawah.
//
// Daftarkan di .claude/settings.local.json (pribadi) atau ~/.claude/settings.json:
//   { "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [
//       { "type": "command", "command": "node .claude/hooks/filter-test-output.mjs" } ] } ] } }

// Hanya perintah tes sederhana: tanpa ; & | < > ` $ \ agar tidak membungkus perintah majemuk.
const COMMAND_PATTERN = /^npm (?:test|run test)(?: [^;&|<>`$\\]*)?$/;

// pipefail: kode keluar tetap milik `npm test`, jadi Claude tahu bila tes gagal.
// awk: cetak ringkasan, baris tes gagal, pesan assert, dan semua baris setelah "failing tests".
const FILTER =
  " 2>&1 | awk '/^✖ failing tests:/{f=1} f || /^(not ok|ℹ (tests|pass|fail) |# (tests|pass|fail) )/ || /^ +(AssertionError|Error|expected|actual)/' | head -80";

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => (raw += chunk));
process.stdin.on('end', () => {
  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.stdout.write('{}');
    return;
  }
  const command = input?.tool_input?.command;
  if (typeof command !== 'string' || !COMMAND_PATTERN.test(command.trim())) {
    process.stdout.write('{}');
    return;
  }
  const output = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      updatedInput: { ...input.tool_input, command: `set -o pipefail; ${command.trim()}${FILTER}` },
    },
  };
  process.stdout.write(JSON.stringify(output));
});
