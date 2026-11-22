import { fileURLToPath } from "node:url";
import { resolve } from "node:path";
import { defineConfig } from "vite";

const portalRoot = fileURLToPath(new URL(".", import.meta.url));
const repositoryRoot = resolve(portalRoot, "..");

export default defineConfig({
  base: "./",
  root: portalRoot,
  server: {
    fs: {
      allow: [repositoryRoot],
    },
  },
});
