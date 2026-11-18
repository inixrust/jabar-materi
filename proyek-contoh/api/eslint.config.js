import js from '@eslint/js';
import globals from 'globals';
import { defineConfig, globalIgnores } from 'eslint/config';

// Aturan di sini adalah PENEGAKAN. CLAUDE.md hanya konteks yang bisa terlewat,
// sedangkan lint ini gagal otomatis jika aturan dilanggar.
export default defineConfig([
  globalIgnores(['node_modules/**']),
  {
    files: ['**/*.js'],
    extends: [js.configs.recommended],
    languageOptions: { globals: globals.node },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],

      // Konfigurasi hanya dibaca lewat src/config/ (lihat override di bawah).
      'no-restricted-properties': [
        'error',
        {
          object: 'process',
          property: 'env',
          message: 'Baca konfigurasi lewat src/config/index.js, bukan process.env langsung.',
        },
      ],

      // Hindari mencatat data sembarangan. console.error/warn/info masih boleh (error handler dan log startup).
      'no-console': ['error', { allow: ['error', 'warn', 'info'] }],

      // Larang eval dan sejenisnya (SC-03).
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',

      // SC-03: tanpa menjalankan perintah shell dari kode aplikasi.
      'no-restricted-imports': [
        'error',
        {
          paths: [
            { name: 'child_process', message: 'child_process dilarang (SC-03, injeksi perintah).' },
            { name: 'node:child_process', message: 'child_process dilarang (SC-03, injeksi perintah).' },
          ],
        },
      ],

      'no-restricted-syntax': [
        'error',
        {
          // SC-06: nilai acak untuk keamanan berasal dari node:crypto.
          selector: "MemberExpression[object.name='Math'][property.name='random']",
          message: 'Math.random tidak aman untuk token atau rahasia. Pakai node:crypto (SC-06).',
        },
        {
          // SC-08: CORS dengan daftar asal eksplisit.
          selector: "CallExpression[callee.name='cors'] Property[key.name='origin'][value.value='*']",
          message: "CORS dengan origin '*' dilarang. Pakai config.corsOrigins (SC-08).",
        },
        {
          selector: "CallExpression[callee.name='cors'] Property[key.name='origin'][value.value=true]",
          message: 'CORS yang memantulkan semua asal dilarang. Pakai config.corsOrigins (SC-08).',
        },
      ],
    },
  },
  {
    // Satu-satunya tempat yang boleh membaca process.env.
    files: ['src/config/**/*.js'],
    rules: { 'no-restricted-properties': 'off' },
  },
]);
