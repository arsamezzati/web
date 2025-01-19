import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3535,
    watch: {
      usePolling: true,  // Add this for Docker compatibility
      poll: 1000         // Check for changes every second
    },
    proxy: {
      '/api': {
        target: 'http://backend:5050',
        changeOrigin: true
      }
    }
  }
})