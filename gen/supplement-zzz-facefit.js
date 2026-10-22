/* Face-safe crops picked live (Naman, Oct 22: no face cut off in any photo).
   A photo with data-faces (face boxes from gen/qa, as shares of the photo)
   gets the object-position, and if needed a slight zoom, that leaves every
   face fully in or fully out of its visible crop at the size it actually has
   on screen; redone on resize. Order of preference: no face cut, most faces
   in, least zoom, closest to data-pos. Without JS the CSS crop stands. */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img[data-faces]'));
  if (!imgs.length) return;
  var ZOOMS = [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];

  // head box: the face widened 20% each side, 45% above (hair), 10% below
  function heads(img) {
    return img.getAttribute('data-faces').split(';').map(function (s) {
      var f = s.split(',').map(Number);
      return [Math.max(0, f[0] - 0.2 * f[2]), Math.max(0, f[1] - 0.45 * f[3]),
              Math.min(1, f[0] + 1.2 * f[2]), Math.min(1, f[1] + 1.1 * f[3])];
    });
  }

  function better(a, b) {
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] < b[i];
    return false;
  }

  function fit(img) {
    var bw = img.clientWidth, bh = img.clientHeight;
    if (!bw || !bh || !img.naturalWidth || getComputedStyle(img).objectFit !== 'cover') return;
    var s = Math.max(bw / img.naturalWidth, bh / img.naturalHeight);
    var wx0 = bw / (img.naturalWidth * s), wy0 = bh / (img.naturalHeight * s);
    var hs = img._heads || (img._heads = heads(img));
    var pref = (img.getAttribute('data-pos') || '50 50').split(' ').map(Number);
    var best = null;
    ZOOMS.forEach(function (z) {
      var wx = wx0 / z, wy = wy0 / z;
      for (var px = 0; px <= 100; px += 2) {
        for (var py = 0; py <= 100; py += (wy < 0.999 ? 5 : 101)) {
          var ppy = wy < 0.999 ? py : 50;
          var l = px / 100 * (1 - wx), t = ppy / 100 * (1 - wy), r = l + wx, b = t + wy;
          var cut = 0, inn = 0;
          for (var i = 0; i < hs.length; i++) {
            var h = hs[i];
            if (h[2] <= l || h[0] >= r || h[3] <= t || h[1] >= b) continue;
            if (h[0] >= l - 1e-4 && h[2] <= r + 1e-4 && h[1] >= t - 1e-4 && h[3] <= b + 1e-4) inn++;
            else cut++;
          }
          var key = [cut, -inn, z, Math.abs(px - pref[0]) + Math.abs(ppy - pref[1])];
          if (!best || better(key, best.key)) best = { key: key, px: px, py: ppy, z: z };
        }
      }
    });
    var pos = best.px + '% ' + best.py + '%';
    img.style.objectPosition = pos;
    img.style.transformOrigin = pos;
    img.style.transform = best.z > 1 ? 'scale(' + best.z + ')' : '';
  }

  function all() { imgs.forEach(fit); }
  imgs.forEach(function (img) {
    if (img.complete) fit(img); else img.addEventListener('load', function () { fit(img); });
  });
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(all, 120); });
  window.addEventListener('load', all);
})();
