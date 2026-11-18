import { ZodError } from 'zod';

// Lemparkan HttpError dari service atau controller untuk error yang sudah diperkirakan.
export class HttpError extends Error {
  constructor(status, code, message) {
    super(message);
    this.name = 'HttpError';
    this.status = status;
    this.code = code;
  }
}

function errorBody(code, message, details) {
  return { error: { code, message, ...(details ? { details } : {}) } };
}

// Error handler terpusat. Detail internal hanya dicatat di server, tidak dikirim ke klien.
export function errorHandler(err, _req, res, next) {
  if (res.headersSent) return next(err);

  if (err instanceof ZodError) {
    const details = err.issues.map((issue) => ({
      path: issue.path.join('.'),
      message: issue.message,
    }));
    return res.status(400).json(errorBody('VALIDATION_ERROR', 'Input tidak valid.', details));
  }

  if (err instanceof HttpError) {
    return res.status(err.status).json(errorBody(err.code, err.message));
  }

  if (err?.type === 'entity.parse.failed') {
    return res.status(400).json(errorBody('INVALID_JSON', 'Isi permintaan bukan JSON yang valid.'));
  }

  if (err?.type === 'entity.too.large') {
    return res.status(413).json(errorBody('PAYLOAD_TOO_LARGE', 'Isi permintaan terlalu besar.'));
  }

  console.error(err);
  return res.status(500).json(errorBody('INTERNAL_ERROR', 'Terjadi kesalahan pada server.'));
}
