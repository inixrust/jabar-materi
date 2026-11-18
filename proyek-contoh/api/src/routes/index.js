import { Router } from 'express';
import { healthRoutes } from './health.routes.js';

export const routes = Router();

routes.use('/health', healthRoutes);

// Daftarkan rute fitur baru di sini, misalnya:
// routes.use('/products', productRoutes);
