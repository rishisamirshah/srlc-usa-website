/* Face-safe crops picked live (Naman, Oct 22: no face cut off in any photo).
   A photo with data-faces (face boxes from gen/qa, as shares of the photo)
   gets the object-position, and if needed a slight zoom, that leaves every
   face fully in or fully out of its visible crop at the size it actually has
   on screen; redone whenever the photo's box changes size. Order of
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
   - Parallax photos (img.px, supplement-zz-px.js) drift inside a frame
     shorter than the photo, so every face must sit in the band that stays
     visible at every scroll position (Naman, Oct 27). Where no crop can do
     that (a head right at the photo's own edge) or the drift would slide a
     face under the text, the photo holds still (data-px-hold) instead.
   The zoom and its origin go out as --fz and --fo, so the parallax drift and
   the zoom share one transform. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img[data-faces]'));
  if (!imgs.length) return;
  var ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];

  // head boxes, each with the face's height last (a forced cut takes the smallest face)
  function heads(img, up) {
    var sh = img.getAttribute('data-pad') === 'shoulders';
    return img.getAttribute('data-faces').split(';').map(function (s) {
      var f = s.split(',').map(Number);
      return sh
        ? [Math.max(0, f[0] - 0.9 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.9 * f[2]), Math.min(1, f[1] + 2.2 * f[3]), f[3]]
        : [Math.max(0, f[0] - 0.2 * f[2]), Math.max(0, f[1] - up * f[3]), Math.min(1, f[0] + 1.2 * f[2]), Math.min(1, f[1] + 1.1 * f[3]), f[3]];
    });
  }

  function better(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] < b[i];
    return false;
  }

  // how far the photo runs past its frame top and bottom while parallax is on
  function overscan(img) {
    if (!img.classList.contains('px') || !img.parentElement) return 0;
    var extra = img.offsetHeight - img.parentElement.clientHeight;
    return extra > 2 ? extra / 2 : 0;
  }

  function avoidRects(img, drift) {
    var sel = img.getAttribute('data-avoid'), sec = img.closest('section');
    var op = img.offsetParent;
    if (!sel || !sec || !op) return [];
    // the photo's untransformed box (offsets ignore the zoom and the drift)
    var opr = op.getBoundingClientRect();
    var ir = { left: opr.left + op.clientLeft + img.offsetLeft, top: opr.top + op.clientTop + img.offsetTop };
    return Array.prototype.slice.call(sec.querySelectorAll(sel)).map(function (e) {
      var r = e.getBoundingClientRect();
      return [r.left - ir.left, r.top - ir.top - drift, r.right - ir.left, r.bottom - ir.top + drift];
    }).filter(function (r) { return r[2] > r[0] && r[3] > r[1]; });
  }

  function clear(img) {
    img.style.objectPosition = img._pos0 || '';
    img.style.removeProperty('--fz');
    img.style.removeProperty('--fo');
  }

  function fit(img) {
    var min = Number(img.getAttribute('data-fit-min') || 0);
    if (min && window.innerWidth < min) { clear(img); return; }
    var bw = img.clientWidth, bh = img.clientHeight;
    if (!bw || !bh || !img.naturalWidth || getComputedStyle(img).objectFit !== 'cover') return;
    var o = overscan(img);
    var best = settle(img, bw, bh, o);
    if (o && (best.key[0] > 0 || best.key[1] > 0)) {
      // the drift would cut a head or slide a face under the text: if the
      // photo holding still does better, hold it
      var calm = settle(img, bw, img.parentElement.clientHeight, 0);
      if (better(calm.key.slice(0, 2), best.key.slice(0, 2))) { img.setAttribute('data-px-hold', ''); return; }  // the box change refits it
    }
    apply(img, best);
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

  function search(img, bw, bh, o, up) {
    var m = o ? 2 * o / bh : 0;  // share of the box that can scroll out of view, each end
    var av = avoidRects(img, o);
    var s = Math.max(bw / img.naturalWidth, bh / img.naturalHeight);
    var wx0 = bw / (img.naturalWidth * s), wy0 = bh / (img.naturalHeight * s);
    var hs = heads(img, up);
    var open = img.getAttribute('data-pad') === 'shoulders';
    var pref = (img.getAttribute('data-pos') || '50 50').split(' ').map(Number);
    var best = null;
    ZOOMS.forEach(function (z) {
      var wx = wx0 / z, wy = wy0 / z;
      for (var px = 0; px <= 100; px += 2) {
        for (var py = 0; py <= 100; py += (wy < 0.999 ? 1 : 101)) {
          var ppy = wy < 0.999 ? py : 50;
          var l = px / 100 * (1 - wx), t = ppy / 100 * (1 - wy), r = l + wx, b = t + wy;
          var st = t + m * wy, sb = b - m * wy;  // always on screen
          var cut = 0, inn = 0, txt = 0;
          for (var i = 0; i < hs.length; i++) {
            var h = hs[i];
            if (h[2] <= l || h[0] >= r || h[3] <= t || h[1] >= b) continue;
            if (h[0] >= l - 1e-4 && h[2] <= r + 1e-4 && h[1] >= st - 1e-4 && (open || h[3] <= sb + 1e-4)) {
              inn++;
              var x0 = (h[0] - l) / wx * bw, y0 = (h[1] - t) / wy * bh, x1 = (h[2] - l) / wx * bw, y1 = (h[3] - t) / wy * bh;
              for (var k = 0; k < av.length; k++) {
                if (x0 < av[k][2] && x1 > av[k][0] && y0 < av[k][3] && y1 > av[k][1]) { txt++; break; }
              }
            } else cut += h[4];
          }
          var key = [cut, txt, -inn, z, Math.abs(px - pref[0]) + Math.abs(ppy - pref[1])];
          if (!best || better(key, best.key)) best = { key: key, px: px, py: ppy, z: z };
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
  // refit whenever a photo's box changes size (equal-height splits, fonts,
  // parallax switching on or off at a breakpoint)
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(function (entries) {
      entries.forEach(function (e) { if (e.target.complete) fit(e.target); });
    });
    imgs.forEach(function (img) { ro.observe(img); });
  }
})();
