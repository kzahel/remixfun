import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  workers: 1,
  use: {
    baseURL: "http://127.0.0.1:8791",
    viewport: { width: 1280, height: 900 },
    trace: "retain-on-failure",
  },
  webServer: {
    command:
      "uv run remixfun serve --port 8791 --data-dir .e2e-data --web-dir web/dist",
    cwd: "..",
    url: "http://127.0.0.1:8791/api/health",
    reuseExistingServer: false,
  },
});
