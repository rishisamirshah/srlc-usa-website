/* Story spotlight parallax (Naman, Oct 24): the photo drifts slower than the
   page while the panel moves normally, like childrenssociety.org.uk. Only
   where the photo sits beside the panel (1180px and up); off on phones and
   with reduced motion. The photo box runs 8% past the band top and bottom,
   so the drift never shows an edge. */
(function () {
  var media = Array.prototype.slice.call(document.querySelectorAll('.spot__media'));
  if (!media.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var ticking = false;
  function update() {
    ticking = false;
    var on = window.innerWidth >= 1180, vh = window.innerHeight;
    media.forEach(function (m) {
      if (!on) { m.style.transform = ''; return; }
      var r = m.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      // -1 as the band enters at the bottom, +1 as it leaves at the top
      var p = (vh - r.top) / (vh + r.height) * 2 - 1;
      m.style.transform = 'translate3d(0,' + (p * 0.07 * r.height).toFixed(1) + 'px,0)';
    });
  }
  function request() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  update();
})();
