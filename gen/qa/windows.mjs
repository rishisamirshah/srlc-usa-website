// node windows.mjs <url> <from> <to> <step> -> per width, each storysplit photo's visible fraction (w_x, w_y)
import { chromium } from '/Users/rishi/Documents/SRA-USA/sra-usa-ash/node_modules/playwright/index.mjs';
const [url, from, to, step] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +from, height: 900 } });
await p.goto(url, { waitUntil: 'networkidle' });
const rows = [];
for (let w = +from; w <= +to; w += +step) {
  await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(60);
  const r = await p.evaluate(() => [...document.querySelectorAll('.storysplit__media img, .pagehead__img')].map(i => {
    const b = i.getBoundingClientRect(); const s = Math.max(b.width / i.naturalWidth, b.height / i.naturalHeight);
    return [i.src.split('/').pop(), +(b.width / (i.naturalWidth * s)).toFixed(4), +(b.height / (i.naturalHeight * s)).toFixed(4)];
  }));
  rows.push([w, r]);
}
console.log(JSON.stringify(rows));
await b.close();
