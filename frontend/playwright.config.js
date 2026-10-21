import { defineConfig } from '@playwright/test'


export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  expect: {
    timeout: 8000,
  },
  use: {
    baseURL: 'http://127.0.0.1:5180',
    channel: process.env.PLAYWRIGHT_CHANNEL || 'msedge',
    headless: true,
    trace: 'retain-on-failure',
  },
})
