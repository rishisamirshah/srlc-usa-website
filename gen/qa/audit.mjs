// node audit.mjs <baseURL> <widths comma> <paths comma | @file> [out.json]
// For every photo on each page and width: which part of the source shows
// (object-fit/background-size math, clipped by overflow ancestors and the
// viewport), then each detected face is OK, out of frame, CUT, HAIR (face in,
// top of head clipped) or under TEXT (a heading/paragraph sits on the face).
import { chromium } from '/Users/rishi/Documents/SRA-USA/sra-usa-ash/node_modules/playwright/index.mjs';
import fs from 'fs';
const DIR = new URL('.', import.meta.url).pathname;
const [base, widthsArg, pathsArg, outFile] = process.argv.slice(2);
const widths = widthsArg.split(",").map(s => s.includes("x") ? s.split("x").map(Number) : [+s, 900]);
const paths = pathsArg.startsWith('@') ? fs.readFileSync(pathsArg.slice(1), 'utf8').split('\n').filter(Boolean) : pathsArg.split(',');
const FACES = {};
for (const l of fs.readFileSync(DIR + 'faces.jsonl', 'utf8').split('\n').filter(Boolean)) { const d = JSON.parse(l); FACES['/' + d.file] = d; }

const b = await chromium.launch();
const issues = [], seen = [];
for (const path of paths) for (const [w, vh] of widths) {
  const p = await b.newPage({ viewport: { width: w, height: vh } });
  await p.addInitScript(() => { try { sessionStorage.setItem('nl-modal-shown', '1'); } catch (e) {} });
  await p.goto(base + path, { waitUntil: 'networkidle' }).catch(() => {});
  await p.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important}' });
  await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); await new Promise(r => setTimeout(r, 300)); });
  await p.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 15000 }).catch(() => {});
  const items = await p.evaluate(async () => {
    const out = [];
    const pct = (v, free) => v.endsWith('%') ? parseFloat(v) / 100 * free : parseFloat(v) || 0;
    const clipOf = (el) => {
      let r = { l: 0, t: -1e9, r: document.documentElement.clientWidth, b: 1e9 };
      for (let a = el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
        const c = getComputedStyle(a);
        if (c.display === 'none') return null;
        if (/(hidden|clip|auto|scroll)/.test(c.overflowX + c.overflowY)) {
          const br = a.getBoundingClientRect();
          r = { l: Math.max(r.l, br.left), t: Math.max(r.t, br.top + scrollY), r: Math.min(r.r, br.right), b: Math.min(r.b, br.bottom + scrollY) };
        }
      }
      return r;
    };
    const natural = (url) => new Promise(res => { const i = new Image(); i.onload = () => res([i.naturalWidth, i.naturalHeight]); i.onerror = () => res(null); i.src = url; });
    // text that is actually showing: every ancestor visible and opaque, and not a hover/back face layer
    const shown = (t) => { for (let a = t; a && a !== document.body; a = a.parentElement) { const c = getComputedStyle(a); if (c.visibility === 'hidden' || +c.opacity < 0.05 || c.display === 'none' || /__(back|hover)\b/.test(String(a.className))) return false; } return true; };
    const textBoxes = (section) => [...section.querySelectorAll('h1,h2,h3,h4,p,li,a.btn,blockquote,figcaption,.btn')].filter(t => {
      return t.textContent.trim() && t.getBoundingClientRect().width > 0 && shown(t);
    }).map(t => { const r = t.getBoundingClientRect(); return { l: r.left, t: r.top + scrollY, r: r.right, b: r.bottom + scrollY, tag: t.tagName.toLowerCase() + (t.className ? '.' + String(t.className).split(' ')[0] : '') }; });
    const describe = (el) => { const s = el.closest('section,header,footer,figure,article,div[class]'); return (s ? (s.tagName.toLowerCase() + '.' + String(s.className).split(' ').join('.')) : '') + ' > ' + el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ').join('.') : ''); };
    const els = [...document.querySelectorAll('img, [style*="background"], *')].filter((e, i, a) => a.indexOf(e) === i);
    for (const el of els) {
      const cs = getComputedStyle(el);
      let src = null, fit, posX, posY, nat;
      if (el.tagName === 'IMG') {
        src = el.currentSrc || el.src; fit = cs.objectFit; [posX, posY] = cs.objectPosition.split(' ');
        nat = el.naturalWidth ? [el.naturalWidth, el.naturalHeight] : null;
      } else {
        const m = cs.backgroundImage.match(/url\("?([^")]+)"?\)/); if (!m) continue;
        src = m[1]; const bs = cs.backgroundSize; fit = bs === 'cover' ? 'cover' : bs === 'contain' ? 'contain' : 'bg:' + bs;
        [posX, posY] = cs.backgroundPosition.split(',')[0].trim().split(' ');
        nat = await natural(src);
      }
      if (!src || !nat || src.startsWith('data:') || /\.svg(\?|$)/.test(src)) continue;
      const br = el.getBoundingClientRect(); if (br.width < 40 || br.height < 40 || cs.display === 'none' || cs.visibility === 'hidden') continue;
      const clip = clipOf(el); if (!clip) continue;
      const bw = br.width, bh = br.height; let rw, rh;
      if (fit === 'cover') { const s = Math.max(bw / nat[0], bh / nat[1]); rw = nat[0] * s; rh = nat[1] * s; }
      else if (fit === 'contain') { const s = Math.min(bw / nat[0], bh / nat[1]); rw = nat[0] * s; rh = nat[1] * s; }
      else if (fit === 'fill' || fit === 'none' && false) { rw = bw; rh = bh; }
      else if (fit && fit.startsWith('bg:')) { const v = fit.slice(3).split(' '); if (v[0] === 'auto') { rw = nat[0]; rh = nat[1]; } else { rw = pct(v[0], bw) || bw; rh = v[1] && v[1] !== 'auto' ? pct(v[1], bh) : rw * nat[1] / nat[0]; } if (v[0].endsWith('%')) rw = parseFloat(v[0]) / 100 * bw; }
      else { rw = bw; rh = bh; }
      const ix = br.left + pct(posX || '50%', bw - rw), iy = br.top + scrollY + pct(posY || '50%', bh - rh);
      const vis = { l: Math.max(br.left, clip.l, ix), t: Math.max(br.top + scrollY, clip.t, iy), r: Math.min(br.right, clip.r, ix + rw), b: Math.min(br.bottom + scrollY, clip.b, iy + rh) };
      if (vis.r - vis.l < 20 || vis.b - vis.t < 20) continue;
      const sec = el.closest('section') || el.parentElement;
      const texts = textBoxes(sec).filter(t => t.r > vis.l && t.l < vis.r && t.b > vis.t && t.t < vis.b && !el.contains(document.elementFromPoint(0, 0)));
      out.push({ src: new URL(src, location.href).pathname, where: describe(el), img: { x: ix, y: iy, w: rw, h: rh }, vis, texts, op: +cs.opacity });
    }
    return out;
  });
  for (const it of items) {
    const fd = FACES[decodeURIComponent(it.src)]; if (!fd) continue;
    const V = { l: (it.vis.l - it.img.x) / it.img.w, t: (it.vis.t - it.img.y) / it.img.h, r: (it.vis.r - it.img.x) / it.img.w, b: (it.vis.b - it.img.y) / it.img.h };
    seen.push({ path, w, vh, src: it.src, where: it.where, V, faces: fd.faces.length });
    fd.faces.forEach(([fx, fy, fw, fh, conf], i) => {
      const F = { l: fx, t: fy, r: fx + fw, b: fy + fh };
      const H = { l: Math.max(0, fx - 0.2 * fw), t: Math.max(0, fy - 0.45 * fh), r: Math.min(1, fx + 1.2 * fw), b: Math.min(1, fy + 1.1 * fh) };
      const iw = Math.max(0, Math.min(F.r, V.r) - Math.max(F.l, V.l)), ih = Math.max(0, Math.min(F.b, V.b) - Math.max(F.t, V.t));
      const frac = (iw * ih) / (fw * fh);
      const eps = 0.002;
      let status = null;
      const hw = Math.max(0, Math.min(H.r, V.r) - Math.max(H.l, V.l)), hh = Math.max(0, Math.min(H.b, V.b) - Math.max(H.t, V.t));
      const hfrac = (hw * hh) / ((H.r - H.l) * (H.b - H.t));
      if (frac === 0) {
        // face itself is out of frame; a sliver of head (ear, hair) left at the edge still reads as cut
        if (hfrac > 0.08) issues.push({ path, w, vh, src: it.src, where: it.where, face: i, conf, status: 'EDGE', frac: +hfrac.toFixed(2), face_box: [fx, fy, fw, fh], V: Object.fromEntries(Object.entries(V).map(([k, v]) => [k, +v.toFixed(3)])) });
        return;
      }
      if (frac < 0.98) status = 'CUT';
      else if (H.l < V.l - eps || H.r > V.r + eps || H.t < V.t - eps || H.b > V.b + eps) status = 'HAIR';
      const page = { l: it.img.x + F.l * it.img.w, t: it.img.y + F.t * it.img.h, r: it.img.x + F.r * it.img.w, b: it.img.y + F.b * it.img.h };
      const area = (page.r - page.l) * (page.b - page.t);
      const over = it.texts.filter(t => Math.max(0, Math.min(t.r, page.r) - Math.max(t.l, page.l)) * Math.max(0, Math.min(t.b, page.b) - Math.max(t.t, page.t)) > 0.1 * area);
      if (over.length && frac > 0) status = (status ? status + '+' : '') + 'TEXT(' + over.map(o => o.tag).join(',') + ')';
      if (status) issues.push({ path, w, vh, src: it.src, where: it.where, face: i, conf, status, frac: +frac.toFixed(2), face_box: [fx, fy, fw, fh], V: Object.fromEntries(Object.entries(V).map(([k, v]) => [k, +v.toFixed(3)])) });
    });
  }
  await p.close();
}
await b.close();

const by = {}; for (const i of issues) { const k = `${i.path} ${i.w} ${i.src}`; (by[k] = by[k] || []).push(i.status + (i.status.startsWith('CUT') ? '@' + i.frac : '')); }
for (const [k, v] of Object.entries(by)) console.log(k, '|', v.join(' '));
for (const s of seen) { const fd = FACES[decodeURIComponent(s.src)]; s.inFrame = fd.faces.filter(([x, y, w, h]) => x >= s.V.l && x + w <= s.V.r && y >= s.V.t && y + h <= s.V.b).length; }
fs.writeFileSync(outFile || DIR + 'audit.json', JSON.stringify({ issues, seen }, null, 1));
console.log(`${issues.length} issues, ${seen.length} photo placements checked`);
