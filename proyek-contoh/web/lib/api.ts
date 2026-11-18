// Klien API. Dipanggil dari komponen server dan Server Action, jadi API_URL tidak dikirim ke browser.
const API_URL = process.env.API_URL ?? 'http://localhost:4000';

type Health = { status: string; time: string };

export type Note = { id: string; title: string; body: string; createdAt: string };

export type NoteField = 'title' | 'body';

export type CreateNoteResult =
  | { ok: true; note: Note }
  | { ok: false; message: string; fieldErrors: Partial<Record<NoteField, string>> };

type ApiError = {
  error?: { code?: string; message?: string; details?: { path?: string; message?: string }[] };
};

export async function getHealth(): Promise<Health | null> {
  try {
    const res = await fetch(`${API_URL}/api/health`, { cache: 'no-store' });
    if (!res.ok) return null;
    const body = (await res.json()) as { data?: Health };
    return body.data ?? null;
  } catch {
    return null;
  }
}

// Mengembalikan null bila API tidak dapat dihubungi atau membalas error,
// supaya halaman menampilkan keadaan error (pola yang sama dengan getHealth).
export async function getNotes(): Promise<Note[] | null> {
  try {
    const res = await fetch(`${API_URL}/api/notes`, { cache: 'no-store' });
    if (!res.ok) return null;
    const body = (await res.json()) as { data?: Note[] };
    return Array.isArray(body.data) ? body.data : null;
  } catch {
    return null;
  }
}

// Validasi yang menentukan ada di API (SC-02). Pesan error per field diteruskan ke formulir.
export async function createNote(input: { title: string; body: string }): Promise<CreateNoteResult> {
  try {
    const res = await fetch(`${API_URL}/api/notes`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(input),
      cache: 'no-store',
    });
    if (res.ok) {
      const body = (await res.json()) as { data: Note };
      return { ok: true, note: body.data };
    }

    const body = (await res.json().catch(() => ({}))) as ApiError;
    const fieldErrors: Partial<Record<NoteField, string>> = {};
    for (const detail of body.error?.details ?? []) {
      if ((detail.path === 'title' || detail.path === 'body') && detail.message && !fieldErrors[detail.path]) {
        fieldErrors[detail.path] = detail.message;
      }
    }
    const message =
      res.status === 400 ? 'Periksa kembali isian yang ditandai.' : 'Catatan gagal disimpan. Coba lagi.';
    return { ok: false, message, fieldErrors };
  } catch {
    return { ok: false, message: 'API tidak dapat dihubungi. Catatan belum tersimpan.', fieldErrors: {} };
  }
}
