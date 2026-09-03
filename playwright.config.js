// @ts-check
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 15_000,
  retries: 0,
  workers: 1,
  use: {
    baseURL: 'http://127.0.0.1:3000',
    headless: true,
    browserName: 'chromium',
  },
  webServer: {
    command: 'node server.js',
    url: 'http://127.0.0.1:3000',
    reuseExistingServer: false,
    timeout: 20_000,
  },
});
