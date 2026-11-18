'use client';

import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';

// Batas error untuk kesalahan tak terduga saat merender halaman.
// Next.js 16.4 memberi `retry` (bukan `reset`) dan `error` bertipe unknown.
// Detail error tidak ditampilkan ke pengguna (SC-09).
export default function CatatanError({ retry }: { error: unknown; retry: () => void }) {
  return (
    <main className="container">
      <h1>Catatan</h1>
      <Card title="Terjadi kesalahan">
        <p>Halaman catatan gagal ditampilkan.</p>
        <Button variant="secondary" onClick={() => retry()}>
          Coba lagi
        </Button>
      </Card>
    </main>
  );
}
