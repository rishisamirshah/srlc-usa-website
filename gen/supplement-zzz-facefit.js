/* Face-safe crops picked live (Naman, Oct 22: no face cut off in any photo).
   A photo with data-faces (face boxes from gen/qa, as shares of the photo)
   gets the object-position, and if needed a slight zoom, that leaves every
   face fully in or fully out of its visible crop at the size it actually has
   on screen; redone whenever the photo's frame changes size. Order of
   preference: no face cut, no face under the data-avoid text, most faces in,
   least zoom, closest to data-pos. Without JS the CSS crop stands.
   - data-avoid: a selector inside the photo's section whose text faces stay
     clear of (a headline, a story panel).
   - data-fit-min: skip widths below it, where the CSS crop for the fixed
     phone and tablet boxes applies.
   - data-pad="shoulders": the box runs out to the shoulders and down to the
     chest, and may run past the bottom of the frame.
   - data-head: room kept above the face, in face heights (default 0.6, eased
     to 0.45 where nothing fits with 0.6).
   - data-keep="x0,y0,x1,y1": an area (shares of the photo) that must stay
     whole at every scroll position, like caps and a diploma.
   - data-fill: prefer the closest crop that still keeps everything whole.
   Parallax photos (img.px, supplement-zz-px.js) drift inside a frame shorter
   than the photo, so every face must sit in the band that stays visible at
   every scroll position (Naman, Oct 27). Each photo gets the strongest drift
   that keeps every face and person whole (10% of its frame, stepping down to
   4%); one that can't drift at all holds still (data-px-hold).
   The zoom and its origin go out as --fz and --fo, so the drift and the zoom
   share one transform; the drift goes out as --pxr. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img[data-faces]'));
  if (!imgs.length) return;
  var ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];
  var FILL_ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6];
  var ROOMS = [0.10, 0.08, 0.06, 0.04];  // drift, as a share of the frame height

  // head boxes: [left, top, right, bottom, face height, shoulders left,
  // shoulders right, prominent]. A prominent person (face at least 8% of the
  // photo's height) counts as in only with the shoulders in too, so nobody
  // in the foreground is sliced at a side edge (Naman, Oct 27); a forced cut
  // takes the smallest face.
  var BIG = 0.08;
  function heads(img, up) {
    var sh = img.getAttribute('data-pad') === 'shoulders';
    return img.getAttribute('data-faces').split(';').map(function (s) {
      var f = s.split(',').map(Number);
      var big = f[3] >= BIG;
      var box = sh
        ? [Math.max(0, f[0] - 0.9 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.9 * f[2]), Math.min(1, f[1] + 2.2 * f[3])]
        : [Math.max(0, f[0] - 0.2 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.2 * f[2]), Math.min(1, f[1] + 1.1 * f[3])];
      var wl = big ? Math.max(0, Math.min(box[0], f[0] - 0.55 * f[2])) : box[0];
      var wr = big ? Math.min(1, Math.max(box[2], f[0] + 1.55 * f[2])) : box[2];
      return box.concat([f[3], wl, wr, big]);
    });
  }

  function better(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] < b[i];
    return false;
  }

  // parallax runs on this photo at this width (the CSS turns it on at 861px
  // and up, never with reduced motion)
  function drifting(img) {
    return img.classList.contains('px') && window.innerWidth >= 861 &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  // the drift positions this photo can actually reach: p runs from -1 (frame
  // entering at the bottom of the screen) to +1 (leaving at the top), but a
  // frame already on screen at the top of the page, or still on screen at
  // the very bottom, never reaches the far end (a hero starts near 0)
  function reach(img) {
    var r = img.parentElement.getBoundingClientRect(), vh = window.innerHeight;
    var top = r.top + window.scrollY, h = r.height;
    var maxS = Math.max(0, document.documentElement.scrollHeight - vh);
    function p(sy) { return Math.max(-1, Math.min(1, (vh - (top - sy)) / (vh + h) * 2 - 1)); }
    return [p(0), p(maxS)];
  }

  // the text lines in the photo box's coordinates (the box sits `room` above
  // the frame), stretched over every drift position the photo can reach (it
  // moves p * room against the text). A short eyebrow counts by its words, not
  // its full-width box; a block holding other blocks (a story panel) counts whole.
  function avoidRects(img, room, pr) {
    var sel = img.getAttribute('data-avoid'), sec = img.closest('section');
    if (!sel || !sec) return [];
    var fr = img.parentElement.getBoundingClientRect();
    var out = [];
    Array.prototype.forEach.call(sec.querySelectorAll(sel), function (e) {
      var rects = [e.getBoundingClientRect()];
      if (e.textContent.trim() && !e.querySelector('div, p, h1, h2, h3, h4, ul, ol')) {
        var rg = document.createRange();
        rg.selectNodeContents(e);
        rects = Array.prototype.slice.call(rg.getClientRects());
      }
      rects.forEach(function (r) {
        if (r.width > 0 && r.height > 0)
          out.push([r.left - fr.left, r.top - fr.top + room - pr[1] * room, r.right - fr.left, r.bottom - fr.top + room - pr[0] * room]);
      });
    });
    return out;
  }

  function clear(img) {
    img.style.objectPosition = img._pos0 || '';
    img.style.removeProperty('--fz');
    img.style.removeProperty('--fo');
    img.style.removeProperty('--pxr');
    img.removeAttribute('data-px-hold');
  }

  function fit(img) {
    var min = Number(img.getAttribute('data-fit-min') || 0);
    if (min && window.innerWidth < min) { clear(img); return; }
    var frame = img.parentElement;
    var fw = frame.clientWidth, fh = frame.clientHeight;
    if (!fw || !fh || !img.naturalWidth || getComputedStyle(img).objectFit !== 'cover') return;
    var calm = settle(img, fw, fh, 0);
    img._calm = calm;  // for QA
    if (drifting(img)) {
      // the strongest drift that does as well as holding still: no more heads
      // cut, no more faces under the text, no prominent person lost
      for (var i = 0; i < ROOMS.length; i++) {
        var o = ROOMS[i] * fh, best = settle(img, fw, fh + 2 * o, o);
        if (!better([calm.key[0], calm.key[1], -calm.big], [best.key[0], best.key[1], -best.big])) {
          img._drift = best;
          img.removeAttribute('data-px-hold');
          img.style.setProperty('--pxr', ROOMS[i] * 100 + '%');
          apply(img, best);
          return;
        }
      }
      img.setAttribute('data-px-hold', '');
    }
    img.style.removeProperty('--pxr');
    apply(img, calm);
  }

  // the best crop with generous room above heads, or with the usual room when
  // the generous one can't keep every face whole
  function settle(img, bw, bh, o) {
    var set = img.getAttribute('data-head');
    var best = search(img, bw, bh, o, set ? Number(set) : 0.6);
    if (!set && (best.key[0] > 0 || best.key[1] > 0)) {
      var eased = search(img, bw, bh, o, 0.45);
      if (better(eased.key.slice(0, 2), best.key.slice(0, 2))) best = eased;
    }
    return best;
  }

  // bw x bh: the photo box (frame plus the drift room o above and below)
  function search(img, bw, bh, o, up) {
    // share of the box that can scroll out of view at the top and at the bottom
    var pr = o ? reach(img) : [0, 0];
    var mt = o ? o * (1 - pr[0]) / bh : 0, mb = o ? o * (1 + pr[1]) / bh : 0;
    var av = avoidRects(img, o, pr);
    var s = Math.max(bw / img.naturalWidth, bh / img.naturalHeight);
    var wx0 = bw / (img.naturalWidth * s), wy0 = bh / (img.naturalHeight * s);
    var hs = heads(img, up);
    var open = img.getAttribute('data-pad') === 'shoulders';
    var keep = img.getAttribute('data-keep');
    keep = keep ? keep.split(',').map(Number) : null;
    var fill = img.hasAttribute('data-fill');
    var pref = (img.getAttribute('data-pos') || '50 50').split(' ').map(Number);
    var best = null;
    (fill ? FILL_ZOOMS : ZOOMS).forEach(function (z) {
      var wx = wx0 / z, wy = wy0 / z;
      for (var px = 0; px <= 100; px += 2) {
        for (var py = 0; py <= 100; py += (wy < 0.999 ? 1 : 101)) {
          var ppy = wy < 0.999 ? py : 50;
          var l = px / 100 * (1 - wx), t = ppy / 100 * (1 - wy), r = l + wx, b = t + wy;
          var st = t + mt * wy, sb = b - mb * wy;  // always on screen
          var cut = 0, inn = 0, txt = 0, big = 0;
          if (keep && !(keep[0] >= l - 1e-4 && keep[2] <= r + 1e-4 && keep[1] >= st - 1e-4 && keep[3] <= sb + 1e-4)) cut += 1;
          for (var i = 0; i < hs.length; i++) {
            var h = hs[i];
            if (h[2] <= l || h[0] >= r || h[3] <= t || h[1] >= b) continue;
            if (h[5] >= l - 1e-4 && h[6] <= r + 1e-4 && h[1] >= st - 1e-4 && (open || h[3] <= sb + 1e-4)) {
              inn++;
              if (h[7]) big++;
              var x0 = (h[0] - l) / wx * bw, y0 = (h[1] - t) / wy * bh, x1 = (h[2] - l) / wx * bw, y1 = (h[3] - t) / wy * bh;
              for (var k = 0; k < av.length; k++) {
                if (x0 < av[k][2] && x1 > av[k][0] && y0 < av[k][3] && y1 > av[k][1]) { txt++; break; }
              }
            } else cut += h[4];
          }
          var key = [cut, txt, -inn, fill ? -z : z, Math.abs(px - pref[0]) + Math.abs(ppy - pref[1])];
          if (!best || better(key, best.key)) best = { key: key, px: px, py: ppy, z: z, big: big };
        }
      }
    });
    return best;
  }

  function apply(img, best) {
    img._fit = best;  // for QA: [cut, under text, -in, zoom, distance] of the chosen crop
    var pos = best.px + '% ' + best.py + '%';
    img.style.objectPosition = pos;
    img.style.setProperty('--fo', pos);
    if (best.z > 1) img.style.setProperty('--fz', best.z); else img.style.removeProperty('--fz');
  }

  function all() { imgs.forEach(fit); }
  imgs.forEach(function (img) {
    img._pos0 = img.style.objectPosition;  // the static crop, restored where fitting is off
    if (img.complete) fit(img); else img.addEventListener('load', function () { fit(img); });
  });
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(all, 120); });
  window.addEventListener('load', all);
  // refit whenever a photo's frame changes size (equal-height splits, fonts)
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function (entries) {
      entries.forEach(function (e) {
        var img = e.target._fitImg;
        if (img && img.complete) fit(img);
      });
    });
    imgs.forEach(function (img) {
      if (!img.parentElement) return;
      img.parentElement._fitImg = img;
      ro.observe(img.parentElement);
    });
  }
})();
