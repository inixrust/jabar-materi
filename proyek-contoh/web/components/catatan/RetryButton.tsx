'use client';

import { useRouter } from 'next/navigation';
import { useTransition } from 'react';
import { Button } from '@/components/ui/Button';

// Memuat ulang data halaman dari server tanpa memuat ulang seluruh browser.
export function RetryButton() {
  const router = useRouter();
  const [pending, startTransition] = useTransition();

  return (
    <Button variant="secondary" disabled={pending} onClick={() => startTransition(() => router.refresh())}>
      {pending ? 'Memuat…' : 'Coba lagi'}
    </Button>
  );
}
