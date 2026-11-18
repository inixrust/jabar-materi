// Pemeriksa design token untuk berkas CSS: warna harus dari var(--...), bukan ditulis langsung.
// Dijalankan oleh `npm run lint`. Berkas styles/tokens.css dikecualikan karena itulah sumbernya.
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const skipDirs = new Set(['node_modules', '.next']);
const allowed = join('styles', 'tokens.css');
const colorPattern = /#[0-9a-fA-F]{3,8}\b|\b(?:rgb|rgba|hsl|hsla)\(/;

function* cssFiles(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!skipDirs.has(entry.name)) yield* cssFiles(join(dir, entry.name));
    } else if (entry.name.endsWith('.css')) {
      yield join(dir, entry.name);
    }
  }
}

const problems = [];
for (const file of cssFiles(root)) {
  const rel = relative(root, file);
  if (rel.split(sep).join('/') === allowed.split(sep).join('/')) continue;
  readFileSync(file, 'utf8')
    .split('\n')
    .forEach((line, i) => {
      if (colorPattern.test(line)) problems.push(`${rel}:${i + 1}  ${line.trim()}`);
    });
}

if (problems.length > 0) {
  console.error('Warna ditulis langsung. Pakai design token (var(--color-...)):');
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}
console.log('Pemeriksa token CSS: bersih.');
