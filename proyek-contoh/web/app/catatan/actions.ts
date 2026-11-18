'use server';

import { revalidatePath } from 'next/cache';
import { createNote } from '@/lib/api';
import type { NoteField } from '@/lib/api';

export type NoteFormState = {
  status: 'idle' | 'success' | 'error';
  message: string;
  fieldErrors: Partial<Record<NoteField, string>>;
  // Nilai yang dikirim, dikembalikan saat gagal agar isian pengguna tidak hilang.
  values: { title: string; body: string };
};

export async function createNoteAction(_prev: NoteFormState, formData: FormData): Promise<NoteFormState> {
  const title = formData.get('title');
  const body = formData.get('body') ?? '';

  // Hanya memastikan tipe. Aturan isi (kosong, panjang) divalidasi API dengan zod (SC-02).
  if (typeof title !== 'string' || typeof body !== 'string') {
    return {
      status: 'error',
      message: 'Isian tidak valid.',
      fieldErrors: {},
      values: { title: '', body: '' },
    };
  }

  const result = await createNote({ title, body });
  if (!result.ok) {
    return { status: 'error', message: result.message, fieldErrors: result.fieldErrors, values: { title, body } };
  }

  revalidatePath('/catatan');
  return { status: 'success', message: 'Catatan tersimpan.', fieldErrors: {}, values: { title: '', body: '' } };
}
