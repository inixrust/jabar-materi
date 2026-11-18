import { Suspense } from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { NoteForm } from '@/components/catatan/NoteForm';
import { NoteList } from '@/components/catatan/NoteList';
import { RetryButton } from '@/components/catatan/RetryButton';
import { getNotes } from '@/lib/api';
import styles from '@/components/catatan/Catatan.module.css';

export const metadata: Metadata = {
  title: 'Catatan · Catatan Tim',
};

// Komponen server yang mengambil data. Tiga keadaan: error (API tidak terhubung), kosong, berisi.
async function DaftarCatatan() {
  const notes = await getNotes();

  if (notes === null) {
    return (
      <>
        <p>Daftar catatan tidak dapat dimuat karena API belum terhubung.</p>
        <RetryButton />
      </>
    );
  }
  if (notes.length === 0) {
    return <p className={styles.empty}>Belum ada catatan. Tambahkan catatan pertama lewat formulir di atas.</p>;
  }
  return <NoteList notes={notes} />;
}

// Formulir tampil langsung; hanya daftar yang menunggu data (keadaan loading lewat Suspense).
export default function CatatanPage() {
  return (
    <main className="container">
      <h1>Catatan</h1>
      <p>
        <Link href="/">Kembali ke beranda</Link>
      </p>

      <Card title="Tambah catatan">
        <NoteForm />
      </Card>

      <Card title="Daftar catatan">
        <Suspense fallback={<p role="status">Memuat catatan…</p>}>
          <DaftarCatatan />
        </Suspense>
      </Card>
    </main>
  );
}
