# -*- coding: utf-8 -*-
"""Dasar teori per slide: baris bawah slide (8,5 pt) + speaker notes (SUMBER).
Kunci = judul slide PERSIS (ganti judul -> ganti kunci). Hanya sumber resmi dan pakar; <= 84 huruf agar 8,5 pt."""
CC = 'Claude Code Docs'
SRC = {
    # Modul 1
    'Proyek contoh: Catatan Tim': 'proyek-contoh/README.md; docs/prd.md dan docs/ard.md proyek contoh',
    'Agent versus autocomplete': f'{CC}: Overview; Anthropic, "Building effective agents" (2024)',
    'Hasil meleset karena maksud belum tertulis': 'Anthropic, "Claude Code: Best practices for agentic coding" (2025)',
    'Konteks: @-mention, seleksi, dan diff': f'{CC}: VS Code integration; Common workflows',
    'Titik aman sebelum agent bekerja': f'{CC}: Checkpointing (/rewind); Git documentation: git-restore',
    'Anatomi prompt spesifik': 'Anthropic, "Claude Code: Best practices for agentic coding" (2025)',
    # Modul 2
    'Rantai spec, plan, dan kode': f'{CC}: Common workflows (plan mode); panduan-lab/lab-02-spec-plan.md',
    'Dokumen lebih murah diubah daripada kode': 'B. Boehm, Software Engineering Economics (1981): biaya perubahan per fase',
    'Plan mode: rencana dulu, ubah kemudian': f'{CC}: Common workflows, "Use Plan Mode for safe code analysis"',
    'Perbaiki di lapisan yang benar': f'{CC}: Checkpointing; panduan-lab/lab-02-spec-plan.md',
    'Keputusan teknis di skema Catatan': 'Zod Docs: strictObject, refine; proyek-contoh docs/prd.md REQ-010',
    # Modul 3
    'Seluruh percakapan dikirim ulang': 'Anthropic Docs: Context windows; ' + f'{CC}: Manage costs effectively',
    'Kebiasaan hemat: /clear dan /compact': f'{CC}: Manage costs effectively; Slash commands',
    'Kebiasaan hemat dan perintahnya': f'{CC}: Slash commands; Manage costs effectively',
    'Model dan effort sesuai tugas': f'{CC}: Model configuration; Manage costs effectively',
    'Mengurangi beban konteks': f'{CC}: MCP; Hooks; Agent Skills',
    'Hook penyaring keluaran tes': f'{CC}: Hooks reference, PreToolUse dan updatedInput',
    'Target verifikasi memangkas perbaikan': 'Anthropic, "Claude Code: Best practices for agentic coding" (2025)',
    'Temuan Lab 3: error 429 harus JSON': 'express-rate-limit Docs: message; proyek-contoh docs/prd.md NFR-002',
    # Modul 4
    'CLAUDE.md dimuat di awal sesi': f'{CC}: Manage Claude\'s memory (CLAUDE.md, /init, rules)',
    'CLAUDE.md dan AGENTS.md': f'{CC}: Memory, impor @path; Next.js 16 Docs: error.js',
    'Aturan yang efektif': f'{CC}: Memory, "Memory best practices"',
    'CLAUDE.md root yang bisa diikuti': f'{CC}: Memory; proyek-contoh/CLAUDE.md (solusi Lab 4a)',
    'Aturan berpath di .claude/rules': f'{CC}: Memory, path-specific rules (.claude/rules)',
    'Aturan berpath yang salah gagal diam-diam': f'{CC}: Memory, path-specific rules; catatan-instruktur.md',
    'Standar UI yang bisa dicek': 'W3C, WCAG 2.2; proyek-contoh .claude/rules/frontend-ui.md',
    'Standar keamanan berbasis OWASP': 'OWASP Top 10:2025; OWASP ASVS 5.0; docs/standar-secure-coding.md',
    'Konteks bukan penegak': f'{CC}: Memory; Hooks; Settings (permissions)',
    'Lapisan penegakan di proyek ini': 'panduan-lab/lab-04-claude-md.md, tabel lapisan penegakan',
    'Penegak mesin: aturan lint': 'ESLint Docs: no-restricted-properties, no-restricted-imports',
    # Modul 5
    'Agent utama dan subagent': f'{CC}: Subagents',
    'Berkas subagent': f'{CC}: Subagents, "File format" dan "Configuration fields"',
    'Urutan penentuan model subagent': f'{CC}: Subagents, "Model selection"',
    'Matriks model per jenis tugas': 'proyek-contoh docs/standarisasi.md bagian 2-4 (solusi Lab 5)',
    'Kriteria kompleksitas K1–K4': 'proyek-contoh docs/standarisasi.md bagian 5 (solusi Lab 5)',
    'Kapan mendelegasikan': f'{CC}: Subagents; docs/standarisasi.md bagian 6-7',
    # Modul 6
    'Capstone: satu fitur, semua standar': 'panduan-lab/lab-06-capstone.md; proyek-contoh docs/prd.md REQ-020',
    'error.tsx di Next.js 16.4': 'Next.js 16 Docs: error.js (node_modules/next/dist/docs)',
    'Mengukur dampak standar': 'panduan-lab/lab-06-capstone.md langkah 4; docs/lembar-pencatatan-token.md',
}
