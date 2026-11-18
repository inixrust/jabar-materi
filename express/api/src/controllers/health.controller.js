import { healthService } from '../services/health.service.js';

export function getHealth(_req, res) {
  res.json({ data: healthService.check() });
}
