import type { Note } from '@/lib/api';
import styles from './Catatan.module.css';

const formatWaktu = new Intl.DateTimeFormat('id-ID', { dateStyle: 'medium', timeStyle: 'short' });

type Props = {
  notes: Note[];
};

// Isi catatan ditampilkan sebagai teks biasa; React meng-encode keluaran (SC-03).
export function NoteList({ notes }: Props) {
  const terbaruDulu = [...notes].sort((a, b) => b.createdAt.localeCompare(a.createdAt));

  return (
    <ul className={styles.list}>
      {terbaruDulu.map((note) => (
        <li key={note.id} className={styles.item}>
          <h3 className={styles.itemTitle}>{note.title}</h3>
          {note.body ? <p className={styles.itemBody}>{note.body}</p> : null}
          <time className={styles.itemTime} dateTime={note.createdAt}>
            {formatWaktu.format(new Date(note.createdAt))}
          </time>
        </li>
      ))}
    </ul>
  );
}
