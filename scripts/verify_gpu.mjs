// Explicit GPU/browser acceptance; run against a source service with --comfy-root.
// Requires the web project's Playwright Chromium installation. Never runs in CI.
import { createRequire } from "node:module";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
const require = createRequire(new URL("../web/package.json", import.meta.url));
const { chromium, expect } = require("@playwright/test");
const base = process.argv[2] ?? "http://127.0.0.1:8793";
if (new URL(base).hostname !== "127.0.0.1") throw new Error("Use the local verification service.");
const output = path.resolve("artifacts/gpu-verification");
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  await page.goto(base);
  await page.getByRole("textbox", { name: "Describe your image" }).fill(
    "A quiet alpine lake at sunrise, snow capped mountains reflected in perfectly still turquoise water, pine forest along the shore, warm golden sunlight, a tiny red canoe, detailed landscape photograph, no text",
  );
  await page.getByRole("button", { name: "Create recipe", exact: true }).click();
  const submitted = page.waitForResponse((response) => response.url().endsWith("/reproduce") && response.request().method() === "POST");
  await page.getByRole("button", { name: "Generate image", exact: true }).click();
  const response = await submitted;
  if (response.status() !== 202) throw new Error(await response.text());
  const started = await response.json();
  console.log(`Submitted real GPU job ${started.id}`);
  await expect(page.getByText("IMAGE GENERATED", { exact: true })).toBeVisible({ timeout: 600000 });
  await expect(page.locator(".image-stage img")).toBeVisible();
  await page.screenshot({ path: path.join(output, "result.png"), fullPage: true });
  const job = await (await page.request.get(`${base}/api/jobs/${started.id}`)).json();
  if (job.engine !== "comfy" || job.status !== "completed") throw new Error("Real generation did not complete");
  const image = await page.request.get(`${base}${job.output.url}`);
  await writeFile(path.join(output, "generated.png"), await image.body());
  await writeFile(path.join(output, "job.json"), JSON.stringify(job, null, 2));
  await page.reload();
  await page.getByRole("button", { name: /SDXL · .*Generation recipe/ }).first().click();
  await page.getByRole("button", { name: "Result", exact: true }).click();
  await expect(page.getByText("IMAGE GENERATED", { exact: true })).toBeVisible();
  console.log(JSON.stringify({ status: job.status, engine: job.engine, image: job.image, output: job.output, runtime: job.runtime, reopen: "passed" }, null, 2));
} finally {
  await browser.close();
}
