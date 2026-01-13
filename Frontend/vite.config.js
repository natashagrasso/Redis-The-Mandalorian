import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Escuchar en todas las direcciones IP (necesario para Docker)
    strictPort: true,
    port: 5173, // Puerto estándar
    watch: {
      usePolling: true, // Necesario en Windows para que detecte cambios en vivo
    },
  },
})
