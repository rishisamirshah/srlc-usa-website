/* Site-wide parallax (Naman, Oct 27): each img.px drifts slower than the page
   inside its frame, by the 6% the photo runs past the frame at each end
   (supplement-zz-px.css), so an edge never shows. Off where the CSS keeps the
   photo flush with its frame (phones, tablets, reduced motion). The QA audit
   sets window.__pxForce to -1 or 1 to hold every photo at the far end it can
   actually reach (a hero starts mid-drift, never at -1). */
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('img.px'));
  if (!imgs.length) return;
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight, force = window.__pxForce;
    imgs.forEach(function (img) {
      var frame = img.parentElement;
      var room = (img.offsetHeight - frame.clientHeight) / 2;
      if (room < 1) { img.style.removeProperty('--py'); return; }
      var r = frame.getBoundingClientRect();
      if (force === undefined && (r.bottom < -room || r.top > vh + room)) return;
      // -1 as the frame enters at the bottom of the screen, +1 as it leaves at the top
      var p = Math.max(-1, Math.min(1, (vh - r.top) / (vh + r.height) * 2 - 1));
      if (force !== undefined) {
        // QA: the far end this frame can actually reach while scrolling
        var top = r.top + window.scrollY, maxS = Math.max(0, document.documentElement.scrollHeight - vh);
        var lo = Math.max(-1, Math.min(1, (vh - top) / (vh + r.height) * 2 - 1));
        var hi = Math.max(-1, Math.min(1, (vh - (top - maxS)) / (vh + r.height) * 2 - 1));
        p = Math.max(lo, Math.min(hi, force));
      }
      img.style.setProperty('--py', (p * room).toFixed(1) + 'px');
    });
  }
  function request() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  window.addEventListener('load', request);
  update();
})();
