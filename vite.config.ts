import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  server: { port: 9999, strictPort: false },
  preview: { port: 9999, strictPort: false },
  test: { environment: "node" },
});
