import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { getHealth } from '@/lib/api';

export default async function HomePage() {
  const health = await getHealth();

  return (
    <main className="container">
      <h1>Catatan Tim</h1>
      <p>
        Kerangka proyek pelatihan Developing dengan AI. Mulailah dengan meminta Claude
        menjelaskan struktur proyek ini.
      </p>
      <p>
        <Link href="/catatan">Buka halaman Catatan</Link>
      </p>
      <Card title="Status API">
        {health ? (
          <p>API berjalan: {health.status}</p>
        ) : (
          <p>
            API belum terhubung. Jalankan <code>npm run dev:api</code> di terminal lain.
          </p>
        )}
      </Card>
    </main>
  );
}
