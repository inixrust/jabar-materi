import { defineConfig, globalIgnores } from 'eslint/config';
import tseslint from 'typescript-eslint';

// Aturan di sini adalah PENEGAKAN. CLAUDE.md hanya konteks yang bisa terlewat,
// sedangkan lint ini gagal otomatis jika aturan dilanggar.
export default defineConfig([
  globalIgnores(['.next/**', 'node_modules/**', 'next-env.d.ts']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [tseslint.configs.recommended],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: "Literal[value=/^#[0-9a-fA-F]{3,8}$/]",
          message: 'Jangan menulis warna hex langsung. Pakai design token (var(--color-...)).',
        },
        {
          selector: "JSXAttribute[name.name='style']",
          message: 'Jangan memakai gaya inline. Pakai CSS Modules dan design token.',
        },
        {
          selector: "JSXAttribute[name.name='dangerouslySetInnerHTML']",
          message: 'dangerouslySetInnerHTML dilarang (risiko XSS, SC-03 dan SC-15).',
        },
        {
          selector: "Identifier[name='localStorage']",
          message: 'localStorage dilarang untuk token atau sesi. Sesi ada di server dengan cookie HttpOnly (SC-05, ADR-010).',
        },
        {
          selector: "Identifier[name='sessionStorage']",
          message: 'sessionStorage dilarang untuk token atau sesi. Sesi ada di server dengan cookie HttpOnly (SC-05, ADR-010).',
        },
        {
          selector: "MemberExpression[object.name='document'][property.name='cookie']",
          message: 'Cookie sesi diatur server (HttpOnly), bukan dari JavaScript klien (SC-05).',
        },
      ],
    },
  },
]);
