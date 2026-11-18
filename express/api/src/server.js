import { createApp } from './app.js';
import { config } from './config/index.js';

const app = createApp();

app.listen(config.port, () => {
  console.info(`API berjalan di http://localhost:${config.port}`);
});
