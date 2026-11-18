import { randomUUID } from 'node:crypto';

// Penyimpanan in-memory sederhana untuk latihan. Data hilang saat server dimulai ulang.
// Ganti dengan basis data sungguhan jika proyek berlanjut.
export function createCollection() {
  const items = new Map();

  return {
    list: () => [...items.values()],

    get: (id) => items.get(id),

    create(data) {
      // id dan createdAt diletakkan terakhir agar tidak bisa ditimpa oleh input.
      const item = { ...data, id: randomUUID(), createdAt: new Date().toISOString() };
      items.set(item.id, item);
      return item;
    },

    update(id, data) {
      const current = items.get(id);
      if (!current) return undefined;
      const next = { ...current, ...data, id: current.id, createdAt: current.createdAt };
      items.set(id, next);
      return next;
    },

    remove: (id) => items.delete(id),
  };
}
