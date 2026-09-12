import { test, expect } from "@playwright/test";
import path from "node:path";

test("demo recipe, result, advanced seed and persisted library", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Your next idea starts with an image." }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Open demo", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Stillwater at dawn" }),
  ).toBeVisible();
  await expect(page.locator("details")).not.toHaveAttribute("open", "");
  await page.getByText("Source details & advanced", { exact: true }).click();
  await expect(
    page.locator("dd").filter({ hasText: "18446744073709551614" }),
  ).toBeVisible();
  await page.getByText("Source details & advanced", { exact: true }).click();
  await page
    .getByRole("button", { name: "Run demo preview", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "A starting point, saved." }),
  ).toBeVisible();
  await expect(page.getByText("Not evaluated", { exact: true })).toBeVisible();
  await page.reload();
  await page
    .getByRole("button", { name: "Stillwater at dawn Demo collection" })
    .click();
  await page.getByRole("button", { name: "Result", exact: true }).click();
  await expect(page.getByText("Not evaluated", { exact: true })).toBeVisible();
});

test("invalid URL remains actionable and does not create an import", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByRole("textbox", { name: "Civitai image URL" })
    .fill("https://example.com/not-civitai");
  await page.getByRole("button", { name: "Import image", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText(
    "Paste a Civitai image link",
  );
  await expect(
    page.getByRole("textbox", { name: "Civitai image URL" }),
  ).toHaveValue("https://example.com/not-civitai");
});

test("mobile workspace has no horizontal overflow", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(
    page.getByRole("button", { name: "Open demo", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBeTruthy();
  await page.getByRole("button", { name: "Open demo", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Stillwater at dawn" }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBeTruthy();
});

test("original PNG upload preserves seed, missing scheduler and unavailable generation", async ({
  page,
}) => {
  await page.goto("/");
  await page
    .getByLabel("Import image file")
    .setInputFiles(path.resolve("../tests/fixtures/metadata.png"));
  await expect(
    page.getByRole("heading", { name: "metadata.png", exact: true }),
  ).toBeVisible();
  await expect(page.getByText("A quiet lake", { exact: true })).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Reproduction unavailable" }),
  ).toBeDisabled();
  await page.getByText("Source details & advanced", { exact: true }).click();
  await expect(
    page.locator("dd").filter({ hasText: "18446744073709551614" }),
  ).toBeVisible();
  await expect(
    page
      .locator("dt")
      .filter({ hasText: /^scheduler$/ })
      .locator("+ dd"),
  ).toHaveText("Unknown");
  await expect(
    page.getByRole("link", { name: "Export recipe" }),
  ).toHaveAttribute("href", /\/manifest$/);
});

test("settings dialog supports keyboard close and restores focus", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings", exact: true }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(
    page.getByRole("button", { name: "Settings", exact: true }),
  ).toBeFocused();
});

test("model download progress and resume controls restore from the service", async ({ page }) => {
  let status = "download_needed";
  const hash = "a".repeat(64);
  await page.route("**/api/imports/*/dependencies", route => route.fulfill({ json: {
    revision: hash, total_download_bytes: 6940000000, unknown_sizes: 0,
    generation_blockers: ["Source scheduler remains unknown."],
    dependencies: [{ id: "0", name: "Owned checkpoint", version_name: "Fixture version", status,
      file: { file_id: "1", name: "owned.safetensors", sha256: hash, size_estimate: 6940000000 }, candidates: [],
      ...(status === "download_needed" ? {} : { download: { id: "owned", status, downloaded_bytes: 123000000,
        total_bytes: 6940000000, message: "Owned download fixture" } }),
    }],
  } }));
  await page.route("**/api/imports/*/downloads", route => {
    expect(route.request().postDataJSON().revision).toBe(hash);
    status = "downloading";
    return route.fulfill({ json: { dependencies: { "0": { status, download_id: "owned" } } } });
  });
  await page.route("**/api/downloads/owned/*", route => {
    status = route.request().url().endsWith("/pause") ? "paused" : "downloading";
    return route.fulfill({ json: { id: "owned", status } });
  });
  await page.goto("/");
  await page.getByLabel("Import image file").setInputFiles(path.resolve("../tests/fixtures/metadata.png"));
  await page.getByRole("button", { name: "Download missing models · 6.94 GB" }).click();
  await expect(page.getByRole("progressbar", { name: "Owned checkpoint download progress" })).toBeVisible();
  await page.getByRole("button", { name: "Pause download", exact: true }).click();
  await expect(page.getByRole("button", { name: "Resume download", exact: true })).toBeVisible();
  await page.reload();
  await page.getByRole("button", { name: /metadata.png/ }).first().click();
  await page.getByRole("button", { name: "Resume download", exact: true }).click();
  await expect(page.getByRole("button", { name: "Pause download", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Reproduction unavailable" })).toBeDisabled();
  await expect(page.getByText("Source scheduler remains unknown.")).toBeVisible();
});
