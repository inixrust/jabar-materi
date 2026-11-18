# ARD: Catatan Tim (Architecture Decision Record)

| | |
|---|---|
| Versi | 1.0 |
| Status | Disetujui (contoh pelatihan) |
| Pemilik | Tech lead |
| Perubahan | **Hanya oleh manusia**, lewat proses di bagian 3. Claude tidak mengubah berkas ini. |

> Berkas ini adalah **sumber kebenaran tentang BAGAIMANA** sistem dibangun: keputusan arsitektur
> yang sudah diambil beserta alasannya. Setiap plan harus mematuhinya dan menyebut ID
> keputusannya (`ADR-`). Jika sebuah tugas lebih mudah dikerjakan dengan melanggar sebuah
> keputusan, itu tanda untuk berhenti dan mengusulkan ADR baru, bukan alasan untuk menyimpang.

Status keputusan: `Berlaku`, `Diputuskan` (sudah disetujui, belum dibangun), `Digantikan`.

## 1. Gambaran

```
Browser ──▶ web (Next.js, :3000) ──▶ api (Express, :4000) ──▶ db/memory-store (Fase 1)
```

## 2. Keputusan

### ADR-001 Monorepo npm workspaces: `api/` dan `web/` — Berlaku
- **Keputusan:** satu repositori, dua workspace. Dependensi dipasang dari root.
- **Alasan:** satu alur kerja dan satu tempat untuk lint, tes, dan pemeriksaan kepatuhan.
- **Konsekuensi:** `api/` dan `web/` tidak saling mengimpor kode. Mereka hanya berbicara lewat HTTP.

### ADR-002 API berlapis: rute → controller → service → skema — Berlaku
- **Keputusan:** Express 5, JavaScript ESM. Rute tipis, controller membentuk respons, service memegang
  logika bisnis, skema zod memvalidasi input. Lapisan tidak dilompati.
- **Alasan:** pola tunggal yang mudah dites dan ditiru (lihat `health.*`).
- **Konsekuensi:** controller dan rute tidak mengakses `db/` langsung. Logika bisnis tidak di berkas rute.

### ADR-003 Validasi ketat di tepi — Berlaku
- **Keputusan:** body, query, dan params divalidasi dengan zod (`z.strictObject`) lewat middleware
  `validate` sebelum controller. Input yang salah ditolak dengan 400, tidak dibersihkan diam-diam.
- **Alasan:** mencegah mass assignment dan data tak terduga masuk ke logika bisnis.

### ADR-004 Penyimpanan di balik service — Berlaku (sementara)
- **Keputusan:** Fase 1 memakai `src/db/memory-store.js`, hanya diakses dari service.
- **Alasan:** cukup untuk latihan dan memudahkan penggantian.
- **Konsekuensi:** data hilang saat restart (NFR-005). Memilih basis data permanen memerlukan ADR baru,
  termasuk keputusan enkripsi, pencadangan, dan akses.

### ADR-005 Konfigurasi dan rahasia hanya lewat `src/config/` — Berlaku
- **Keputusan:** hanya `src/config/` yang membaca `process.env`. Rahasia tidak ada di kode,
  log, atau respons. `.env` tidak masuk Git.
- **Penegakan:** aturan lint `no-restricted-properties`.

### ADR-006 Web: Next.js App Router, TypeScript strict, UI berbasis token — Berlaku
- **Keputusan:** komponen server secara default. UI hanya dari `components/ui/` dan design token
  (`styles/tokens.css`). Akses ke API lewat `lib/api.ts` dari sisi server. `API_URL` tidak di `NEXT_PUBLIC_*`.
- **Penegakan:** lint (hex, `style`, `dangerouslySetInnerHTML`) dan `scripts/check-tokens.mjs`.

### ADR-007 Dependensi dibatasi allowlist — Berlaku
- **Keputusan:** paket yang boleh dipakai ada di `docs/dependencies.json`. Menambah paket berarti
  manusia memperbarui allowlist (dan ADR bila perlu) lebih dulu.
- **Alasan:** mengurangi risiko rantai pasok perangkat lunak, termasuk paket dengan nama
  menyesatkan yang disarankan AI (OWASP Top 10:2025 A03).
- **Penegakan:** `npm run check:compliance`.

### ADR-008 Format respons dan kode status — Berlaku
- **Keputusan:** sukses `{ data }`, gagal `{ error: { code, message } }`. 201 dibuat, 204 dihapus,
  400 input salah, 401 belum masuk, 403 dilarang, 404 tidak ada. Detail internal hanya di log server.

### ADR-009 Baseline keamanan HTTP — Berlaku
- **Keputusan:** `helmet`, CORS dengan daftar asal eksplisit (bukan `*`), rate limit 100 per menit
  per IP, batas body 100 KB, `x-powered-by` mati.
- **Konsekuensi:** pengaturan di `src/app.js` tidak dilonggarkan tanpa ADR.

### ADR-010 Autentikasi Fase 2: magic link dengan sesi di server — Diputuskan (belum dibangun)
- **Keputusan:**
  - Tautan masuk berisi token acak dari CSPRNG (`node:crypto`), sekali pakai, berbatas waktu,
    disimpan **dalam bentuk hash**.
  - Tautan dibuka lewat halaman yang melakukan verifikasi dengan **POST** (agar pemindai email
    tidak menghabiskan token). Token tidak memuat parameter pengalihan bebas.
  - Sesi disimpan di server. Browser hanya membawa cookie acak dengan `HttpOnly`, `Secure`, `SameSite`.
  - **Tidak memakai JWT** dan tidak menyimpan token atau sesi di `localStorage` atau `sessionStorage`.
  - Pesan respons sama untuk email terdaftar dan tidak terdaftar. Permintaan tautan dibatasi lajunya.
- **Alasan:** mengurangi permukaan serangan dan menjaga sesi bisa dicabut dari server.
- **Konsekuensi:** pustaka email dan penyimpanan sesi memerlukan pembaruan allowlist (ADR-007).

## 3. Proses perubahan ARD

1. Pengusul menulis ADR baru atau usulan penggantian (konteks, keputusan, alasan, konsekuensi).
2. Tech lead menyetujui. Jika menyentuh persyaratan, PRD ikut diubah oleh product owner.
3. **Manusia** mengubah berkas ini dan menaikkan versi.
4. Baru setelah itu plan dan kode boleh mengikuti.

| Versi | Tanggal | Perubahan | Disetujui oleh |
|---|---|---|---|
| 1.0 | Hari pelatihan | Versi awal (contoh) | Tech lead |
