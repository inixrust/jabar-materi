'use client';

import { useActionState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { createNoteAction } from '@/app/catatan/actions';
import type { NoteFormState } from '@/app/catatan/actions';
import styles from './Catatan.module.css';

const initialState: NoteFormState = {
  status: 'idle',
  message: '',
  fieldErrors: {},
  values: { title: '', body: '' },
};

export function NoteForm() {
  const [state, formAction, pending] = useActionState(createNoteAction, initialState);

  return (
    <form action={formAction}>
      {/* key: setiap hasil baru memasang ulang field dengan nilai dari state, jadi isian
          tetap ada saat gagal dan kosong kembali saat berhasil. */}
      <div key={JSON.stringify(state.values) + state.status}>
        <Input
          label="Judul"
          name="title"
          required
          maxLength={100}
          defaultValue={state.values.title}
          error={state.fieldErrors.title}
        />
        <Textarea
          label="Isi (opsional)"
          name="body"
          maxLength={5000}
          defaultValue={state.values.body}
          error={state.fieldErrors.body}
        />
      </div>
      <p className={styles.hint}>
        Catatan disimpan sementara dan hilang saat API dimulai ulang. Jangan menulis data pribadi atau rahasia.
      </p>
      <p
        role="status"
        aria-live="polite"
        className={state.status === 'error' ? styles.errorMessage : styles.successMessage}
      >
        {state.message}
      </p>
      <Button type="submit" disabled={pending}>
        {pending ? 'Menyimpan…' : 'Simpan catatan'}
      </Button>
    </form>
  );
}
