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

      // Larang eval dan sejenisnya.
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',
    },
  },
  {
    // Satu-satunya tempat yang boleh membaca process.env.
    files: ['src/config/**/*.js'],
    rules: { 'no-restricted-properties': 'off' },
  },
]);
