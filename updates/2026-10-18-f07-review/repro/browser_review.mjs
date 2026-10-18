// Requires Playwright outside the application checkout and a running local app.
// Uses only the application's documented SYNTHETIC local E2E fixtures.
import { mkdir, writeFile } from 'node:fs/promises';
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.F07_UI_BASE || 'http://127.0.0.1:3017';
const output = process.env.F07_REVIEW_OUTPUT || '/tmp/f07-browser-review';
const password = process.env.F07_SYNTHETIC_PASSWORD || 'E2e-local-2026!';
if (!['127.0.0.1', 'localhost'].includes(new URL(base).hostname)) throw new Error('Local synthetic testing only');
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
const results = [];
function record(id, expected, observed) {
  const pass = expected === observed;
  results.push({ id, expected, observed, pass });
  console.log(`${pass ? 'PASS' : 'FAIL'} ${id}: expected=${expected}, observed=${observed}`);
}
async function login(page, code) {
  await page.goto(`${base}/#/login`);
  await page.locator('#fb-cred-code').fill(code);
  await page.locator('#fb-cred-password').fill(password);
  await page.getByRole('button', { name: 'Đăng nhập vào không gian' }).click();
  await page.waitForURL(url => !url.hash.startsWith('#/login'));
}
async function route(page, name) {
  await page.evaluate(value => { location.hash = value; }, `/${name}`);
  await page.locator(`[data-page="${name}"]`).waitFor();
}
try {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await login(page, 'HSZE2E01');
  await route(page, 'mood');
  const shareButton = page.getByRole('button', { name: 'Chia sẻ mục này' }).first();
  await shareButton.waitFor();
  await shareButton.click();
  await page.getByRole('dialog').waitFor();
  const notePresentBefore = await page.locator('.fb-sheet__body').getByText(/^Ghi chú:/).innerText();
  await page.screenshot({ path: `${output}/r01-before-navigation.png`, fullPage: true });
  await route(page, 'help');
  record('R01-sheet-removed-on-navigation', 0, await page.getByRole('dialog').count());
  await page.screenshot({ path: `${output}/r01-after-navigation.png`, fullPage: true });
  await page.evaluate(async () => {
    const session = await import('/src/core/session.js');
    session.clearSession();
    location.hash = '/login';
  });
  await page.locator('#fb-cred-code').waitFor();
  record('R01-sheet-removed-after-session-clear', 0, await page.getByRole('dialog').count());
  record('R01-old-preview-cleared', false,
    (await page.locator('body').innerText()).includes(notePresentBefore));
  await page.screenshot({ path: `${output}/r01-after-session-clear.png`, fullPage: true });
  await page.close();

  for (const width of [320, 390, 430]) {
    const screen = await browser.newPage({ viewport: { width, height: 844 } });
    await login(screen, 'HSZE2E01');
    await route(screen, 'mood');
    await screen.getByRole('button', { name: 'Chia sẻ mục này' }).first().waitFor();
    const normal = await screen.evaluate(() => ({ viewport: document.documentElement.clientWidth, content: document.documentElement.scrollWidth }));
    record(`layout-${width}-normal-horizontal-overflow`, false, normal.content > normal.viewport);
    await screen.screenshot({ path: `${output}/layout-${width}-normal.png`, fullPage: true });
    // Explicit CSS text scaling: desktop browser approximation, not an OS/device claim.
    await screen.evaluate(() => {
      const elements = Array.from(document.querySelectorAll('p,span,a,button,label,input,textarea,select,option,strong,h1,h2,h3'));
      const styles = elements.map(el => [el, getComputedStyle(el).fontSize, getComputedStyle(el).lineHeight]);
      for (const [el, size, height] of styles) {
        el.style.setProperty('font-size', `${parseFloat(size) * 2}px`, 'important');
        if (height.endsWith('px')) el.style.setProperty('line-height', `${parseFloat(height) * 2}px`, 'important');
      }
    });
    const scaled = await screen.evaluate(() => ({ viewport: document.documentElement.clientWidth, content: document.documentElement.scrollWidth,
      overflow: Array.from(document.querySelectorAll('[data-page="mood"] *')).filter(el => el.getBoundingClientRect().right > innerWidth + 1).slice(0, 8).map(el => ({ tag: el.tagName, className: el.className, right: Math.round(el.getBoundingClientRect().right) })) }));
    console.log(`LAYOUT ${width} CSS text 200: ${JSON.stringify(scaled)}`);
    record(`layout-${width}-css-text-200-horizontal-overflow`, false, scaled.content > scaled.viewport);
    await screen.screenshot({ path: `${output}/layout-${width}-css-text-200.png`, fullPage: true });
    await screen.close();
  }
} finally {
  await writeFile(`${output}/browser-results.json`, JSON.stringify({ method: 'Chromium + real local API; text scaling uses explicit CSS font/line-height doubling', results }, null, 2) + '\n');
  await browser.close();
}
process.exitCode = results.some(r => !r.pass) ? 1 : 0;
