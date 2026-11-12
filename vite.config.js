import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// SPA fallback is Vite's default, so /about and /project/:id deep links work.
export default defineConfig({
  plugins: [react()],
  server: { port: 5190, host: true },
});
