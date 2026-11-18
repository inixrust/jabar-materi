import { createCollection } from '../db/memory-store.js';
import { HttpError } from '../middlewares/error-handler.js';

// ADR-004: hanya service yang mengakses penyimpanan.
const notes = createCollection();

// SC-12: respons hanya memuat kolom catatan yang dikenal, bukan objek penyimpanan mentah.
function toNote({ id, title, body, createdAt }) {
  return { id, title, body, createdAt };
}

function notFound() {
  return new HttpError(404, 'NOTE_NOT_FOUND', 'Catatan tidak ditemukan.');
}

export const noteService = {
  list() {
    return notes.list().map(toNote);
  },

  getById(id) {
    const note = notes.get(id);
    if (!note) throw notFound();
    return toNote(note);
  },

  create({ title, body }) {
    return toNote(notes.create({ title, body }));
  },

  update(id, changes) {
    const patch = {};
    if (changes.title !== undefined) patch.title = changes.title;
    if (changes.body !== undefined) patch.body = changes.body;

    const note = notes.update(id, patch);
    if (!note) throw notFound();
    return toNote(note);
  },

  remove(id) {
    if (!notes.remove(id)) throw notFound();
  },
};
