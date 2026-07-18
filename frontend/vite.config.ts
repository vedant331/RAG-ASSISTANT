import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})

// What changed: we added the import for tailwindcss 
// and included it in the plugins array, alongside the react() plugin Vite already set up.
