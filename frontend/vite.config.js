import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '')
  const backendUrl = (env.VITE_BACKEND_URL || env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

  return {
    plugins: [react(), tailwindcss()],
    server: {
      proxy: {
        '/ask': {
          target: backendUrl,
          changeOrigin: true,
        },
        '/healthz': {
          target: backendUrl,
          changeOrigin: true,
        },
        '/readyz': {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  }
})
