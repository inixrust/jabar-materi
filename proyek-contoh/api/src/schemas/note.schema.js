import { z } from 'zod';

// REQ-010: judul wajib, tidak boleh kosong atau hanya spasi, maksimum 100 karakter.
// Judul tidak dipangkas: server menolak, bukan mengubah diam-diam (ADR-003).
const title = z
  .string()
  .max(100, 'Judul maksimum 100 karakter.')
  .refine((value) => value.trim().length > 0, 'Judul tidak boleh kosong.');

const body = z.string().max(5000, 'Isi maksimum 5000 karakter.');

// z.strictObject menolak kolom tak dikenal, termasuk id dan createdAt (REQ-014, SC-14).
export const createNoteSchema = z.strictObject({
  title,
  body: body.default(''),
});

export const updateNoteSchema = z
  .strictObject({
    title: title.optional(),
    body: body.optional(),
  })
  .refine((data) => data.title !== undefined || data.body !== undefined, {
    message: 'Kirim minimal satu kolom: title atau body.',
  });

export const noteParamsSchema = z.strictObject({
  id: z.uuid('id harus berupa UUID.'),
});
