import { Router } from 'express';
import { validate } from '../middlewares/validate.js';
import { createNoteSchema, noteParamsSchema, updateNoteSchema } from '../schemas/note.schema.js';
import {
  createNote,
  deleteNote,
  getNote,
  listNotes,
  updateNote,
} from '../controllers/note.controller.js';

export const noteRoutes = Router();

noteRoutes.get('/', listNotes);
noteRoutes.post('/', validate({ body: createNoteSchema }), createNote);
noteRoutes.get('/:id', validate({ params: noteParamsSchema }), getNote);
noteRoutes.patch('/:id', validate({ params: noteParamsSchema, body: updateNoteSchema }), updateNote);
noteRoutes.delete('/:id', validate({ params: noteParamsSchema }), deleteNote);
