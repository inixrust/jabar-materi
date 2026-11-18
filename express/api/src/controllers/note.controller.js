import { noteService } from '../services/note.service.js';

// Controller membaca input yang sudah divalidasi (req.validated) dan membentuk respons.

export function listNotes(_req, res) {
  res.json({ data: noteService.list() });
}

export function getNote(req, res) {
  res.json({ data: noteService.getById(req.validated.params.id) });
}

export function createNote(req, res) {
  res.status(201).json({ data: noteService.create(req.validated.body) });
}

export function updateNote(req, res) {
  res.json({ data: noteService.update(req.validated.params.id, req.validated.body) });
}

export function deleteNote(req, res) {
  noteService.remove(req.validated.params.id);
  res.status(204).end();
}
