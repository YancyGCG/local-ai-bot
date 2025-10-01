import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true, // Allow external connections
    proxy: {
      '/api': 'http://localhost:8899',
      '/status': 'http://localhost:8899',
      '/documents': 'http://localhost:8899',
      '/data': 'http://localhost:8899',
      '/chat': 'http://localhost:8899',
      '/upload-document': 'http://localhost:8899',
      '/upload': 'http://localhost:8899'
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  }
})
