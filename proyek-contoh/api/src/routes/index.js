import { Router } from 'express';
import { healthRoutes } from './health.routes.js';
import { noteRoutes } from './note.routes.js';

export const routes = Router();

routes.use('/health', healthRoutes);
routes.use('/notes', noteRoutes);

// Daftarkan rute fitur baru di sini, misalnya:
// routes.use('/products', productRoutes);
