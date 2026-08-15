import path from "path"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
	  alias: {
		  "@": path.resolve(__dirname, "./src"),
	  },
  },
  server: {
    watch: {
      usePolling: true, // Alternative to setting environment variables
    },
    host: true, // Exposes the server to the local network inside Docker
    strictPort: true,
    hmr: {
      clientPort: 5173, // Forces the browser to connect to the exposed host port
    },
  },
})
