import { useId } from 'react';
import type { TextareaHTMLAttributes } from 'react';
import styles from './Textarea.module.css';

type Props = Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, 'id'> & {
  label: string;
  error?: string;
};

// Field multi-baris. Perilakunya sama dengan Input: label terhubung, error di bawah field.
export function Textarea({ label, error, className, rows = 4, ...rest }: Props) {
  const id = useId();
  const errorId = `${id}-error`;
  const classes = [styles.textarea, className].filter(Boolean).join(' ');

  return (
    <div className={styles.field}>
      <label htmlFor={id} className={styles.label}>
        {label}
      </label>
      <textarea
        id={id}
        rows={rows}
        className={classes}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : undefined}
        {...rest}
      />
      {error ? (
        <p id={errorId} role="alert" className={styles.error}>
          {error}
        </p>
      ) : null}
    </div>
  );
}
