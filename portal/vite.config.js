import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { defineConfig } from "vite";
import { createVoiceId001WritebackPlugin } from "./server/voice-id-001-writeback.js";

const portalRoot = fileURLToPath(new URL(".", import.meta.url));
const repositoryRoot = resolve(portalRoot, "..");

export default defineConfig({
  base: "./",
  root: portalRoot,
  plugins: [createVoiceId001WritebackPlugin({ repositoryRoot })],
  server: {
    host: "127.0.0.1",
    allowedHosts: ["127.0.0.1", "localhost"],
    fs: {
      allow: [repositoryRoot],
    },
  },
});
