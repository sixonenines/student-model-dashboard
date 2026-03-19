import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api/python": {
        target: "http://localhost:8000",
        rewrite: (path) => path.replace(/^\/api\/python/, "/api"),
      },
      "/api/r": {
        target: "http://localhost:8001",
        rewrite: (path) => path.replace(/^\/api\/r/, "/api"),
      },
    },
  },
});
