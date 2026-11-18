import { existsSync } from 'node:fs';

// Muat .env jika ada (dijalankan dari folder api/).
if (existsSync('.env')) process.loadEnvFile('.env');

const env = process.env;

export const config = Object.freeze({
  nodeEnv: env.NODE_ENV ?? 'development',
  isProduction: env.NODE_ENV === 'production',
  port: Number(env.PORT ?? 4000),
  corsOrigins: (env.CORS_ORIGINS ?? 'http://localhost:3000')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean),
});
